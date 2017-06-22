#encoding=utf-8

'''
Modified on June 20, 2017

@author: tangr
'''

 #年最高涨幅榜

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

class StockPoolYearRank:
    def StockPoolYearRankPort(self):
        '''
        获取端口数据
        '''
        url = "http://125.70.0.228:9525/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
        self.AnalogSyncInfoObj = AnalogSyncInfo()
        querySyncInfo = AnalogSyncInfo.query

        querySyncInfo.equal_to('type', 'StockPoolYearRank')
        syncObj = querySyncInfo.find()
        if len(syncObj)== 0:
            dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
            self.AnalogSyncInfoObj.set("type","StockPoolYearRank")
            self.AnalogSyncInfoObj.set("mainKeyId",0)
            self.AnalogSyncInfoObj.set("AccessDateTime","1990-01-01")
            self.AnalogSyncInfoObj.save()

        self.AnalogSyncInfoObj = querySyncInfo.first()
        self.maxKeyId = int(self.AnalogSyncInfoObj.get('mainKeyId'))
        self.rsDateTime = self.AnalogSyncInfoObj.get('rsDate')


        # 年最高涨幅榜 WebService 测试接口Query_NZGZF
        for i in range(1,3):
            response = client.service.Query_NZGZF(Coordinates='021525374658617185',
                                                    Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                  PoolStyle=i
                                                        )
            self.CommStockPoolYearRank = []
            try:
                self.CommStockPoolYearRank.append(json.loads(response))

            except Exception, e:
                logging.error("%s  webservice 接口数据获取失败 %s" %(__file__ ,response))

    def StockPoolYearRankMC(self):
        '''
        mc更新 A_DxtStockPoolYearRankDiary(年最高涨幅榜)表
        '''

        for self.CommStockPoolYearRankLog in self.CommStockPoolYearRank:
            maxKeyId = int(self.AnalogSyncInfoObj.get('mainKeyId'))

            if self.CommStockPoolYearRankLog["Code"] == 0:
                try:
                    self.DataObj =  json.loads(self.CommStockPoolYearRankLog["DataObj"])#
                except Exception, e:
                    logging.error("%s  webservice 接口DataObj数据获取失败 %s" % (__file__, self.CommStockPoolYearRankLog["DataObj"]))

                map(self.DealData,self.DataObj)

            else:
                 logging.warning("提交股票池股票数据返回失败：%s" %self.CommStockPoolYearRankLog)

    def DealData(self,DataObjArr):

        #判断最后一条
        if DataObjArr==self.DataObj[-1]:
            self.maxKeyId = int(DataObjArr['rsMainkeyID'])
            self.AccessDateTime = DataObjArr['AccessDateTime']
            self.AnalogSyncInfoObj.set('mainKeyId', self.maxKeyId)
            self.AnalogSyncInfoObj.set('AccessDateTime', self.AccessDateTime)
            self.AnalogSyncInfoObj.save()
        #打印
        print ("maxKeyId:", self.maxKeyId, "===", "rsMainKeyID:", DataObjArr['rsMainkeyID'], "===",
               "AccessDateTime:", DataObjArr['AccessDateTime'])

        A_DxtStockPoolYearRankQuery = leancloud.Query('A_DxtStockPoolYearRank')
        A_DxtStockPoolYearRankQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
        self.A_DxtStockPoolYearRankList = A_DxtStockPoolYearRankQuery.find()
        # 编辑
        if len(self.A_DxtStockPoolYearRankList) > 0:

            self.Edit(DataObjArr)
        else:
            self.Add(DataObjArr)


    def Edit(self,DataObjArr):

        self.A_DxtStockPoolYearRankList[0].set('stockPoolObjectId', str(DataObjArr['StockPoolYearRankID']))
        self.A_DxtStockPoolYearRankList[0].set('stockCode', DataObjArr['StockCode'])
        self.A_DxtStockPoolYearRankList[0].set('stockName', DataObjArr['StockShortName'])
        self.A_DxtStockPoolYearRankList[0].set('marketCode', DataObjArr['MarketCode'])  ########

        self.A_DxtStockPoolYearRankList[0].set('cqPrice', DataObjArr['CQPrice'])
        self.A_DxtStockPoolYearRankList[0].set('dqsy', DataObjArr['Dqsy'])
        self.A_DxtStockPoolYearRankList[0].set('inPrice', DataObjArr['AccessPrice'])

        self.A_DxtStockPoolYearRankList[0].set('stockComeFrom', DataObjArr['StockComeFrom'])
        self.A_DxtStockPoolYearRankList[0].set('inTime', DataObjArr['AccessDateTime'])

        self.A_DxtStockPoolYearRankList[0].set('relationId', str(DataObjArr["rsMainkeyID"]))
        self.A_DxtStockPoolYearRankList[0].save()

    def Add(self,DataObjArr):

        A_DxtStockPoolYearRankDiary = leancloud.Object.extend('A_DxtStockPoolYearRank')
        A_DxtStockPoolYearRankDiaryObj = A_DxtStockPoolYearRankDiary()

        A_DxtStockPoolYearRankDiaryObj.set('stockPoolObjectId', str(DataObjArr['StockPoolYearRankID']))
        A_DxtStockPoolYearRankDiaryObj.set('stockCode', DataObjArr['StockCode'])
        A_DxtStockPoolYearRankDiaryObj.set('stockName', DataObjArr['StockShortName'])
        A_DxtStockPoolYearRankDiaryObj.set('marketCode', DataObjArr['MarketCode'])  ########

        A_DxtStockPoolYearRankDiaryObj.set('cqPrice', DataObjArr['CQPrice'])
        A_DxtStockPoolYearRankDiaryObj.set('dqsy', DataObjArr['Dqsy'])
        A_DxtStockPoolYearRankDiaryObj.set('inPrice', DataObjArr['AccessPrice'])

        A_DxtStockPoolYearRankDiaryObj.set('stockComeFrom', DataObjArr['StockComeFrom'])
        A_DxtStockPoolYearRankDiaryObj.set('inTime', DataObjArr['AccessDateTime'])

        A_DxtStockPoolYearRankDiaryObj.set('relationId', str(DataObjArr["rsMainkeyID"]))
        A_DxtStockPoolYearRankDiaryObj.save()

if __name__ == "__main__":

	StockPoolYearRank_object = StockPoolYearRank()

	StockPoolYearRank_object.StockPoolYearRankPort()
	StockPoolYearRank_object.StockPoolYearRankMC()

