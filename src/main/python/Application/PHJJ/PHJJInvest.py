#encoding=utf-8

'''
Modified on July 7, 2017

@author: tangr
'''

 #盘后掘金投资记录

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

class PHJJInvest:

    def CreateSyncInfo(self):
        AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
        self.AnalogSyncInfoObj = AnalogSyncInfo()
        querySyncInfo = AnalogSyncInfo.query

        querySyncInfo.equal_to('type', 'PHJJInvest')
        syncObj = querySyncInfo.find()
        if len(syncObj) == 0:
            self.AnalogSyncInfoObj.set("type", "PHJJInvest")
            self.AnalogSyncInfoObj.set("mainKeyId", 0)
            self.AnalogSyncInfoObj.set("rsDateTime", "1990-01-01")
            self.AnalogSyncInfoObj.save()

        self.AnalogSyncInfoObj = querySyncInfo.first()
        self.maxKeyId = int(self.AnalogSyncInfoObj.get('mainKeyId'))
        self.rsDateTime = self.AnalogSyncInfoObj.get('rsDateTime')

    def PHJJInvestPort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)
        self.CreateSyncInfo()
        # 盘后掘金投资记录 WebService 测试接口 Query_uimsVSTSCD_phjj
        response = client.service.Query_uimsVSTSCD_phjj(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                        VGroupid=3,
                                                        ksrq=self.rsDateTime,
                                                        jsrq='9999-12-31'
                                                    )
        try:
            self.PHJJInvest = json.loads(response)

        except Exception, e:
            logging.error("%s : webservice get data fail! data:%s" %(__file__ ,response))

    def PHJJInvestMC(self):
        '''
        mc更新 A_DxtPHJJInvest(盘后掘金投资记录)表
        '''

        if self.PHJJInvest["Code"] == 0:

            self.DataObj =  json.loads(self.PHJJInvest["DataObj"])  

            #存储所有 新数据
            map(self.DealData,self.DataObj)

        else:
             logging.warning("not data or data error：%s" %self.PHJJInvest)



    def DealData(self,DataObjArr):

        # 最后一条数据赋值
        if DataObjArr == self.DataObj[0]:
            self.maxKeyId = int(DataObjArr['rsmainkeyid'])
            self.rsDateTime = DataObjArr['rsdatetime']
            self.AnalogSyncInfoObj.set('mainKeyId', self.maxKeyId)
            self.AnalogSyncInfoObj.set('rsDateTime', self.rsDateTime)
            self.AnalogSyncInfoObj.save()

        # 打印
        print ("maxKeyId:", self.maxKeyId, "===", "rsMainKeyId:", DataObjArr['rsmainkeyid'], "===",
               "rsDateTime:", DataObjArr['rsdatetime'])

        A_DxtPHJJInvestQuery = leancloud.Query('A_DxtPHJJInvest')
        A_DxtPHJJInvestQuery.equal_to('relationId', DataObjArr['rsmainkeyid'])
        self.A_DxtPHJJInvestList = A_DxtPHJJInvestQuery.find()

        # 编辑
        if len(self.A_DxtPHJJInvestList) > 0:

            self.Save(self.A_DxtPHJJInvestList[0], DataObjArr)
        else:
            A_DxtPHJJInvest = leancloud.Object.extend('A_DxtPHJJInvest')
            A_DxtPHJJInvestObj = A_DxtPHJJInvest()
            self.Save(A_DxtPHJJInvestObj, DataObjArr)

    def Save(self,Obj,DataObjArr):
        self.Calculate(DataObjArr)
        # Obj.set('groupBmId',)
        Obj.set('stockCode',DataObjArr["stockcode"])
        Obj.set('stockName', DataObjArr["stockshortName"])
        Obj.set('marketCode',DataObjArr["MarketCode"])
        Obj.set('cjje',DataObjArr["je"] )
        Obj.set('price', DataObjArr["price"])
        Obj.set('syl', self.syl)

        Obj.set('volume', DataObjArr["volume"])
        Obj.set('profitorLoss', DataObjArr["ProfitorLoss"])
        Obj.set('transType', self.TransStyle)
        # Obj.set('wtTime', 0)
        Obj.set('dealTime', self.rsdatetime)

        Obj.set('relationId', DataObjArr['rsmainkeyid'])
        Obj.save()

    def Calculate(self,DataObjArr):

        style = {
            -1: "卖",
            1: "买",
            20: "分红",
            30: "送股"
        }
        # 买卖
        self.TransStyle = style[DataObjArr["TransStyle"]]

        #收益率计算
        self.syl = 0
        #卖 收益率 =  本次盈亏 /（成交金额 - 本次盈亏）
        if DataObjArr["TransStyle"] ==-1:
            self.syl = DataObjArr["ProfitorLoss"]/(DataObjArr["je"] - DataObjArr["ProfitorLoss"])

        #时间转换
        self.rsdatetime = datetime.strptime(DataObjArr["rsdatetime"], "%Y-%m-%d")


if __name__ == "__main__":

	PHJJInvest_object = PHJJInvest()

	PHJJInvest_object.PHJJInvestPort()
	PHJJInvest_object.PHJJInvestMC()

