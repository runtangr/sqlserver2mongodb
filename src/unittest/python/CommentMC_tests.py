#encoding=utf-8

'''
Modified on May 25, 2017

@author: tangr
'''

#专家点评 MC存储测试模块

import unittest
from suds.client import Client
import json
import leancloud_patch
import leancloud
from Utils import init_leancloud_client

init_leancloud_client()

class TestComment(unittest.TestCase):

    #写入mc数据测试
    def test_mc(self):

        #mc更新AnalogComment(专家点评)表
        uimsZJDP = leancloud.Object.extend('uimsZJDP')
        uimsZJDPObj = uimsZJDP()

        uimsZJDPObj.set('rsOperateID', '1')

        uimsZJDPObj.set('rsStatus', "1")
        uimsZJDPObj.set('rsProjectId', "1")
        uimsZJDPObj.set('groupbm', "qwert")
        uimsZJDPObj.set('JudgeContent', "adsgasdgsbfhgs")

        # 还有一些未写出来
        uimsZJDPObj.save()


if __name__ == "__main__":

    unittest.main()