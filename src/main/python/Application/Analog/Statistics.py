#encoding=utf-8

'''
Modified on June 20, 2017

@author: tangr
'''

 #模拟炒股
 #大赛统计同步
 #未使用本程序！

import unittest
from suds.client import Client
import json
from datetime import datetime
import time
import leancloud_patch
import leancloud
from Utils import init_leancloud_client
import logging

logging.basicConfig(level=logging.WARNING,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S'
					)

init_leancloud_client()

class Statistics:
    def StatisticsPort(self):
        '''
        获取端口数据
        '''
        url = "http://114.80.94.175:8084/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

       

        # 大赛统计同步 WebService 测试接口P_GameStatistic
        response = client.service.P_GameStatistic(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A'
                                                    )
        try:
            self.GameStatistic = json.loads(response)

        except Exception, e:
            logging.error("%s  webservice 接口数据获取失败 %s" %(__file__ ,response))

    def StatisticsMC(self):
        '''
        mc更新 AnalogMatch(大赛统计同步)表
        '''

        if self.GameStatistic["Code"] == 0:

            self.DataObj =  json.loads(self.GameStatistic["DataObj"])

            map(self.DealData,self.DataObj)

        else:
             logging.warning("提交大赛统计同步数据返回失败：%s" %self.GameStatistic)

    def DealData(self,DataObjArr):


        AnalogMatchQuery = leancloud.Query('AnalogMatch')
        AnalogMatchQuery.equal_to('objectId', str(DataObjArr['rsMainKeyID']))
        self.AnalogMatchObj = AnalogMatchQuery.find()
        # 编辑
        if len(self.AnalogMatchObj) > 0:

            self.Edit(DataObjArr)
        else:
            self.Add(DataObjArr)

    def Edit(self,DataObjArr):

        self.AnalogMatchObj.set('StatisticsObjectId', str(DataObjArr['StatisticsID']))
        self.AnalogMatchObj.set('title', DataObjArr['LogTitle'])
        self.AnalogMatchObj.set('content', DataObjArr['LogContent'])
        self.AnalogMatchObj.set('publishTime', DataObjArr['rsDateTime'])  ########
        self.AnalogMatchObj.set('relationId', str(DataObjArr["rsMainKeyID"]))
        self.AnalogMatchObj.save()

    def Add(self,DataObjArr):

        A_DxtStatisticsDiary = leancloud.Object.extend('A_DxtStatisticsDiary')
        A_DxtStatisticsDiaryObj = A_DxtStatisticsDiary()

        A_DxtStatisticsDiaryObj.set('StatisticsObjectId', str(DataObjArr['StatisticsID']))
        A_DxtStatisticsDiaryObj.set('title', DataObjArr['LogTitle'])
        A_DxtStatisticsDiaryObj.set('content', DataObjArr['LogContent'])

        A_DxtStatisticsDiaryObj.set('publishTime', DataObjArr['rsDateTime'])  ########

        A_DxtStatisticsDiaryObj.set('relationId', str(DataObjArr["rsMainKeyID"]))
        A_DxtStatisticsDiaryObj.save()

if __name__ == "__main__":

	Statistics_object = Statistics()

	Statistics_object.StatisticsPort()
	Statistics_object.StatisticsMC()

