#encoding=utf-8

'''
Modified on June 8, 2017

@author: tangr
'''

#牛股榜 MC存储测试模块

import unittest
from suds.client import Client
import json
import leancloud_patch
import leancloud
from Utils import init_leancloud_client

init_leancloud_client()

class TestNiuguList(unittest.TestCase):

    #写入mc数据测试
    def test_mc(self):

        #mc更新 牛股榜 对应表 uimsNGB
        uimsNGBSet = leancloud.Object.extend('uimsNGB')
        uimsNGBSetObj = uimsNGBSet()

        #参考文档 达人赛.md 或数据库表结构
        uimsNGBSetObj.set('rsOperateID', '1')
        uimsNGBSetObj.set('rsStatus', "1")
        uimsNGBSetObj.set('rsProjectId', "1")
        uimsNGBSetObj.set('groupbm', 'balabala')
        uimsNGBSetObj.set('StockCode', "800013")
        uimsNGBSetObj.set('Stockid', "23524")

        # 还有一些未写出来

        uimsNGBSetObj.save()


if __name__ == "__main__":

    unittest.main()