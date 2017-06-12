#encoding=utf-8

'''
Modified on June 1, 2017

@author: tangr
'''

#获奖感言WebService 接口测试模块

import unittest
from suds.client import Client
import json
import leancloud_patch
import leancloud
from Utils import init_leancloud_client
from datetime import datetime
init_leancloud_client()

class TestSpeech(unittest.TestCase):

    #WebService 接口测试
    def test_WebService(self):
        print ("start!")

        #测试地址
        url = "http://10.30.0.122:8091/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        #获奖感言 WebService 测试接口Query_uimsHJGY
        response = client.service.Query_uimsHJGY(Coordinates='021525374658617185',
                                                 Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                 rsMainkeyID = 0,
                                                 rsDatetime ="2004-02-02 0:0:0"
                                                )

        self.data= json.loads(response)
        print (self.data)


if __name__ == "__main__":

    unittest.main()