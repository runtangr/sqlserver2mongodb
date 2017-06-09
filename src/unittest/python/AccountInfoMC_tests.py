#encoding=utf-8

'''
Modified on May 27, 2017

@author: tangr
'''

#用户查询 MC存储测试模块

import unittest
from suds.client import Client
import json
import leancloud_patch
import leancloud
from Utils import init_leancloud_client

init_leancloud_client()

class TestOrder(unittest.TestCase):

    #写入mc数据测试
    def test_mc(self):

        #mc更新AnalogRange(用户查询)表
        AnalogRange = leancloud.Object.extend('AnalogRange')
        rangeObj = AnalogRange()

        rangeObj.set('groupBmId',18)
        rangeObj.set('matchName',"达人竞技赛")
        rangeObj.set('residualCapital',100000)
        rangeObj.set('analogMatchId',1)
        rangeObj.set('tradeCountYL',0)
        rangeObj.set('pmWeek',4731)
        rangeObj.set('updatedAt', "2017-05-24T07:28:22.980Z")
        rangeObj.set('isDefault', "0")
        rangeObj.set('pm', 12140)
        rangeObj.set('syl', "0.00%")
        rangeObj.set('userName', "小强哥")
        #还有一些未写出来

        rangeObj.save()


if __name__ == "__main__":

    unittest.main()