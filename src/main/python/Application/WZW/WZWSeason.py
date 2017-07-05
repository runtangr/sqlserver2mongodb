#encoding=utf-8

'''
Modified on June 27, 2017

@author: tangr
'''

 #王中王赛季列表

import unittest
from suds.client import Client
import json
from datetime import datetime
import time
import leancloud_patch
import leancloud
from Utils import init_leancloud_client
import logging
import MarketData

logging.basicConfig(level=logging.WARNING,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S'
					)

init_leancloud_client()

class WZWSeason:
    def WZWSeasonPort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        # 王中王赛季列表 WebService 测试接口 Query_SJLB
        response = client.service.Query_SJLB(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A'
                                                    )
        try:
            self.WZWSeason = json.loads(response)

        except Exception, e:
            logging.error("%s:get data error! %s" %(__file__ ,response))

    def WZWSeasonMC(self):
        '''
        mc更新 A_DxtWZWSeason(王中王赛季列表)表
        '''

        if self.WZWSeason["Code"] == 0:

            self.DataObj =  json.loads(self.WZWSeason["DataObj"])#


            map(self.DealData,self.DataObj)


        else:
            logging.warning("%s:get data fail! %s" % (__file__, self.WZWSeason))

    def DealData(self,DataObjArr):

        A_DxtWZWSeasonQuery = leancloud.Query('A_DxtWZWSeason')
        A_DxtWZWSeasonQuery.equal_to('relationId', DataObjArr.values()[0])
        self.A_DxtWZWSeasonList = A_DxtWZWSeasonQuery.find()

        if len(self.A_DxtWZWSeasonList) > 0:

            self.Save(self.A_DxtWZWSeasonList[0],DataObjArr)
        else:
            A_DxtWZWSeason = leancloud.Object.extend('A_DxtWZWSeason')
            A_DxtWZWSeasonObj = A_DxtWZWSeason()
            self.Save(A_DxtWZWSeasonObj,DataObjArr)

    def Save(self,Obj,DataObjArr):

        Obj.set('season', DataObjArr.values()[0])
        Obj.set('name', "第"+ str(DataObjArr.values()[0]) + "赛季")
        Obj.set('relationId', DataObjArr.values()[0])
        Obj.save()

if __name__ == "__main__":

	WZWSeason_object = WZWSeason()

	WZWSeason_object.WZWSeasonPort()
	WZWSeason_object.WZWSeasonMC()

