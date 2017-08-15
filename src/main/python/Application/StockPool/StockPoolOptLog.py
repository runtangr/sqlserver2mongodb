#encoding=utf-8

'''
Modified on June 27, 2017

@author: tangr
'''

 #股票池近期更新(操作日志)

import unittest
from suds.client import Client
import json
from datetime import datetime
import time
import leancloud_patch
import leancloud
from Utils import init_leancloud_client
import logging
import MarketData

logging.basicConfig(level=logging.WARNING,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S'
					)

init_leancloud_client()

class StockPoolOptLog:
    def StockPoolOptLogPort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        SyncControl = leancloud.Object.extend('SyncControl')
        self.SyncControlObj = SyncControl()
        querySyncInfo = SyncControl.query

        querySyncInfo.equal_to('type', 'StockPoolOptLog')
        syncObj = querySyncInfo.find()
        if len(syncObj)== 0:
            dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
            self.SyncControlObj.set("type","StockPoolOptLog")
            self.SyncControlObj.set("mainKeyId",0)
            self.SyncControlObj.set("rsDateTime","1990-01-01")
            self.SyncControlObj.save()

        self.SyncControlObj = querySyncInfo.first()
        self.maxKeyId = int(self.SyncControlObj.get('mainKeyId'))
        self.rsDateTime = self.SyncControlObj.get('rsDateTime')
        top = 100

        # 股票池近期更新(操作日志) WebService 测试接口 P_Z_CommStockPoolLog
        response = client.service.P_Z_CommStockPoolLog(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                rsMainkeyID=self.maxKeyId,
                                                rsDateTime=self.rsDateTime,
                                                  top=top
                                                    )
        try:
            self.StockPoolOptLog = json.loads(response)

        except Exception, e:
            logging.error("%s  webservice 接口数据获取失败 %s" %(__file__ ,response))

    def StockPoolOptLogMC(self):
        '''
        mc更新 A_DxtStockPoolOptLog(股票池近期更新(操作日志))表
        '''

        maxKeyId = int(self.SyncControlObj.get('mainKeyId'))

        if self.StockPoolOptLog["Code"] == 0:

            self.DataObj =  json.loads(self.StockPoolOptLog["DataObj"])#


            map(self.DealData,self.DataObj)


        else:
            logging.warning("not data or data error：%s" % self.StockPoolOptLog)

    def DealData(self,DataObjArr):

        # 最后一条数据赋值
        if DataObjArr == self.DataObj[-1]:
            self.maxKeyId = int(DataObjArr['rsMainKeyID'])
            self.rsDateTime = DataObjArr['rsDateTime']
            self.SyncControlObj.set('mainKeyId', self.maxKeyId)
            self.SyncControlObj.set('rsDateTime', self.rsDateTime)
            self.SyncControlObj.save()

        #打印
        print ("maxKeyId:", self.maxKeyId, "===", "rsMainkeyID:", DataObjArr['rsMainKeyID'], "===",
               "rsDateTime:", DataObjArr['rsDateTime'])


        A_DxtStockPoolOptLogQuery = leancloud.Query('A_DxtStockPoolOptLog')
        A_DxtStockPoolOptLogQuery.equal_to('relationId', DataObjArr['rsMainKeyID'])
        self.A_DxtStockPoolOptLogList = A_DxtStockPoolOptLogQuery.find()

        # 查找StockPool 匹配relationId ，取出objectid
        A_DxtStockPoolQuery = leancloud.Query('A_DxtStockPool')
        A_DxtStockPoolQuery.equal_to('relationId', str(DataObjArr['PoolStyle']))
        self.A_DxtStockPoolList = A_DxtStockPoolQuery.find()

        # 编辑
        if len(self.A_DxtStockPoolOptLogList) > 0 and len(self.A_DxtStockPoolList) > 0:

            self.Save(self.A_DxtStockPoolOptLogList[0],DataObjArr)
        elif len(self.A_DxtStockPoolList) > 0:
            A_DxtStockPoolOptLog = leancloud.Object.extend('A_DxtStockPoolOptLog')
            A_DxtStockPoolOptLogObj = A_DxtStockPoolOptLog()
            self.Save(A_DxtStockPoolOptLogObj,DataObjArr)

    def Calculate(self, DataObjArr):
        self.publishTime = datetime.strptime(DataObjArr["rsDateTime"],'%Y-%m-%d %H:%M:%S')
        self.optTypeStr = {
                            10:"买入",
                            20:"持有",
                            30:"卖出"
                            }

    def Save(self,Obj,DataObjArr):

        self.Calculate(DataObjArr)

        Obj.set('stockPoolObjectId', self.A_DxtStockPoolList[0].get('objectId'))

        Obj.set('stockCode',DataObjArr["StockCode"])
        Obj.set('stockName', DataObjArr["StockShortName"])
        # Obj.set('marketCode', )
        Obj.set('title',  DataObjArr["LogTitle"])
        Obj.set("content", DataObjArr["LogContent"])

        Obj.set('optType', DataObjArr["LogStyle"])
        Obj.set('optTypeStr', self.optTypeStr[DataObjArr["LogStyle"]])
        Obj.set('publishTime', self.publishTime)

        Obj.set('relationId', DataObjArr['rsMainKeyID'])
        Obj.save()

if __name__ == "__main__":

	StockPoolOptLog_object = StockPoolOptLog()

	StockPoolOptLog_object.StockPoolOptLogPort()
	StockPoolOptLog_object.StockPoolOptLogMC()

