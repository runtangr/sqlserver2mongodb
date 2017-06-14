#encoding=utf-8

'''
Modified on May 25, 2017

@author: tangr
'''

#大赛统计 MC存储测试模块

import unittest
from suds.client import Client
import json
import leancloud_patch
import leancloud
from Utils import init_leancloud_client

init_leancloud_client()

class TestStatistics(unittest.TestCase):

    #写入mc数据测试
    def test_mc(self):

        #mc更新AnalogMatch(大赛统计)表
        AnalogMatch = leancloud.Object.extend('AnalogMatch')
        AnalogMatchObj = AnalogMatch()

        AnalogMatchObj.set('rsOperateID', '1')

        AnalogMatchObj.set('rsStatus', "1")
        AnalogMatchObj.set('rsProjectId', "1")
        AnalogMatchObj.set('groupbm', "qwert")
        AnalogMatchObj.set('JudgeContent', "adsgasdgsbfhgs")

        # 还有一些未写出来
        AnalogMatchObj.save()


if __name__ == "__main__":

    unittest.main()