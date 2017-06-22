#encoding=utf-8

'''
Modified on June 20, 2017

@author: tangr
'''

 #月最高涨幅榜

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

class StockPoolMonthRank:
    def StockPoolMonthRankPort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
        AnalogSyncInfoObj = AnalogSyncInfo()
        querySyncInfo = AnalogSyncInfo.query

        querySyncInfo.equal_to('type', 'StockPoolMonthRank')
        count = querySyncInfo.count()
        if count == 0:
            dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
            AnalogSyncInfoObj.set("type","StockPoolMonthRank")
            AnalogSyncInfoObj.set("mainKeyId",0)
            AnalogSyncInfoObj.set("rsDateTime","1990-01-01")
            AnalogSyncInfoObj.save()

        syncObj = querySyncInfo.first()
        maxKeyId = int(syncObj.get('mainKeyId'))
        rsDateTime = syncObj.get('rsDateTime')
        top = 100

        # 月最高涨幅榜 WebService 测试接口P_Z_CommStockPoolMonthRank
        response = client.service.P_Z_CommStockPoolMonthRank(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                  rsMainkeyID=maxKeyId,
                                                  rsDateTime=rsDateTime,
                                                  top=top
                                                                  )
        self.data = json.loads(response)

    def StockPoolMonthRankMC(self):
        '''
        mc更新 A_DxtStockPoolMonthRank(月最高涨幅榜)表
        '''
        StockPoolMonthRankMC = self.data
        isChange = 0

        AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
        querySyncInfo = AnalogSyncInfo.query
        querySyncInfo.equal_to('type', 'StockPoolMonthRank')
        syncObj = querySyncInfo.first()
        maxKeyId = int(syncObj.get('mainKeyId'))

        if StockPoolMonthRankMC["Code"] == 0:

            DataObj =  json.loads(StockPoolMonthRankMC["DataObj"])#

            for DataObjArr in DataObj:

                # if int(DataObjArr['rsMainkeyID']) > maxKeyId:
                #     isChange = 1
                maxKeyId = int(DataObjArr['rsMainkeyID'])
                rsDateTime = DataObjArr['rsDateTime']

                print ("maxKeyId:",maxKeyId, "===","rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
                     "rsDateTime:",DataObjArr['rsDateTime'])

                try:
                    A_DxtStockPoolMonthRankQuery = leancloud.Query('A_DxtStockPoolMonthRank')
                    A_DxtStockPoolMonthRankQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
                    count = A_DxtStockPoolMonthRankQuery.count()
                    # 编辑
                    if count > 0:
                        A_DxtStockPoolMonthRankObj = A_DxtStockPoolMonthRankQuery.first()

                        A_DxtStockPoolMonthRankObj.set('stockPoolObjectId', DataObjArr['PoolStyle'])
                        A_DxtStockPoolMonthRankObj.set('stockCode', DataObjArr['StockCode'])
                        A_DxtStockPoolMonthRankObj.set('stockName', DataObjArr['StockShortName'])
                        A_DxtStockPoolMonthRankObj.set('marketCode', DataObjArr['MarketCode'])
                        A_DxtStockPoolMonthRankObj.set('cqPrice', DataObjArr['CQPrice'])
                        A_DxtStockPoolMonthRankObj.set('dqsy', DataObjArr['TargetPrice'])

                        A_DxtStockPoolMonthRankObj.set('inPrice', DataObjArr['AccessPrice'])
                        A_DxtStockPoolMonthRankObj.set('stockComeFrom', DataObjArr['StockComeFrom'])
                        A_DxtStockPoolMonthRankObj.set('inTime', DataObjArr['AccessDateTime'])

                        A_DxtStockPoolMonthRankObj.set('relationId',  DataObjArr["rsMainkeyID"])
                        A_DxtStockPoolMonthRankObj.save()
                    # 新增
                    else:


                except Exception, e:
                    logging.error("股票池月最高涨幅榜数据更新失败: %s" % DataObjArr)

            # if isChange == 1:
            syncObj.set('mainKeyId', maxKeyId)
            syncObj.set('rsDateTime', rsDateTime)
            syncObj.save()

        else:
             logging.warning("股票池提交月最高涨幅榜数据返回失败：%s" %StockPoolMonthRankMC)

if __name__ == "__main__":

	StockPoolMonthRank_object = StockPoolMonthRank()

	StockPoolMonthRank_object.StockPoolMonthRankPort()
	StockPoolMonthRank_object.StockPoolMonthRankMC()

