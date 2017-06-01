#encoding=utf-8

'''
Modified on June 1, 2017

@author: tangr
'''

#历史排名 MC存储测试模块

import unittest
from suds.client import Client
import json
from core import leancloud_patch
import leancloud
from core.Utils import init_leancloud_client

init_leancloud_client()

class TestOrder(unittest.TestCase):

    #写入mc数据测试
    def test_mc(self):

        #mc更新 历史排名 对应表 uimsLSPM
        uimsLSPM = leancloud.Object.extend('uimsLSPM') #!!!未知表结构  优先级放低
        uimsLSPMObj = uimsLSPM()

        #参考文档 达人赛.md 或数据库表结构
        uimsLSPMObj.set('groupBmId',18)
        uimsLSPMObj.set('matchName',"达人竞技赛")
        uimsLSPMObj.set('userName',"小强哥")
        uimsLSPMObj.set('syl',"0.00%")
        # 还有一些未写出来

        uimsLSPMObj.save()


if __name__ == "__main__":

    unittest.main()