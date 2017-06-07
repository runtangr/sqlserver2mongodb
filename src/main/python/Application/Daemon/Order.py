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

			for DataObjArr in DataObj:

				#计算
				cjje = DataObjArr['Volume'] * DataObjArr['Price'] - DataObjArr['Commission'] - DataObjArr['Commission1']
				transType =  "买" if DataObjArr['TransStyle'] == 1 else "卖"
				dateTime = datetime.strptime(DataObjArr["cjdatetime"],"%Y-%m-%d %H:%M:%S")  #转换


				queryOrder.equal_to('mainKeyId',int(DataObjArr["TransRecordId"])) ####注意转换 int
				count = queryOrder.count()


				queryMyMatch.equal_to('groupBmId', DataObjArr['VGroupid'])
				myMatchObj = queryMyMatch.find()

				if count > 0:

					if myMatchObj:
						#编辑
						OrderObj.set('stockCode', DataObjArr['StockCode'])
						OrderObj.set('stockName', DataObjArr['stockname'])
						OrderObj.set('marketCode', DataObjArr['marketcode'])
						OrderObj.set('price', DataObjArr['Price'])
						OrderObj.set('volume', DataObjArr['Volume'])
						OrderObj.set('cjje', cjje)
						OrderObj.set('transType', transType)
						OrderObj.set('dealTime', dateTime)
						OrderObj.set('profitorLoss', DataObjArr['ProfitorLoss'])
						OrderObj.set('syl', DataObjArr['syl'])
						OrderObj.set('userName',DataObjArr['ZhName'])
						OrderObj.set('headImageUrl',myMatchObj[0].get('headImageUrl'))
						OrderObj.save()
				#count =0
				else:
					#新增

					if myMatchObj:
						OrderObj.set('userObjectId',myMatchObj[0].get('userObjectId'))
						OrderObj.set('userName',DataObjArr['ZhName'])
						OrderObj.set('analogUserId',myMatchObj[0].get('analogUserId'))
						OrderObj.set('headImageUrl',myMatchObj[0].get('headImageUrl'))
						OrderObj.set('matchObjectId',myMatchObj[0].get('matchObjectId'))
						OrderObj.set('matchName',myMatchObj[0].get('matchName'))
						OrderObj.set('analogMatchId',myMatchObj[0].get('analogMatchId'))
						OrderObj.set('groupBmId',DataObjArr['VGroupid'])
						OrderObj.set('mainKeyId', int(DataObjArr['TransRecordId'])) ####注意转换int
						OrderObj.set('stockCode',DataObjArr['StockCode'])
						OrderObj.set('stockName',DataObjArr['stockname'])
						OrderObj.set('marketCode',DataObjArr['marketcode'])
						OrderObj.set('price',DataObjArr['Price'])
						OrderObj.set('volume',DataObjArr['Volume'])
						OrderObj.set('cjje',cjje)
						OrderObj.set('transType',transType)
						OrderObj.set('dealTime',dateTime)
						OrderObj.set('profitorLoss',DataObjArr['ProfitorLoss'])
						OrderObj.set('syl',DataObjArr['syl'])
						OrderObj.save()


if __name__ == "__main__":

	Order_object = Order()

	Order_object.OrderPort()
	Order_object.OrderMC()

