#encoding=utf-8

'''
Modified on May 25, 2017

@author: tangr
'''

#成交明细 MC存储测试模块

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

        #mc更新AnalogOrder(成交明细)表
        AnalogOrder = leancloud.Object.extend('AnalogOrder')
        orderObj = AnalogOrder()

        dealTime = {"__type": "Date", "iso": "2011-12-09T01:30:46.000Z"}

        orderObj.set('stockCode', "600009")
        orderObj.set('stockName', "上海机场")
        orderObj.set('marketCode',"SH")
        orderObj.set('price', 12.78)
        orderObj.set('volume', 7800)
        orderObj.set('cjje', 99484.64)
        orderObj.set('transType', "卖")
        orderObj.set('dealTime', dealTime)
        orderObj.set('profitorLoss', -377.12)
        orderObj.set('syl', "-0.38%")
        orderObj.set('userName',"薄荷微凉")
        # 还有一些未写出来
        orderObj.save()


if __name__ == "__main__":

    unittest.main()