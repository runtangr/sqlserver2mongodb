#encoding=utf-8

'''
Modified on May 25, 2017

@author: tangr
'''

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

    def test_query(self):

        url = "http://10.30.0.122:8091/Stocks.asmx?WSDL"
        data = {
                "Coordinates":"021525374658617185",
                "Encryptionchar":"F5AC95F60BBEDAA9372AE29B84F5E67A",
                "Userid":"24124"
                 }

        client = Client(url)
        # print (client)
        response = client.service.Query_uimsStockTransDataSetList(Coordinates='021525374658617185',
                                                       Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A'
                                                        )
        data= json.loads(response)
        print (data)

        Todo = leancloud.Object.extend('Todo')
        todo = Todo()
        todo.set('title', '工程师周会')
        todo.set('content', '每周工程师会议，周一下午2点')
        todo.set('location', '会议室')  # 增加一个字段
        todo.save()

if __name__ == "__main__":

    unittest.main()