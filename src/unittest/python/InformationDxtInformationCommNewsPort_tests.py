#encoding=utf-8

'''
Modified on June 12, 2017

@author: tangr
'''

#自主新闻查询WebService 接口测试模块

import unittest
from suds.client import Client
import json
import leancloud_patch
import leancloud
from Utils import init_leancloud_client

init_leancloud_client()

class TestCommNews(unittest.TestCase):

    #WebService 接口测试
    def test_WebService(self):
        print ("start!")

        #测试地址
        url = "http://61.139.76.139:9527/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)


        #自主新闻查询 WebService 测试接口Query_CommNews_EDIT
        response = client.service.Query_CommNews_EDIT(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                 rsMainkeyid=0,
                                                 rsDatetime="2000-06-02 10:15:0",
                                                 top=1
                                                                )

        self.data= json.loads(response)
        print (self.data)


if __name__ == "__main__":

    unittest.main()