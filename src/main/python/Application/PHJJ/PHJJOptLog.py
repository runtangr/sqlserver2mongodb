#encoding=utf-8

'''
Modified on July 7, 2017

@author: tangr
'''

 #盘后掘金操作日志

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

class PHJJOptLog:
        
    def PHJJOptLogPort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        # 盘后掘金操作日志 WebService 测试接口 Query_ZCRZ
        response = client.service.Query_ZCRZ(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                            
                                                    )
        try:
            self.PHJJOptLog = json.loads(response)

        except Exception, e:
            logging.error("%s : webservice get data fail! data:%s" %(__file__ ,response))

    def PHJJOptLogMC(self):
        '''
        mc更新 A_DxtPHJJOptLog(盘后掘金操作日志)表
        '''

        if self.PHJJOptLog["Code"] == 0:

            self.DataObj =  json.loads(self.PHJJOptLog["DataObj"])

            # 先删除原有数据
            while True:
                queryPHJJOptLog = leancloud.Query('A_DxtPHJJOptLog')
                query_list = queryPHJJOptLog.find()
                if len(query_list) == 0:
                    break
                leancloud.Object.destroy_all(query_list)

            #存储所有 新数据
            map(self.DealData,self.DataObj)

        else:
             logging.warning("not data or data error：%s" %self.PHJJOptLog)



    def DealData(self,DataObjArr):


        A_DxtPHJJOptLog = leancloud.Object.extend('A_DxtPHJJOptLog')
        A_DxtPHJJOptLogObj = A_DxtPHJJOptLog()
        self.Save(A_DxtPHJJOptLogObj,DataObjArr)

    def Save(self,Obj,DataObjArr):

        self.Calculate(DataObjArr)

        Obj.set('title', DataObjArr['Logtitle'])
        Obj.set('content', DataObjArr['LogContent'])
        Obj.set('publishTime', self.publishTime)

        Obj.set('relationId', DataObjArr['rsmainkeyid'])
        Obj.save()

    def Calculate(self,DataObjArr):
        #时间
        self.publishTime = datetime.strptime(DataObjArr["rsdatetime"], '%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":

	PHJJOptLog_object = PHJJOptLog()

	PHJJOptLog_object.PHJJOptLogPort()
	PHJJOptLog_object.PHJJOptLogMC()

