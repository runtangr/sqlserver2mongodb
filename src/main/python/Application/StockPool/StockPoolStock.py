# encoding=utf-8

'''
Modified on June 20, 2017

@author: tangr
'''

# 股票池股票

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


class StockPool:
    def StockPoolPort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        SyncControl = leancloud.Object.extend('SyncControl')
        SyncControlObj = SyncControl()
        querySyncInfo = SyncControl.query

        querySyncInfo.equal_to('type', 'StockPoolStock')
        count = querySyncInfo.count()
        if count == 0:
            dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
            SyncControlObj.set("type", "StockPoolStock")
            SyncControlObj.set("mainKeyId", 0)
            SyncControlObj.set("rsDateTime", "1990-01-01")
            SyncControlObj.save()

        syncObj = querySyncInfo.first()
        maxKeyId = int(syncObj.get('mainKeyId'))
        rsDateTime = syncObj.get('rsDateTime')
        top = 100

        # 股票池股票 WebService 测试接口P_Z_CommStockPool
        response = client.service.P_Z_CommStockPool(Coordinates='021525374658617185',
                                                    Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                    rsMainkeyID=maxKeyId,
                                                    rsDateTime=rsDateTime,
                                                    top=top
                                                    )
        self.data = json.loads(response)

    def StockPoolMC(self):
        '''
        mc更新 A_DxtStockPoolStock(股票池股票)表
        '''
        StockPoolMC = self.data
        isChange = 0

        SyncControl = leancloud.Object.extend('SyncControl')
        querySyncInfo = SyncControl.query
        querySyncInfo.equal_to('type', 'StockPoolStock')
        syncObj = querySyncInfo.first()
        maxKeyId = int(syncObj.get('mainKeyId'))

        if StockPoolMC["Code"] == 0:

            DataObj = json.loads(StockPoolMC["DataObj"])  #

            # map(self.DealData,DataObj)

            for DataObjArr in DataObj:

                if DataObjArr == DataObj[-1]:
                    #     isChange = 1
                    maxKeyId = int(DataObjArr['rsMainkeyID'])
                    rsDateTime = DataObjArr['rsDateTime']
                    syncObj.set('mainKeyId', maxKeyId)
                    syncObj.set('rsDateTime', rsDateTime)
                    syncObj.save()

                print ("maxKeyId:", maxKeyId, "===", "rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
                       "rsDateTime:", DataObjArr['rsDateTime'])

                inTime = datetime.strptime(DataObjArr['AccessDateTime'], "%Y-%m-%d %H:%M:%S.%f")
                if DataObjArr["OutDateTime"] is None or DataObjArr["OutDateTime"] == "1900-01-01 00:00:00":
                    outTime = datetime(year=1900, month=1, day=1)
                else:
                    outTime = datetime.strptime(DataObjArr["OutDateTime"], "%Y-%m-%d %H:%M:%S.%f")
                try:
                    A_DxtStockPoolStockQuery = leancloud.Query('A_DxtStockPoolStock')
                    A_DxtStockPoolStockQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
                    count = A_DxtStockPoolStockQuery.count()

                    A_DxtStockPoolQuery = leancloud.Query('A_DxtStockPool')
                    A_DxtStockPoolQuery.equal_to('relationId', str(DataObjArr['PoolStyle']))
                    A_DxtStockPoolObj = A_DxtStockPoolQuery.find()
                    # 编辑
                    if count > 0 and len(A_DxtStockPoolObj) > 0:

                        A_DxtStockPoolStockObj = A_DxtStockPoolStockQuery.first()

                        A_DxtStockPoolStockObj.set('stockPoolObjectId', A_DxtStockPoolObj[0].get('objectId'))
                        A_DxtStockPoolStockObj.set('stockCode', DataObjArr['StockCode'])
                        A_DxtStockPoolStockObj.set('stockName', DataObjArr['StockShortName'])
                        A_DxtStockPoolStockObj.set('marketCode', DataObjArr['MarketCode'])
                        A_DxtStockPoolStockObj.set('cqPrice', DataObjArr['CQPrice'])
                        A_DxtStockPoolStockObj.set('targetPrice', DataObjArr['TargetPrice'])
                        A_DxtStockPoolStockObj.set('zsPrice', DataObjArr['ZSPrice'])
                        A_DxtStockPoolStockObj.set('inPrice', DataObjArr['AccessPrice'])
                        A_DxtStockPoolStockObj.set('outPrice', DataObjArr['OutPrice'])

                        A_DxtStockPoolStockObj.set('bestAvail', DataObjArr['Dqsy'])
                        A_DxtStockPoolStockObj.set('stockComeFrom', DataObjArr['StockComeFrom'])
                        A_DxtStockPoolStockObj.set('stockId', DataObjArr['StockId'])
                        A_DxtStockPoolStockObj.set('inTime', inTime)
                        A_DxtStockPoolStockObj.set('outTime', outTime)

                        # add
                        A_DxtStockPoolStockObj.set('rsStatus', DataObjArr['rsStatus'])
                        A_DxtStockPoolStockObj.set('relationId', str(DataObjArr["rsMainkeyID"]))

                        A_DxtStockPoolStockObj.set('suggestion', DataObjArr['dqjy'])
                        A_DxtStockPoolStockObj.set('willBuy', DataObjArr['mrsj'])
                        A_DxtStockPoolStockObj.set('willSale', DataObjArr['mcsj'])

                        A_DxtStockPoolStockObj.save()
                    # 新增
                    elif len(A_DxtStockPoolObj) > 0:
                        A_DxtStockPoolStock = leancloud.Object.extend('A_DxtStockPoolStock')
                        A_DxtStockPoolStockObj = A_DxtStockPoolStock()

                        A_DxtStockPoolStockObj.set('stockPoolObjectId', A_DxtStockPoolObj[0].get('objectId'))
                        A_DxtStockPoolStockObj.set('stockCode', DataObjArr['StockCode'])
                        A_DxtStockPoolStockObj.set('stockName', DataObjArr['StockShortName'])
                        A_DxtStockPoolStockObj.set('marketCode', DataObjArr['MarketCode'])
                        A_DxtStockPoolStockObj.set('cqPrice', DataObjArr['CQPrice'])
                        A_DxtStockPoolStockObj.set('targetPrice', DataObjArr['TargetPrice'])
                        A_DxtStockPoolStockObj.set('zsPrice', DataObjArr['ZSPrice'])
                        A_DxtStockPoolStockObj.set('inPrice', DataObjArr['AccessPrice'])
                        A_DxtStockPoolStockObj.set('outPrice', DataObjArr['OutPrice'])

                        A_DxtStockPoolStockObj.set('bestAvail', DataObjArr['Dqsy'])
                        A_DxtStockPoolStockObj.set('stockComeFrom', DataObjArr['StockComeFrom'])
                        A_DxtStockPoolStockObj.set('stockId', DataObjArr['StockId'])
                        A_DxtStockPoolStockObj.set('inTime', inTime)
                        A_DxtStockPoolStockObj.set('outTime', outTime)

                        # add
                        A_DxtStockPoolStockObj.set('rsStatus', DataObjArr['rsStatus'])
                        A_DxtStockPoolStockObj.set('relationId', str(DataObjArr["rsMainkeyID"]))

                        A_DxtStockPoolStockObj.set('suggestion', DataObjArr['dqjy'])
                        A_DxtStockPoolStockObj.set('willBuy', DataObjArr['mrsj'])
                        A_DxtStockPoolStockObj.set('willSale', DataObjArr['mcsj'])

                        A_DxtStockPoolStockObj.save()

                except Exception, e:
                    logging.error("股票池股票数据更新失败: %s" % DataObjArr)

                    # if isChange == 1:


        else:
            logging.warning("提交股票池股票数据返回失败：%s" % StockPoolMC)

    def DealData(self, DataObjArr):

        A_DxtStockPoolStockQuery = leancloud.Query('A_DxtStockPoolStock')
        A_DxtStockPoolStockQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
        count = A_DxtStockPoolStockQuery.count()
        # 编辑
        if count > 0:
            self.Edit(DataObjArr)
        else:
            self.Add(DataObjArr)

    def Edit(self, DataObjArr):

        pass

    def Add(self, DataObjArr):
        pass


if __name__ == "__main__":
    StockPool_object = StockPool()

    StockPool_object.StockPoolPort()
    StockPool_object.StockPoolMC()
