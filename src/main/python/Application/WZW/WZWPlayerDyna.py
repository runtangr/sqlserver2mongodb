#encoding=utf-8

'''
Modified on June 27, 2017

@author: tangr
'''

 #王中王高手动态

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

class WZWPlayerDyna:
    def WZWPlayerDynaPort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        SyncControl = leancloud.Object.extend('SyncControl')
        self.SyncControlObj = SyncControl()
        querySyncInfo = SyncControl.query

        querySyncInfo.equal_to('type', 'WZWPlayerDyna')
        syncObj = querySyncInfo.find()
        if len(syncObj)== 0:
            dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
            self.SyncControlObj.set("type","WZWPlayerDyna")
            self.SyncControlObj.set("mainKeyId",0)
            self.SyncControlObj.set("rsDateTime","1990-01-01")
            self.SyncControlObj.save()

        self.SyncControlObj = querySyncInfo.first()
        self.maxKeyId = int(self.SyncControlObj.get('mainKeyId'))
        self.rsDateTime = self.SyncControlObj.get('rsDateTime')
        top = 100

        # 王中王高手动态 WebService 测试接口 P_Z_CommUserAlert_dx
        response = client.service.P_Z_CommUserAlert_dx(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                rsMainkeyID=self.maxKeyId,
                                                rsDateTime=self.rsDateTime,
                                                  top=top
                                                    )
        try:
            self.WZWPlayerDyna = json.loads(response)

        except Exception, e:
            logging.error("%s  webservice 接口数据获取失败 %s" %(__file__ ,response))

    def WZWPlayerDynaMC(self):
        '''
        mc更新 A_DxtWZWPlayerDyna(王中王高手动态)表
        '''

        maxKeyId = int(self.SyncControlObj.get('mainKeyId'))

        if self.WZWPlayerDyna["Code"] == 0:

            self.DataObj =  json.loads(self.WZWPlayerDyna["DataObj"])#


            map(self.DealData,self.DataObj)


        else:
            logging.warning("not data or data error：%s" % self.WZWPlayerDyna)

    def DealData(self,DataObjArr):

        # 最后一条数据赋值
        if DataObjArr == self.DataObj[-1]:
            self.maxKeyId = int(DataObjArr['rsMainkeyID'])
            self.rsDateTime = DataObjArr['rsDateTime']
            self.SyncControlObj.set('mainKeyId', self.maxKeyId)
            self.SyncControlObj.set('rsDateTime', self.rsDateTime)
            self.SyncControlObj.save()

        #打印
        print ("maxKeyId:", self.maxKeyId, "===", "rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
               "rsDateTime:", DataObjArr['rsDateTime'])

        #数据处理
        #时间格式处理
        # self.wtTime = datetime.strptime(DataObjArr["wtTime"],'%Y-%m-%d %H:%M:%S')
        # self.dealTime = datetime.strptime(DataObjArr["CJDate"], '%Y-%m-%d %H:%M:%S')


        A_DxtWZWPlayerDynaQuery = leancloud.Query('A_DxtWZWPlayerDyna')
        A_DxtWZWPlayerDynaQuery.equal_to('relationId', DataObjArr['rsMainkeyID'])
        self.A_DxtWZWPlayerDynaList = A_DxtWZWPlayerDynaQuery.find()

        # 编辑
        if len(self.A_DxtWZWPlayerDynaList) > 0:

            self.Save(self.A_DxtWZWPlayerDynaList[0],DataObjArr)
        else:
            A_DxtWZWPlayerDyna = leancloud.Object.extend('A_DxtWZWPlayerDyna')
            A_DxtWZWPlayerDynaObj = A_DxtWZWPlayerDyna()
            self.Save(A_DxtWZWPlayerDynaObj,DataObjArr)

    def Calculate(self, DataObjArr):
        self.dealTime = datetime.strptime(DataObjArr["rsDateTime"],'%Y-%m-%d %H:%M:%S')
        self.AlertNewsDate = datetime.strptime(DataObjArr["AlertNewsDate"],'%Y-%m-%d')

    def Save(self,Obj,DataObjArr):

        self.Calculate(DataObjArr)

        # Obj.set('groupBmId', )
        # Obj.set('stockCode', )
        Obj.set('stockName', DataObjArr['StockShortName'])
        # Obj.set('marketCode', )

        Obj.set('teacherName',DataObjArr["UserName"])
        Obj.set('price', DataObjArr["cjj"])
        Obj.set('transType', DataObjArr["UserCZ"])
        Obj.set('dealTime',  self.dealTime)
        Obj.set("AlertNewsDate",self.AlertNewsDate)
        Obj.set('relationId', DataObjArr['rsMainkeyID'])
        Obj.save()

if __name__ == "__main__":

	WZWPlayerDyna_object = WZWPlayerDyna()

	WZWPlayerDyna_object.WZWPlayerDynaPort()
	WZWPlayerDyna_object.WZWPlayerDynaMC()

