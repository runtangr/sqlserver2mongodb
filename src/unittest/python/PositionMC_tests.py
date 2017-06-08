#encoding=utf-8

'''
Modified on June 1, 2017

@author: tangr
'''

#资金持仓 MC存储测试模块

import unittest
from suds.client import Client
import json
from core import leancloud_patch
import leancloud
from core.Utils import init_leancloud_client

init_leancloud_client()

class TestPosition(unittest.TestCase):

    #写入mc数据测试
    def test_mc(self):

        #mc更新 资金持仓对应表 AnalogMyMatch  AnalogStock
        AnalogMyMatch = leancloud.Object.extend('AnalogMyMatch')
        MyMatchObj = AnalogMyMatch()

        #参考文档 达人赛.md 或数据库表结构
        MyMatchObj.set('groupBmId',181)
        MyMatchObj.set('matchName',"达人竞技赛")
        MyMatchObj.set('userName',"小强de哥")
        MyMatchObj.set('syl',"0.00%")
        # 还有一些未写出来

        MyMatchObj.save()

        AnalogStock = leancloud.Object.extend('AnalogStock')
        StockObj = AnalogStock()

        #参考文档 达人赛.md 或数据库表结构
        StockObj.set('groupBmId',245991)
        StockObj.set('matchName',"达人竞技赛")
        StockObj.set('userName',"欢乐de 英雄")
        StockObj.set('stockName',"光明地产")
        StockObj.set('stockTypeName',"A股")
        # 还有一些未写出来

        StockObj.save()

if __name__ == "__main__":

    unittest.main()