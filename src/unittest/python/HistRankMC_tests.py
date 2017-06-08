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

class TestHistRank(unittest.TestCase):

    #写入mc数据测试
    def test_mc(self):

        #mc更新 历史排名 对应表 uimsLSPM
        uimsLSPM = leancloud.Object.extend('uimsLSPM')
        uimsLSPMObj = uimsLSPM()

        #参考文档 达人赛.md 或数据库表结构
        uimsLSPMObj.set('rsOperateID', '1')
        uimsLSPMObj.set('rsStatus', "1")
        uimsLSPMObj.set('rsProjectId', "1")
        uimsLSPMObj.set('groupbm', "qwert")
        uimsLSPMObj.set('JudgeContent', "adsgasdgsbfhgs")
        # 还有一些未写出来

        uimsLSPMObj.save()


if __name__ == "__main__":

    unittest.main()