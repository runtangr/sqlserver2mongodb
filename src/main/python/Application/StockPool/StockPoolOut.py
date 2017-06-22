#encoding=utf-8

'''
Modified on June 20, 2017

@author: tangr
'''

 #股票池最近出池

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

class StockPoolOut:
    def StockPoolOutPort(self):
        '''
        获取端口数据
        '''
        url = "http://125.70.0.228:9525/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        self.CommStockPoolOut = []

        # 股票池最近出池 WebService 测试接口 Query_ZJCC
        for StockPoolNumber in range(1,4):
            response = client.service.Query_ZJCC(Coordinates='021525374658617185',
                                                    Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                  PoolStyle=StockPoolNumber
                                                        )

            try:
                self.CommStockPoolOut.append(json.loads(response))

            except Exception, e:
                logging.error("%s  webservice 接口数据获取失败 %s" %(__file__ ,response))

    def StockPoolOutMC(self):
        '''
        mc更新 A_DxtStockPoolOutDiary(年最高涨幅榜)表
        '''

        for self.CommStockPoolOutLog in self.CommStockPoolOut:


            if self.CommStockPoolOutLog["Code"] == 0:
                try:
                    self.DataObj =  json.loads(self.CommStockPoolOutLog["DataObj"])#
                except Exception, e:
                    logging.error("%s  webservice 接口DataObj数据获取失败 %s" % (__file__, self.CommStockPoolOutLog["DataObj"]))

                self.SelectStockPool =0

                map(self.DealData,self.DataObj)

            else:
                 logging.warning("提交股票池股票池最近出池数据返回失败：%s" %self.CommStockPoolOutLog)

    def DealData(self,DataObjArr):

        A_DxtStockPoolOutQuery = leancloud.Query('A_DxtStockPoolOut')
        A_DxtStockPoolOutQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
        self.A_DxtStockPoolOutList = A_DxtStockPoolOutQuery.find()

        # 判断股票池
        self.SelectStockPool += 1

        # 查找StockPool 匹配relationId ，取出objectid
        A_DxtStockPoolQuery = leancloud.Query('A_DxtStockPool')
        A_DxtStockPoolQuery.equal_to('relationId', str(self.SelectStockPool))
        self.A_DxtStockPoolList = A_DxtStockPoolQuery.find()

        #转换
        self.AccessDateTime = datetime.strptime(DataObjArr['AccessDateTime'], "%Y-%m-%d %H:%M:%S")
        self.OutDateTime = datetime.strptime(DataObjArr['OutDateTime'], "%Y-%m-%d %H:%M:%S")

        # 编辑
        if len(self.A_DxtStockPoolOutList) > 0:

            self.Edit(DataObjArr)
        else:
            self.Add(DataObjArr)

    # | stockPoolObjectId | string | 股票池ID | 无 |
    # | stockCode | string | 股票代码 | 无 |
    # | stockName | string | 股票名称 | 无 |
    # | marketCode | string | 市场代码 | 无 |
    # | cqPrice | number | 除权价格 | 无 |
    # | outPrice | number | 入池价格 | 无 |
    # | dqsy | number | 区间最高收益 | 无 |
    # | inPrice | number | 入池价格 | 无 |
    # | stockComeFrom | string | 推荐机构 | 无 |
    # | inDateTime | datetime | 发布时间，对应websercie的AccessDateTime | 无 |
    # | outDateTime | datetime | 发布时间，对应websercie的OutDateTime | 无 |
    # | stockId | number | 股票ID | 无 |
    # | relationId | string | 同步系统关联ID | 无 |
    #
    # 输出列：StockCode股票代码, StockShortName股票名称,
    # AccessDateTime入池时间, AccessPrice入池价,
    # OutDateTime出池时间, OutPrice出池价, Dqsy区间最高收益,
    # rsMainkeyID记录ID, CQPrice除权价, StockComeFrom推荐机构

    def Edit(self,DataObjArr):

        self.A_DxtStockPoolOutList[0].set('stockPoolObjectId', self.A_DxtStockPoolList[0].get('objectId'))
        self.A_DxtStockPoolOutList[0].set('stockCode', DataObjArr['StockCode'])
        self.A_DxtStockPoolOutList[0].set('stockName', DataObjArr['StockShortName'])
        self.A_DxtStockPoolOutList[0].set('marketCode', DataObjArr['MarketCode'])

        self.A_DxtStockPoolOutList[0].set('cqPrice', DataObjArr['CQPrice'])
        self.A_DxtStockPoolOutList[0].set('dqsy', DataObjArr['Dqsy'])
        self.A_DxtStockPoolOutList[0].set('inPrice', DataObjArr['AccessPrice'])

        self.A_DxtStockPoolOutList[0].set('stockComeFrom', DataObjArr['StockComeFrom'])
        self.A_DxtStockPoolOutList[0].set('inDateTime', self.AccessDateTime)
        self.A_DxtStockPoolOutList[0].set('outDateTime', self.OutDateTime)
        self.A_DxtStockPoolOutList[0].set('stockId', DataObjArr['StockId'])
        self.A_DxtStockPoolOutList[0].set('relationId', str(DataObjArr["rsMainkeyID"]))
        self.A_DxtStockPoolOutList[0].save()

    def Add(self,DataObjArr):

        A_DxtStockPoolOutDiary = leancloud.Object.extend('A_DxtStockPoolOut')
        A_DxtStockPoolOutDiaryObj = A_DxtStockPoolOutDiary()

        A_DxtStockPoolOutDiaryObj.set('stockPoolObjectId', self.A_DxtStockPoolList[0].get('objectId'))
        A_DxtStockPoolOutDiaryObj.set('stockCode', DataObjArr['StockCode'])
        A_DxtStockPoolOutDiaryObj.set('stockName', DataObjArr['StockShortName'])
        A_DxtStockPoolOutDiaryObj.set('marketCode', DataObjArr['MarketCode'])  ########

        A_DxtStockPoolOutDiaryObj.set('cqPrice', DataObjArr['CQPrice'])
        A_DxtStockPoolOutDiaryObj.set('dqsy', DataObjArr['Dqsy'])
        A_DxtStockPoolOutDiaryObj.set('inPrice', DataObjArr['AccessPrice'])

        A_DxtStockPoolOutDiaryObj.set('stockComeFrom', DataObjArr['StockComeFrom'])
        A_DxtStockPoolOutDiaryObj.set('inDateTime', self.AccessDateTime)
        A_DxtStockPoolOutDiaryObj.set('outDateTime', self.OutDateTime)
        A_DxtStockPoolOutDiaryObj.set('stockId', DataObjArr['StockId'])
        A_DxtStockPoolOutDiaryObj.set('relationId', str(DataObjArr["rsMainkeyID"]))
        A_DxtStockPoolOutDiaryObj.save()

if __name__ == "__main__":

	StockPoolOut_object = StockPoolOut()

	StockPoolOut_object.StockPoolOutPort()
	StockPoolOut_object.StockPoolOutMC()

