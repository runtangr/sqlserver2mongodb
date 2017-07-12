#encoding=utf-8

'''
Modified on June 29, 2017

@author: tangr
'''

 #王中王战绩快报表

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

class WZWNews:
    def WZWNewsPort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        SyncControl = leancloud.Object.extend('SyncControl')
        self.SyncControlObj = SyncControl()
        querySyncInfo = SyncControl.query

        querySyncInfo.equal_to('type', 'WZWNews')
        syncObj = querySyncInfo.find()
        if len(syncObj)== 0:
            dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
            self.SyncControlObj.set("type","WZWNews")
            self.SyncControlObj.set("mainKeyId",0)
            self.SyncControlObj.set("rsDateTime","1990-01-01")
            self.SyncControlObj.save()

        self.SyncControlObj = querySyncInfo.first()
        self.maxKeyId = int(self.SyncControlObj.get('mainKeyId'))
        self.rsDateTime = self.SyncControlObj.get('rsDateTime')
        top = 100

        # 王中王战绩快报表 WebService 测试接口P_Z_uimsVSGG_Pro
        response = client.service.P_Z_uimsVSGG_Pro (Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                rsMainkeyID=self.maxKeyId,
                                                rsDateTime=self.rsDateTime,
                                                  top=top
                                                    )
        try:
            self.WZWNews = json.loads(response)

        except Exception, e:
            logging.error("%s  webservice 接口数据获取失败 %s" %(__file__ ,response))

    def WZWNewsMC(self):
        '''
        mc更新 A_DxtWZWNews(王中王战绩快报表)表
        '''

        maxKeyId = int(self.SyncControlObj.get('mainKeyId'))

        if self.WZWNews["Code"] == 0:

            self.DataObj =  json.loads(self.WZWNews["DataObj"])#


            map(self.DealData,self.DataObj)


        else:
             logging.warning("提交王中王战绩快报表数据返回失败：%s" %self.WZWNews)

    def DealData(self,DataObjArr):

        #最后一条数据赋值
        if DataObjArr==self.DataObj[-1]:
            self.maxKeyId = int(DataObjArr['rsMainkeyID'])
            self.rsDateTime = DataObjArr['rsdatetime']
            self.SyncControlObj.set('mainKeyId', self.maxKeyId)
            self.SyncControlObj.set('rsDateTime', self.rsDateTime)
            self.SyncControlObj.save()

        #打印
        print ("maxKeyId:", self.maxKeyId, "===", "rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
               "rsDateTime:", DataObjArr['rsdatetime'])

        #数据处理
        #时间格式处理
        self.publishTime = datetime.strptime(DataObjArr["rsdatetime"],'%Y-%m-%d %H:%M:%S')
        # self.dealTime = datetime.strptime(DataObjArr["CJDate"], '%Y-%m-%d %H:%M:%S')
        # totalCapital = DataObjArr["ResidualCapital"] + DataObjArr["ResidualCapital"]

        A_DxtWZWNewsQuery = leancloud.Query('A_DxtWZWNews')
        A_DxtWZWNewsQuery.equal_to('relationId', DataObjArr['rsMainkeyID'])
        self.A_DxtWZWNewsList = A_DxtWZWNewsQuery.find()

        # 查找A_DxtWZWTeacher VGroupID，取出teacherObjectId
        A_DxtWZWTeacherQuery = leancloud.Query('A_DxtWZWTeacher')
        A_DxtWZWTeacherQuery.equal_to('groupBmId', DataObjArr["VgroupID"])
        self.A_DxtWZWTeacherList = A_DxtWZWTeacherQuery.find()
        # 编辑
        if len(self.A_DxtWZWNewsList) > 0 and len(self.A_DxtWZWTeacherList)>0:

            self.Save(self.A_DxtWZWNewsList[0],DataObjArr)
        elif len(self.A_DxtWZWTeacherList)>0:
            A_DxtWZWNews = leancloud.Object.extend('A_DxtWZWNews')
            A_DxtWZWNewsObj = A_DxtWZWNews()
            self.Save(A_DxtWZWNewsObj,DataObjArr)

    def Save(self,Obj,DataObjArr):
        Obj.set('groupBmId', DataObjArr['VgroupID'])
        Obj.set('teacherObjectId', self.A_DxtWZWTeacherList[0].get("objectId"))
        Obj.set('stockCode', DataObjArr['stockcode'])
        Obj.set('stockName', DataObjArr['stockshortname'])
        Obj.set('marketCode', DataObjArr["MarketCode"])

        Obj.set('zdf',DataObjArr["Price_ZDF"] )
        Obj.set('publishTime', self.publishTime)

        Obj.set('relationId', DataObjArr['rsMainkeyID'])
        Obj.save()

if __name__ == "__main__":

	WZWNews_object = WZWNews()

	WZWNews_object.WZWNewsPort()
	WZWNews_object.WZWNewsMC()

