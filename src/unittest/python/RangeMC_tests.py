#encoding=utf-8

'''
Modified on May 25, 2017

@author: tangr
'''

#大赛排名 MC存储测试模块

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

        #mc更新AnalogRange(大赛排名)表
        AnalogRange = leancloud.Object.extend('AnalogRange')
        rangeObj = AnalogRange()

        rangeObj.set('pm',1)
        rangeObj.set('type',1)
        rangeObj.set('groupBmId',8687)
        rangeObj.set('groupBm',"黑天鹅")
        rangeObj.set('userName',"黑天鹅")
        rangeObj.set('syl',"9.8969%")
        # 还有一些未写出来

        rangeObj.save()


if __name__ == "__main__":

    unittest.main()