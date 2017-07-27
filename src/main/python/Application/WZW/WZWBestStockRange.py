#encoding=utf-8

'''
Modified on June 27, 2017

@author: tangr
'''

 #王中王牛股英雄榜

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

class WZWBestStockRange:
    def WZWBestStockRangePort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        top = 500

        # 王中王牛股英雄榜 WebService 测试接口 Query_StockNGB
        response = client.service.Query_StockNGB(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                 Userid=0,
                                                 PageSize=10000,
                                                 Page=1,
                                                 TotalNum=top
                                                    )
        try:
            self.WZWBestStockRange = json.loads(response)

        except Exception, e:
            logging.error("%s  webservice 接口数据获取失败 %s" %(__file__ ,response))

    def WZWBestStockRangeMC(self):
        '''
        mc更新 A_DxtWZWBestStockRange(王中王牛股英雄榜)表
        '''

        if self.WZWBestStockRange["Code"] == 0:

            self.DataObj =  json.loads(self.WZWBestStockRange["DataObj"])#

            # 先删除原有数据
            while True:
                queryWZWBestStockRange = leancloud.Query('A_DxtWZWBestStockRange')
                query_list = queryWZWBestStockRange.find()
                if len(query_list) == 0:
                    break
                leancloud.Object.destroy_all(query_list)

            map(self.DealData,self.DataObj)


        else:
            logging.warning("not data or data error：%s" % self.WZWBestStockRange)

    def DealData(self,DataObjArr):


        A_DxtWZWBestStockRange = leancloud.Object.extend('A_DxtWZWBestStockRange')
        A_DxtWZWBestStockRangeObj = A_DxtWZWBestStockRange()
        self.Save(A_DxtWZWBestStockRangeObj,DataObjArr)

    def Calculate(self, DataObjArr):
        pass
        # self.dealTime = datetime.strptime(DataObjArr["rsDateTime"],'%Y-%m-%d %H:%M:%S')
        # self.AlertNewsDate = datetime.strptime(DataObjArr["AlertNewsDate"],'%Y-%m-%d')

    def Save(self,Obj,DataObjArr):

        self.Calculate(DataObjArr)

        Obj.set('stockCode',DataObjArr["stockCode"])
        Obj.set('stockName', DataObjArr["StockShortName"])
        # Obj.set('marketCode',)
        Obj.set('inPrice',  DataObjArr["Price"])
        Obj.set("zdf", DataObjArr["Price_ZDF"])
        Obj.set("StockID", DataObjArr["StockID"])

        # Obj.set("dealTime", )
        # Obj.set('relationId', DataObjArr['rsMainkeyID'])
        Obj.save()

if __name__ == "__main__":

	WZWBestStockRange_object = WZWBestStockRange()

	WZWBestStockRange_object.WZWBestStockRangePort()
	WZWBestStockRange_object.WZWBestStockRangeMC()

