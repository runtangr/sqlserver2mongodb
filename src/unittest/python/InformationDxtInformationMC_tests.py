#encoding=utf-8

'''
Modified on June 12, 2017

@author: tangr
'''

#自主新闻查询 MC存储测试模块

import unittest
from suds.client import Client
import json
import leancloud_patch
import leancloud
from Utils import init_leancloud_client

init_leancloud_client()

class TestCommNews(unittest.TestCase):

    #写入mc数据测试
    def test_mc(self):

        #mc更新A_DxtInformation 资讯栏目更新表
        A_DxtInformation = leancloud.Object.extend('A_DxtInformation')
        A_DxtInformationObj = A_DxtInformation()

        A_DxtInformationObj.set('title', "xyz")
        # A_DxtInformationObj.set('source', "")
        # A_DxtInformationObj.set('summary', "")  ##content
        # A_DxtInformationObj.set('thumbnail', "")
        # A_DxtInformationObj.set('url', "www.baidu.com")
        # A_DxtInformationObj.set('content', "afsafsa")
        # A_DxtInformationObj.set('srcContent', "afsafsa")
        #
        # A_DxtInformationObj.set('author',"tangr")
        # A_DxtInformationObj.set('publishTime', "2017-06-14")
        # A_DxtInformationObj.set('clickNumber', "")
        # A_DxtInformationObj.set('likeNumber', "")
        # A_DxtInformationObj.set('shareNumber', "")
        # A_DxtInformationObj.set('collectNumber', "")
        # A_DxtInformationObj.set('relationId', "100")
        #
        Data = {}
        Data["Images"] = 'Images'
        Data["NewsID"] = 'NewsID'
        Data["rsDateTime"] = 'rsDateTime'
        Data["rsDispIndex"] ='rsDispIndex'
        Data["rsStatus"] = 'rsStatus'
        #
        A_DxtInformationObj.set('images', Data)
        A_DxtInformationObj.save()

        # 还有一些未写出来
        # A_DxtInformationObj.save()


if __name__ == "__main__":

    unittest.main()