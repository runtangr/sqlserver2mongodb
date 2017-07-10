#encoding=utf-8

'''
Modified on July 7, 2017

@author: tangr
'''

 #盘后掘金历史收益率表

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

class PHJJHisSyl:

    def PHJJHisSylPort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        # 盘后掘金历史收益率表 WebService 测试接口 Query_PHJJZF
        response = client.service.Query_PHJJZF(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                    )
        try:
            self.PHJJHisSyl = json.loads(response)

        except Exception, e:
            logging.error("%s : webservice get data fail! data:%s" %(__file__ ,response))

    def PHJJHisSylMC(self):
        '''
        mc更新 A_DxtPHJJHisSyl(盘后掘金历史收益率表)表
        '''

        if self.PHJJHisSyl["Code"] == 0:

            self.DataObj =  json.loads(self.PHJJHisSyl["DataObj"])

            #删除
            while True:
                queryPHJJHisSyl = leancloud.Query('A_DxtPHJJHisSyl')
                # queryPHJJHisSyl.limit(1000)
                query_list = queryPHJJHisSyl.find()
                if len(query_list) ==0:
                    break
                # count =  queryPHJJHisSyl.count()
                leancloud.Object.destroy_all(query_list)

            #存储所有 新数据
            map(self.DealData,self.DataObj)

        else:
             logging.warning("not data or data error：%s" %self.PHJJHisSyl)

    def DealData(self,DataObjArr):


        A_DxtPHJJHisSyl = leancloud.Object.extend('A_DxtPHJJHisSyl')
        A_DxtPHJJHisSylObj = A_DxtPHJJHisSyl()
        self.Save(A_DxtPHJJHisSylObj, DataObjArr)

    def Save(self,Obj,DataObjArr):
        self.Calculate(DataObjArr)

        Obj.set('syl',DataObjArr["sy"])
        Obj.set('settleTime', self.settleTime)

        Obj.save()

    def Calculate(self,DataObjArr):

        #时间转换
        self.settleTime = datetime.strptime(DataObjArr["syDate"], "%Y-%m-%d")

if __name__ == "__main__":

	PHJJHisSyl_object = PHJJHisSyl()

	PHJJHisSyl_object.PHJJHisSylPort()
	PHJJHisSyl_object.PHJJHisSylMC()

