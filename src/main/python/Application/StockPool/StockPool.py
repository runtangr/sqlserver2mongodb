#encoding=utf-8

'''
Modified on June 19, 2017

@author: tangr
'''

 #股票池

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

        querySyncInfo.equal_to('type', 'StockPool')
        count = querySyncInfo.count()
        if count == 0:
            dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
            SyncControlObj.set("type","StockPool")
            SyncControlObj.set("mainKeyId",0)
            SyncControlObj.set("rsDateTime","1990-01-01")
            SyncControlObj.save()

        syncObj = querySyncInfo.first()
        maxKeyId = int(syncObj.get('mainKeyId'))
        rsDateTime = syncObj.get('rsDateTime')
        top = 100

        # 股票池 WebService 测试接口P_Z_CommStockZB
        response = client.service.P_Z_CommStockZB(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                  rsMainkeyID=maxKeyId,
                                                  rsDateTime=rsDateTime,
                                                  top=top
                                                                  )
        try:
            self.CommStockZB = json.loads(response)

        except Exception, e:
            logging.error("%s  webservice 接口数据获取失败 %s" % (__file__, response))
       

    def StockPoolMC(self):
        '''
        mc更新A_DxtStockPool(股票池)表
        '''
        StockPoolMC = self.CommStockZB
        isChange = 0

        SyncControl = leancloud.Object.extend('SyncControl')
        querySyncInfo = SyncControl.query
        querySyncInfo.equal_to('type', 'StockPool')
        syncObj = querySyncInfo.first()
        maxKeyId = int(syncObj.get('mainKeyId'))

        if StockPoolMC["Code"] == 0:

            DataObj =  json.loads(StockPoolMC["DataObj"])#

            for DataObjArr in DataObj:

                if int(DataObjArr['rsMainkeyID']) > maxKeyId:
                    isChange = 1
                    maxKeyId = int(DataObjArr['rsMainkeyID'])
                    rsDateTime = DataObjArr['rsDateTime']

                print ("maxKeyId:",maxKeyId, "===","rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
                     "rsDateTime:",DataObjArr['rsDateTime'])

                stockCLFKYL =""
                stockCLFKZS =""
                if len(DataObjArr['StockCLFK'])!=0:
                    StockCLFK = DataObjArr['StockCLFK'].split(',')
                    stockCLFKYL = StockCLFK[0]
                    stockCLFKZS= StockCLFK[1]

                isDisable = 0 if DataObjArr['rsProjectId']==0 else 1


                StockCLFGList = DataObjArr['StockCLFG'].split(',')

                try:

                    A_DxtStockPoolQuery = leancloud.Query('A_DxtStockPool')
                    A_DxtStockPoolQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
                    count = A_DxtStockPoolQuery.count()
                    #编辑
                    if count>0:
                        A_DxtStockPoolObj = A_DxtStockPoolQuery.first()
                        A_DxtStockPoolObj.set('name', DataObjArr['StockZBName'])
                        A_DxtStockPoolObj.set('stockCLFG', StockCLFGList)
                        A_DxtStockPoolObj.set('stockCLFKYL', stockCLFKYL)
                        A_DxtStockPoolObj.set('stockCLFKZS', stockCLFKZS)
                        A_DxtStockPoolObj.set('stockType', DataObjArr['StockType'])
                        A_DxtStockPoolObj.set('stockTP', DataObjArr["StockTP"])
                        A_DxtStockPoolObj.set('stockPJSY', DataObjArr['StockPJSY'])
                        A_DxtStockPoolObj.set('stockZGZF', DataObjArr['StockPJSY'])
                        A_DxtStockPoolObj.set('stockXGMX', DataObjArr['StockSGMX'])

                        #add
                        A_DxtStockPoolObj.set('isDisable', isDisable)

                        A_DxtStockPoolObj.set('relationId', str(DataObjArr["rsMainkeyID"]))
                        A_DxtStockPoolObj.save()

                    #新增
                    else:

                        A_DxtStockPool = leancloud.Object.extend('A_DxtStockPool')
                        A_DxtStockPoolObj = A_DxtStockPool()

                        A_DxtStockPoolObj.set('name', DataObjArr['StockZBName'])
                        A_DxtStockPoolObj.set('stockCLFG', StockCLFGList)
                        A_DxtStockPoolObj.set('stockCLFKYL', stockCLFKYL)
                        A_DxtStockPoolObj.set('stockCLFKZS', stockCLFKZS)
                        A_DxtStockPoolObj.set('stockType', DataObjArr['StockType'])
                        A_DxtStockPoolObj.set('stockTP', DataObjArr["StockTP"])
                        A_DxtStockPoolObj.set('stockPJSY', DataObjArr['StockPJSY'])
                        A_DxtStockPoolObj.set('stockZGZF', DataObjArr['StockPJSY'])
                        A_DxtStockPoolObj.set('stockXGMX', DataObjArr['StockSGMX'])

                        # add
                        A_DxtStockPoolObj.set('isDisable', isDisable)

                        A_DxtStockPoolObj.set('relationId',  str(DataObjArr["rsMainkeyID"]))
                        A_DxtStockPoolObj.save()

                except Exception, e:
                    logging.error("股票池数据更新失败: %s" % DataObjArr)

            if isChange == 1:
                syncObj.set('mainKeyId', maxKeyId)
                syncObj.set('rsDateTime', rsDateTime)
                syncObj.save()

        else:
             logging.warning("提交股票池数据返回失败：%s" %StockPoolMC)

if __name__ == "__main__":

	StockPool_object = StockPool()

	StockPool_object.StockPoolPort()
	StockPool_object.StockPoolMC()

