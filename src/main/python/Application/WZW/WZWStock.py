# encoding=utf-8

'''
Modified on June 27, 2017

@author: tangr
'''

# 王中王持仓列表
import os
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

logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s.%(funcName)s Line:%(lineno)d %(message)s',
                    level=os.getenv("LOG_LEVEL", 'INFO'))

init_leancloud_client()


class WZWStock:
    def WZWStockPort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        SyncControl = leancloud.Object.extend('SyncControl')
        self.SyncControlObj = SyncControl()
        querySyncInfo = SyncControl.query

        querySyncInfo.equal_to('type', 'WZWStock')
        syncObj = querySyncInfo.find()
        if len(syncObj) == 0:
            dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
            self.SyncControlObj.set("type", "WZWStock")
            self.SyncControlObj.set("mainKeyId", 0)
            self.SyncControlObj.set("rsDateTime", "1990-01-01")
            self.SyncControlObj.save()

        self.SyncControlObj = querySyncInfo.first()
        self.maxKeyId = int(self.SyncControlObj.get('mainKeyId'))
        self.rsDateTime = self.SyncControlObj.get('rsDateTime')
        top = 200

        # 王中王持仓列表 WebService 测试接口P_Z_uimsVSTSC_pro
        response = client.service.P_Z_uimsVSTSC_pro(Coordinates='021525374658617185',
                                                    Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                    rsMainkeyID=self.maxKeyId,
                                                    rsDateTime="2017-08-01 00:00:00",
                                                    top=top
                                                    )
        try:
            self.WZWStock = json.loads(response)

        except Exception, e:
            logging.error("%s  webservice 接口数据获取失败 %s" % (__file__, response))

    def WZWStockMC(self):
        '''
        mc更新 A_DxtWZWStock(王中王持仓列表)表
        '''

        maxKeyId = int(self.SyncControlObj.get('mainKeyId'))

        if self.WZWStock["Code"] == 0:

            self.DataObj = json.loads(self.WZWStock["DataObj"])  #

            map(self.DealData, self.DataObj)


        else:
            logging.warning("提交王中王持仓列表数据返回失败：%s" % self.WZWStock)

    def DealData(self, DataObjArr):
        # logging.warning("1")
        # 最后一条数据赋值
        if DataObjArr == self.DataObj[-1]:
            self.maxKeyId = int(DataObjArr['rsmainkeyid'])
            self.rsDateTime = DataObjArr['rsDateTime']
            self.SyncControlObj.set('mainKeyId', self.maxKeyId)
            self.SyncControlObj.set('rsDateTime', self.rsDateTime)
            self.SyncControlObj.save()

        # 打印
        print ("maxKeyId:", self.maxKeyId, "===", "rsMainkeyID:", DataObjArr['rsmainkeyid'], "===",
               "rsDateTime:", DataObjArr['rsDateTime'])

        # 数据处理
        # 时间格式
        self.firstBuyDate = datetime.strptime(DataObjArr['FirstBuyDate'], '%Y-%m-%d %H:%M:%S')
        # totalCapital = DataObjArr["ResidualCapital"] + DataObjArr["ResidualCapital"]
        # logging.warning("2")
        if DataObjArr["currentVolume"] > 0:
            # 持仓市价  持仓市值 = 行情接口获取当前价 * 当前持仓股数
            market_data = MarketData.getTicker(DataObjArr["marketcode"] + DataObjArr['stockcode'])
            if market_data.ZuiXinJia:
                current = market_data.ZuiXinJia / 10000.00
            else:
                current = market_data.ZuoShou / 10000.00
        else:
            current = 0
        # logging.warning("3")
        self.position_sz = current * DataObjArr["currentVolume"]

        A_DxtWZWStockStockQuery = leancloud.Query('A_DxtWZWStock')
        A_DxtWZWStockStockQuery.equal_to('relationId', DataObjArr['rsmainkeyid'])
        self.A_DxtWZWStockStockList = A_DxtWZWStockStockQuery.find()

        # 查找A_DxtWZWTeacher VGroupID，取出teacherObjectId
        A_DxtWZWTeacherQuery = leancloud.Query('A_DxtWZWTeacher')
        A_DxtWZWTeacherQuery.equal_to('groupBmId', int(DataObjArr["VGroupid"]))
        self.A_DxtWZWTeacherList = A_DxtWZWTeacherQuery.find()
        # 编辑  王中王老师有 才会有持仓
        # logging.warning("4")
        if len(self.A_DxtWZWStockStockList) > 0 and len(self.A_DxtWZWTeacherList) > 0:

            self.Save(self.A_DxtWZWStockStockList[0], DataObjArr)
        elif len(self.A_DxtWZWTeacherList) > 0:
            A_DxtWZWStock = leancloud.Object.extend('A_DxtWZWStock')
            A_DxtWZWStockObj = A_DxtWZWStock()
            self.Save(A_DxtWZWStockObj, DataObjArr)

            # logging.warning("5")

    def Save(self, Obj, DataObjArr):
        # 如果原持仓数据及即将更新的持仓数据都为0,则不进行处理
        if Obj.get('currentVolume', 0) and DataObjArr["currentVolume"]:
            return
        Obj.set('groupBmId', DataObjArr['VGroupid'])
        Obj.set('teacherObjectId', self.A_DxtWZWTeacherList[0].get("objectId"))
        Obj.set('stockCode', DataObjArr['stockcode'])
        Obj.set('stockName', DataObjArr['stockshortname'])
        Obj.set('marketCode', DataObjArr["marketcode"])
        Obj.set('marketName', DataObjArr["marketName"])

        Obj.set('currentVolume', DataObjArr["currentVolume"])

        Obj.set('usevolume', DataObjArr["usevolume"])
        Obj.set('buyMonney', DataObjArr["BuyMonney"])

        Obj.set('cost', DataObjArr['Cost'])
        Obj.set('price', DataObjArr['cbj'])
        Obj.set('stockId', DataObjArr['gpid'])
        Obj.set('firstBuyDate', self.firstBuyDate)

        Obj.set('relationId', DataObjArr['rsmainkeyid'])

        # if (DataObjArr['rsMainkeyID'] == 34099):
        #     a=1

        # 持仓市价
        Obj.set('total_sz', self.position_sz)
        Obj.save()


if __name__ == "__main__":
    WZWStock_object = WZWStock()

    WZWStock_object.WZWStockPort()
    WZWStock_object.WZWStockMC()
