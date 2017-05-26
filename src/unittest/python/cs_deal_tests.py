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
class Test(unittest.TestCase):

    def test_deal(self):
        #测试接口
        url = "http://10.30.0.122:8091/Stocks.asmx?WSDL"

        client = Client(url)
        # print (client)
        response = client.service.Query_uimsStockTransDataSetList(Coordinates='021525374658617185',
                                                       Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A'
                                                        )
        data= json.loads(response)
        print (data)

        AnalogOrder = leancloud.Object.extend('AnalogOrder')
        orderObj = AnalogOrder()

        orderObj.set('stockCode', data["StockCode"])
        orderObj.set('stockName', data["stockname"])
        orderObj.set('marketCode', data["marketcode"])
        orderObj.set('price', data["Price"])
        orderObj.set('volume', data["Volume"])
        orderObj.set('cjje', data["cjje"])
        orderObj.set('transType', data["transType"])
        orderObj.set('dealTime', data["dateTime"])
        orderObj.set('profitorLoss', data["ProfitorLoss"])
        orderObj.set('syl', data["syl"])

        orderObj.save();


if __name__ == "__main__":

    unittest.main()