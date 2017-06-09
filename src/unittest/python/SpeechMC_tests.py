#encoding=utf-8

'''
Modified on June 1, 2017

@author: tangr
'''

#获奖感言 MC存储测试模块

import unittest
from suds.client import Client
import json
import leancloud_patch
import leancloud
from Utils import init_leancloud_client

init_leancloud_client()

class TestSpeech(unittest.TestCase):

    #写入mc数据测试
    def test_mc(self):

        #mc更新 获奖感言 对应表 uimsHJGY
        uimsHJGY = leancloud.Object.extend('uimsHJGY') #!!!未知表结构  优先级放低
        uimsHJGYObj = uimsHJGY()

        #参考文档 达人赛.md 或数据库表结构
        uimsHJGYObj.set('groupBmId',18)
        uimsHJGYObj.set('matchName',"达人竞技赛")
        uimsHJGYObj.set('userName',"小强哥")
        uimsHJGYObj.set('syl',"0.00%")
        # 还有一些未写出来

        uimsHJGYObj.save()


if __name__ == "__main__":

    unittest.main()