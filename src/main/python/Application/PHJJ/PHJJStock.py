#encoding=utf-8

'''
Modified on July 7, 2017

@author: tangr
'''

 #盘后掘金持仓列表

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

class PHJJStock:
        
    def PHJJStockPort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        # 盘后掘金持仓列表 WebService 测试接口 Query_phjj
        response = client.service.Query_phjj(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                            
                                                    )
        try:
            self.PHJJStock = json.loads(response)

        except Exception, e:
            logging.error("%s : webservice get data fail! data:%s" %(__file__ ,response))

    def PHJJStockMC(self):
        '''
        mc更新 A_DxtPHJJStock(盘后掘金持仓列表)表
        '''

        if self.PHJJStock["Code"] == 0:

            self.DataObj =  json.loads(self.PHJJStock["DataObj"])

            # 先删除原有数据
            queryPHJJStock = leancloud.Query('A_DxtPHJJStock')
            query_list = queryPHJJStock.find()
            leancloud.Object.destroy_all(query_list)

            #获取老数据
            # A_DxtPHJJStockQuery = leancloud.Query('A_DxtPHJJStock')
            # self.A_DxtPHJJStockOldList = A_DxtPHJJStockQuery.find()

            #存储所有 新数据
            map(self.DealData,self.DataObj)

            #删除数据
            #
            # if len(self.A_DxtPHJJStockOldList) !=0:
            #     for OldData in self.A_DxtPHJJStockOldList:
            #         relationId = OldData.get("relationId")
            #         isDelate =1
            #         for NewData in self.DataObj:
            #             if relationId in NewData.values():
            #                 isDelate = 0
            #         if  isDelate ==1:
            #             OldData.destroy()

        else:
             logging.warning("not data or data error：%s" %self.PHJJStock)



    def DealData(self,DataObjArr):

        # A_DxtPHJJStockQuery = leancloud.Query('A_DxtPHJJStock')
        # A_DxtPHJJStockQuery.equal_to('relationId', DataObjArr['rsmainkeyid'])
        # self.A_DxtPHJJStockNewList = A_DxtPHJJStockQuery.find()
        #
        # # 编辑
        # if len(self.A_DxtPHJJStockNewList) > 0:
        #
        #     self.Save(self.A_DxtPHJJStockNewList[0],DataObjArr)
        # else:
        #     A_DxtPHJJStock = leancloud.Object.extend('A_DxtPHJJStock')
        #     A_DxtPHJJStockObj = A_DxtPHJJStock()
        #     self.Save(A_DxtPHJJStockObj,DataObjArr)


        A_DxtPHJJStock = leancloud.Object.extend('A_DxtPHJJStock')
        A_DxtPHJJStockObj = A_DxtPHJJStock()
        self.Save(A_DxtPHJJStockObj,DataObjArr)

    def Save(self,Obj,DataObjArr):

        self.Calculate(DataObjArr)
        Obj.set('currentPrice',self.currentPrice)
        Obj.set('profitorLoss', self.profitorLoss)
        Obj.set('profitLossThan',self.profitLossThan)
        Obj.set('sz', self.sz)

        Obj.set('groupBmId', DataObjArr['Vgroupid'])
        Obj.set('stockCode', DataObjArr["stockcode"])
        Obj.set('stockName', DataObjArr['stockshortname'])
        Obj.set('marketCode', DataObjArr['marketcode'])
        Obj.set('marketName', DataObjArr["marketName"])

        Obj.set('currentVolume',DataObjArr["currentVolume"] )
        Obj.set('usevolume', DataObjArr["usevolume"])

        Obj.set('buyMonney', DataObjArr['buymonney'])
        Obj.set('cost', DataObjArr["Cost"])
        Obj.set('price', self.price)
        Obj.set('stockId',  DataObjArr["gpid"])

        Obj.set('firstBuyDate', self.firstBuyDate)

        Obj.set('relationId', DataObjArr['rsmainkeyid'])
        Obj.save()

    def Calculate(self,DataObjArr):
        #时间
        self.firstBuyDate = datetime.strptime(DataObjArr['firstbuydate'], "%Y-%m-%d")
        #单个成本
        self.price = DataObjArr["Cost"]/DataObjArr["currentVolume"]

        #当前价
        if MarketData.getTicker(DataObjArr["marketcode"]+DataObjArr['stockcode']).ZuiXinJia:
            self.currentPrice = MarketData.getTicker(DataObjArr["marketcode"]+DataObjArr['stockcode']).ZuiXinJia/10000
        else:
            self.currentPrice = MarketData.getTicker(DataObjArr["marketcode"]+DataObjArr['stockcode']).ZuoShou/10000

        #盈亏 = （当前价 - 成本价）*持有数量
        self.profitorLoss = (self.currentPrice - self.price) * DataObjArr["currentVolume"]

        #盈亏比例 = 当前价 / 成本价 - 1
        self.profitLossThan = self.currentPrice/self.price -1


        #证券市值 = 当前价 * 持有数量
        self.sz = self.currentPrice * DataObjArr["currentVolume"]

if __name__ == "__main__":

	PHJJStock_object = PHJJStock()

	PHJJStock_object.PHJJStockPort()
	PHJJStock_object.PHJJStockMC()

