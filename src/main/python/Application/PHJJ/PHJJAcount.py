#encoding=utf-8

'''
Modified on July 7, 2017

@author: tangr
'''

 #资金账户

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

class PHJJAcount:
        
    def PHJJAcountPort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        # 资金账户 WebService 测试接口 Query_ZHXX
        response = client.service.Query_ZHXX(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                             Userid=0
                                                    )
        try:
            self.PHJJAcount = json.loads(response)

        except Exception, e:
            logging.error("%s : webservice get data fail! data:%s" %(__file__ ,response))

    def PHJJAcountMC(self):
        '''
        mc更新 A_DxtPHJJAcount(资金账户)表
        '''

        if self.PHJJAcount["Code"] == 0:

            self.DataObj =  json.loads(self.PHJJAcount["DataObj"])  

            #存储所有 新数据
            map(self.DealData,self.DataObj)

        else:
             logging.warning("not data or data error：%s" %self.PHJJAcount)



    def DealData(self,DataObjArr):

        A_DxtPHJJAcountQuery = leancloud.Query('A_DxtPHJJAcount')
        A_DxtPHJJAcountQuery.equal_to('relationId', DataObjArr['rsMainkeyID'])
        self.A_DxtPHJJAcountList = A_DxtPHJJAcountQuery.find()

        # 编辑
        if len(self.A_DxtPHJJAcountList) > 0:

            self.Save(self.A_DxtPHJJAcountList[0], DataObjArr)
        else:
            A_DxtPHJJAcount = leancloud.Object.extend('A_DxtPHJJAcount')
            A_DxtPHJJAcountObj = A_DxtPHJJAcount()
            self.Save(A_DxtPHJJAcountObj, DataObjArr)

    def Save(self,Obj,DataObjArr):

        self.Calculate(DataObjArr)
        Obj.set('totalCapital',self.totalCapital)
        Obj.set('sz',self.total_sz )
        Obj.set('cw', self.cw)
        # Obj.set('originalCapital',0)

        Obj.set('residualCapital',DataObjArr["ResidualCapital"] )
        Obj.set('frozenCapital', DataObjArr["FrozenCapital"])
        Obj.set('OriginalCapital', DataObjArr["OriginalCapital"])


        Obj.set('syl', self.syl)

        Obj.set('relationId', DataObjArr['rsMainkeyID'])
        Obj.save()

    def Calculate(self,DataObjArr):
        A_DxtPHJJStockQuery = leancloud.Query('A_DxtPHJJStock')
        A_DxtPHJJStockList = A_DxtPHJJStockQuery.find()

        #总市值计算
        self.total_sz = 0
        if len(A_DxtPHJJStockList) !=0:
            for PHJJStockData in A_DxtPHJJStockList:
                self.total_sz += PHJJStockData.get("sz")
        #总资产计算
        self.totalCapital = self.total_sz + DataObjArr["ResidualCapital"] + DataObjArr["FrozenCapital"]

        # #收益率 = 总市值/本期起始资金 -1  错误
        # 收益率 = （总资产-本期起始资金） / 本期起始资金
        self.syl =  (self.totalCapital - DataObjArr["OriginalCapital"])/DataObjArr["OriginalCapital"]

        #仓位=总市值/总资产
        self.cw = self.total_sz/self.totalCapital



if __name__ == "__main__":

	PHJJAcount_object = PHJJAcount()

	PHJJAcount_object.PHJJAcountPort()
	PHJJAcount_object.PHJJAcountMC()

