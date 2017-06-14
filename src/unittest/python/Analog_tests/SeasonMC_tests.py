#encoding=utf-8

'''
Modified on June 8, 2017

@author: tangr
'''

#赛季同步 MC存储测试模块

import unittest
from suds.client import Client
import json
import leancloud_patch
import leancloud
from Utils import init_leancloud_client

init_leancloud_client()

class TestHistRank(unittest.TestCase):

    #写入mc数据测试
    def test_mc(self):

        #mc更新 赛季同步 对应表 uimsuimsSeasonSet
        uimsSeasonSet = leancloud.Object.extend('uimsSeasonSet')
        uimsSeasonSetObj = uimsSeasonSet()

        #参考文档 达人赛.md 或数据库表结构
        uimsSeasonSetObj.set('rsOperateID', '1')
        uimsSeasonSetObj.set('rsStatus', "1")
        uimsSeasonSetObj.set('rsProjectId', "1")
        uimsSeasonSetObj.set('groupbm', "qwert")
        uimsSeasonSetObj.set('JudgeContent', "hello world!")

        # 还有一些未写出来

        uimsSeasonSetObj.save()


if __name__ == "__main__":

    unittest.main()