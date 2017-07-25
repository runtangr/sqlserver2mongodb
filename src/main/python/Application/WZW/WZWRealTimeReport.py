#encoding=utf-8

'''
Modified on June 27, 2017

@author: tangr
'''

 #王中王实时战绩播报

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

class WZWRealTimeReport:
    def WZWRealTimeReportPort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        # 王中王实时战绩播报 WebService 测试接口 P_N_SSZJBB_WZW
        response = client.service.P_N_SSZJBB_WZW(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A'
                                                    )
        try:
            self.WZWRealTimeReport = json.loads(response)

        except Exception, e:
            logging.error("%s  webservice 接口数据获取失败 %s" %(__file__ ,response))

    def WZWRealTimeReportMC(self):
        '''
        mc更新 A_DxtWZWRealTimeReport(王中王实时战绩播报)表
        '''

        if self.WZWRealTimeReport["Code"] == 0:

            self.DataObj =  json.loads(self.WZWRealTimeReport["DataObj"])#

            # 先删除原有数据
            while True:
                queryWZWRealTimeReport = leancloud.Query('A_DxtWZWRealTimeReport')
                query_list = queryWZWRealTimeReport.find()
                if len(query_list) == 0:
                    break
                leancloud.Object.destroy_all(query_list)


            map(self.DealData,self.DataObj)

        else:
            logging.warning("not data or data error：%s" % self.WZWRealTimeReport)

    def DealData(self,DataObjArr):

        #打印
        print ("rsDateTime:", DataObjArr['rsDateTime'])

        A_DxtWZWRealTimeReport = leancloud.Object.extend('A_DxtWZWRealTimeReport')
        A_DxtWZWRealTimeReportObj = A_DxtWZWRealTimeReport()
        self.Save(A_DxtWZWRealTimeReportObj,DataObjArr)

    def Calculate(self, DataObjArr):

        self.dealTime = datetime.strptime(DataObjArr["rsDateTime"],'%Y-%m-%d %H:%M:%S')

    def Save(self,Obj,DataObjArr):

        self.Calculate(DataObjArr)
        # Obj.set('groupBmId', )

        Obj.set('stockCode', DataObjArr['StockCode'])
        Obj.set('stockName', DataObjArr['StockShortName'])
        # Obj.set('marketCode', )

        Obj.set('teacherName',DataObjArr["NickName"] )

        Obj.set('profitorLoss', DataObjArr['OtherDefine3'])
        Obj.set('transType', DataObjArr['OtherDefine2'])
        Obj.set('dealTime',  self.dealTime)
        Obj.save()

if __name__ == "__main__":

	WZWRealTimeReport_object = WZWRealTimeReport()

	WZWRealTimeReport_object.WZWRealTimeReportPort()
	WZWRealTimeReport_object.WZWRealTimeReportMC()

