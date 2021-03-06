#encoding=utf-8

'''
Modified on June 8, 2017

@author: tangr
'''

#专家点评WebService 接口测试模块

import unittest
from suds.client import Client
import json
import leancloud_patch
import leancloud
from Utils import init_leancloud_client

init_leancloud_client()

class TestComment(unittest.TestCase):

    #WebService 接口测试
    def test_WebService(self):
        print ("start!")

        #测试地址
        url = "http://114.80.94.175:8084/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)


        #专家点评 WebService 测试接口Query_uimsZJDP
        response = client.service.Query_uimsZJDP(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                 rsMainkeyid=1,
                                                 rsDatetime="2004-02-02"
                                                                )
        self.data= json.loads(response)
        print (self.data)


if __name__ == "__main__":

    unittest.main()