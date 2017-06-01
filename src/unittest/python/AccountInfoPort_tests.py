#encoding=utf-8

'''
Modified on May 27, 2017

@author: tangr
'''

#用户查询WebService 接口测试模块

import unittest
from suds.client import Client
import json
from core import leancloud_patch
import leancloud
from core.Utils import init_leancloud_client

init_leancloud_client()

class TestOrder(unittest.TestCase):

    #WebService 接口测试
    def test_WebService(self):
        print ("start!")

        #测试地址
        url = "http://180.169.122.18:8091/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        #用户查询 WebService 测试接口AppSoftGet_uimsStockTransList
        response = client.service.AppSoftGet_uimsStockTransList(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A'
                                                )
        self.data= json.loads(response)
        print (self.data)


if __name__ == "__main__":

    unittest.main()