#encoding=utf-8

'''
Modified on June 20, 2017

@author: tangr
'''

 #股票池日总结

import unittest
from suds.client import Client
import json
from datetime import datetime
import time
import leancloud_patch
import leancloud
from Utils import init_leancloud_client
import logging

logging.basicConfig(level=logging.WARNING,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S'
					)

init_leancloud_client()

class StockPool:
    def StockPoolPort(self):
        '''
        获取端口数据
        '''
        url = "http://61.139.76.139:9527/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        SyncControl = leancloud.Object.extend('SyncControl')
        self.SyncControlObj = SyncControl()
        querySyncInfo = SyncControl.query

        querySyncInfo.equal_to('type', 'StockPoolDiary')
        syncObj = querySyncInfo.find()
        if len(syncObj)== 0:
            dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
            self.SyncControlObj.set("type","StockPoolDiary")
            self.SyncControlObj.set("mainKeyId",0)
            self.SyncControlObj.set("rsDateTime","2010-06-20")#每日总结 时间从 2010-06-22 开始
            self.SyncControlObj.save()

        self.SyncControlObj = querySyncInfo.first()
        self.maxKeyId = int(self.SyncControlObj.get('mainKeyId'))
        self.rsDateTime = self.SyncControlObj.get('rsDateTime')
        top = 200

        # 股票池日总结 WebService 测试接口Query_CommNews_EDIT  资讯CommNews_EDIT表
        response = client.service.Query_CommNews_EDIT(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                rsMainkeyid=self.maxKeyId,
                                                rsDatetime=self.rsDateTime,
                                                  top=top
                                                    )
        try:
            self.CommStockPoolLog = json.loads(response)

        except Exception, e:
            logging.error("%s  webservice 接口数据获取失败 %s" %(__file__ ,response))

    def StockPoolMC(self):
        '''
        mc更新 A_DxtStockPoolDiary(股票池日总结)表
        '''

        maxKeyId = int(self.SyncControlObj.get('mainKeyId'))

        if self.CommStockPoolLog["Code"] == 0:

            self.DataObj =  json.loads(self.CommStockPoolLog["DataObj"])#
            # newsStyle = 28000 为机构实战池
            # newsStyle = 31161 为机构研报池
            # newsStyle = 27590 为天机一号池
            self.StcokPool={"28000":"机构实战池",
                            "31161":"机构研报池",
                           "27590":"天玑I号池"}
            self.StcokPoolList= list(self.StcokPool.keys())


            map(self.DealData,self.DataObj)

            #最后保存同步数据
            self.SyncControlObj.set('mainKeyId', self.maxKeyId)
            self.SyncControlObj.set('rsDateTime', self.rsDateTime)
            self.SyncControlObj.save()

        else:
             logging.warning("提交股票池股票池日总结数据返回失败：%s" %self.CommStockPoolLog)

    def DealData(self,DataObjArr):

        if DataObjArr["NewsStyle"] not in self.StcokPoolList:
            return
        #此处无法判断左后一条数据，每次赋值
        # if DataObjArr==self.DataObj[-1]:
        self.maxKeyId = int(DataObjArr['rsMainkeyID'])
        self.rsDateTime = DataObjArr['rsDateTime']

        #打印
        print ("maxKeyId:", self.maxKeyId, "===", "rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
               "rsDateTime:", DataObjArr['rsDateTime'])

        #数据处理
        self.NewsDate = datetime.strptime(DataObjArr['NewsDate'][:-5],'%Y-%m-%d %H:%M:%S')

        A_DxtStockPoolStockQuery = leancloud.Query('A_DxtStockPoolDiary')
        A_DxtStockPoolStockQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
        self.A_DxtStockPoolStockList = A_DxtStockPoolStockQuery.find()

        #查找StockPool 匹配name ，取出objectid
        A_DxtStockPoolQuery = leancloud.Query('A_DxtStockPool')
        A_DxtStockPoolQuery.equal_to('name', self.StcokPool[DataObjArr["NewsStyle"]])
        self.A_DxtStockPoolList = A_DxtStockPoolQuery.find()
        # 编辑
        if len(self.A_DxtStockPoolStockList) > 0:

            self.Edit(DataObjArr)
        else:
            self.Add(DataObjArr)

    def Edit(self,DataObjArr):

        self.A_DxtStockPoolStockList[0].set('stockPoolObjectId', self.A_DxtStockPoolList[0].get("objectId"))
        self.A_DxtStockPoolStockList[0].set('title', DataObjArr['NewsTitle'])
        self.A_DxtStockPoolStockList[0].set('content', DataObjArr['NewsContent'])
        self.A_DxtStockPoolStockList[0].set('publishTime', self.NewsDate)  ########
        self.A_DxtStockPoolStockList[0].set('relationId', str(DataObjArr["rsMainkeyID"]))
        self.A_DxtStockPoolStockList[0].save()

    def Add(self,DataObjArr):

        A_DxtStockPoolDiary = leancloud.Object.extend('A_DxtStockPoolDiary')
        A_DxtStockPoolDiaryObj = A_DxtStockPoolDiary()

        A_DxtStockPoolDiaryObj.set('stockPoolObjectId', self.A_DxtStockPoolList[0].get("objectId"))
        A_DxtStockPoolDiaryObj.set('title', DataObjArr['NewsTitle'])
        A_DxtStockPoolDiaryObj.set('content', DataObjArr['NewsContent'])
        A_DxtStockPoolDiaryObj.set('publishTime', self.NewsDate)  ########
        A_DxtStockPoolDiaryObj.set('relationId', str(DataObjArr["rsMainkeyID"]))
        A_DxtStockPoolDiaryObj.save()

if __name__ == "__main__":

	StockPool_object = StockPool()

	StockPool_object.StockPoolPort()
	StockPool_object.StockPoolMC()

