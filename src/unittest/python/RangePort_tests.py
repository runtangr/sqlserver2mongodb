#encoding=utf-8

'''
Modified on May 25, 2017

@author: tangr
'''

#大赛排名WebService 接口测试模块

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
        url = "http://10.30.0.122:8091/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        #大赛排名 WebService 测试接口Query_uimsSYPM
        response = client.service.Query_uimsSYPM(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                 mainkeyid = 0,
                                                datetime ='Y-m-d H:i:s',
                                                flag = 0
                                                )
        self.data= json.loads(response)
        print (self.data)


if __name__ == "__main__":

    unittest.main()