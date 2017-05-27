#encoding=utf-8

'''
Modified on May 25, 2017

@author: tangr
'''

#成交明细

import sys,os
import unittest
from suds.client import Client
import json

import os, sys

from core import leancloud_patch
import leancloud
from core.Utils import init_leancloud_client

init_leancloud_client()
class TestDeal(unittest.TestCase):

    #webserver 接口测试
    def setUp(self):
        print ("start!")

        #测试接口
        url = "http://10.30.0.122:8091/Stocks.asmx?WSDL"

        client = Client(url)
        # print (client)
        response = client.service.Query_uimsStockTransDataSetList(Coordinates='021525374658617185',
                                                       Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A'
                                                        )
        self.data= json.loads(response)
        print (self.data)

    #写入mc数据测试
    def test_mc(self):
        mc_data = self.data
        AnalogOrder = leancloud.Object.extend('AnalogOrder')
        orderObj = AnalogOrder()

        orderObj.set('stockCode', mc_data["StockCode"])
        orderObj.set('stockName', mc_data["stockname"])
        orderObj.set('marketCode', mc_data["marketcode"])
        orderObj.set('price', mc_data["Price"])
        orderObj.set('volume', mc_data["Volume"])
        orderObj.set('cjje', mc_data["cjje"])
        orderObj.set('transType', mc_data["transType"])
        orderObj.set('dealTime', mc_data["dateTime"])
        orderObj.set('profitorLoss', mc_data["ProfitorLoss"])
        orderObj.set('syl', mc_data["syl"])

        orderObj.save()


if __name__ == "__main__":

    unittest.main()