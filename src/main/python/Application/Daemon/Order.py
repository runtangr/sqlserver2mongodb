#encoding=utf-8

'''
Modified on June 2, 2017

@author: tangr
'''
 #模拟炒股
 #成交数据同步

import unittest
from suds.client import Client
import json
from datetime import datetime
from core import leancloud_patch
import leancloud
from core.Utils import init_leancloud_client

init_leancloud_client()

class Order:
    def OrderPort(self):
        '''
        获取端口数据
        '''
        url = "http://180.169.122.18:8091/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        # 成交明细 WebService 测试接口Query_uimsStockTransDataSetList
        response = client.service.Query_uimsStockTransDataSetList(Coordinates='021525374658617185',
																  Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A'
																  )
        self.data = json.loads(response)

    def OrderMC(self):
		'''
		mc更新AnalogOrder(成交明细)表
		'''
		OrderMC = self.data
		AnalogOrder = leancloud.Object.extend('AnalogOrder')
		OrderObj = AnalogOrder()
		queryOrder = AnalogOrder.query

		AnalogMyMatch = leancloud.Object.extend('AnalogMyMatch')
		queryMyMatch = AnalogMyMatch.query

		if OrderMC["Code"] == 0:

			DataObj =  json.loads(OrderMC["DataObj"])#

			for DataObj_first in DataObj:

				#计算
				cjje = DataObj_first['Volume'] * DataObj_first['Price'] - DataObj_first['Commission'] - DataObj_first['Commission1']
				transType =  "买" if DataObj_first['TransStyle'] == 1 else "卖"
				dateTime = datetime.strptime(DataObj_first["cjdatetime"],"%Y-%m-%d %H:%M:%S")  #转换


				queryOrder.equal_to('mainKeyId',int(DataObj_first["TransRecordId"])) ####注意转换 int
				count = queryOrder.count()


				queryMyMatch.equal_to('groupBmId', DataObj_first['VGroupid'])
				myMatchObj = queryMyMatch.find()

				if count > 0:

					if myMatchObj:
						#编辑
						OrderObj.set('stockCode', DataObj_first['StockCode'])
						OrderObj.set('stockName', DataObj_first['stockname'])
						OrderObj.set('marketCode', DataObj_first['marketcode'])
						OrderObj.set('price', DataObj_first['Price'])
						OrderObj.set('volume', DataObj_first['Volume'])
						OrderObj.set('cjje', cjje)
						OrderObj.set('transType', transType)
						OrderObj.set('dealTime', dateTime)
						OrderObj.set('profitorLoss', DataObj_first['ProfitorLoss'])
						OrderObj.set('syl', DataObj_first['syl'])
						OrderObj.set('userName',DataObj_first['ZhName'])
						OrderObj.set('headImageUrl',myMatchObj[0].get('headImageUrl'))
						OrderObj.save()
				#count =0
				else:
					#新增

					if myMatchObj:
						OrderObj.set('userObjectId',myMatchObj[0].get('userObjectId'))
						OrderObj.set('userName',DataObj_first['ZhName'])
						OrderObj.set('analogUserId',myMatchObj[0].get('analogUserId'))
						OrderObj.set('headImageUrl',myMatchObj[0].get('headImageUrl'))
						OrderObj.set('matchObjectId',myMatchObj[0].get('matchObjectId'))
						OrderObj.set('matchName',myMatchObj[0].get('matchName'))
						OrderObj.set('analogMatchId',myMatchObj[0].get('analogMatchId'))
						OrderObj.set('groupBmId',DataObj_first['VGroupid'])
						OrderObj.set('mainKeyId', int(DataObj_first['TransRecordId'])) ####注意转换int
						OrderObj.set('stockCode',DataObj_first['StockCode'])
						OrderObj.set('stockName',DataObj_first['stockname'])
						OrderObj.set('marketCode',DataObj_first['marketcode'])
						OrderObj.set('price',DataObj_first['Price'])
						OrderObj.set('volume',DataObj_first['Volume'])
						OrderObj.set('cjje',cjje)
						OrderObj.set('transType',transType)
						OrderObj.set('dealTime',dateTime)
						OrderObj.set('profitorLoss',DataObj_first['ProfitorLoss'])
						OrderObj.set('syl',DataObj_first['syl'])
						OrderObj.save()


if __name__ == "__main__":

	Order_object = Order()

	Order_object.OrderPort()
	Order_object.OrderMC()

