#encoding=utf-8

'''
Modified on May 25, 2017

@author: tangr
'''
 #模拟炒股
 #更新成交明细数据

import unittest
from suds.client import Client
import json
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

		DataObj =  OrderMC["DataObj"]#####

		#计算
		cjje = DataObj['Volume'] * DataObj['Price'] - DataObj['Commission'] - DataObj['Commission1']
		transType =  "买" if DataObj['TransStyle'] == 1 else "卖"
		dateTime = DataObj["cjdatetime"]  #可能要转换 "Y-m-d H:i:s",$v['cjdatetime']

		query = AnalogOrder.query
		query.equal_to('mainKeyId',(DataObj["transRecordid"])) ####注意转换 int
		count = query.count()
		if count > 0:

			myMatchQuery = leancloud.Object.extend('AnalogMyMatch')
			myMatchQuery.equal_to('groupBmId',DataObj['VGroupid'])
			myMatchObj = myMatchQuery.find()
			if myMatchObj:
				#编辑
				OrderObj.set('stockCode', DataObj['StockCode'])
				OrderObj.set('stockName', DataObj['stockname'])
				OrderObj.set('marketCode', DataObj['marketcode'])
				OrderObj.set('price', DataObj['Price'])
				OrderObj.set('volume', DataObj['Volume'])
				OrderObj.set('cjje', cjje)
				OrderObj.set('transType', transType)
				OrderObj.set('dealTime', dateTime)
				OrderObj.set('profitorLoss', DataObj['ProfitorLoss'])
				OrderObj.set('syl', DataObj['syl'])
				OrderObj.set('userName',DataObj['ZhName'])
				OrderObj.set('headImageUrl',myMatchObj[0].get('headImageUrl'))
				OrderObj.save()
		#count =0
		else:
			#新增

			myMatchQuery = leancloud.Object.extend('AnalogMyMatch')
			myMatchQuery.equal_to('groupBmId', DataObj['VGroupid'])
			myMatchObj = myMatchQuery.find()
			if myMatchObj:
				OrderObj.set('userObjectId',myMatchObj[0].get('userObjectId'))
				OrderObj.set('userName',DataObj['ZhName'])
				OrderObj.set('analogUserId',myMatchObj[0].get('analogUserId'))
				OrderObj.set('headImageUrl',myMatchObj[0].get('headImageUrl'))
				OrderObj.set('matchObjectId',myMatchObj[0].get('matchObjectId'))
				OrderObj.set('matchName',myMatchObj[0].get('matchName'))
				OrderObj.set('analogMatchId',myMatchObj[0].get('analogMatchId'))
				OrderObj.set('groupBmId',DataObj['VGroupid'])
				OrderObj.set('mainKeyId', (DataObj['TransRecordId'])) ####注意转换
				OrderObj.set('stockCode',DataObj['StockCode'])
				OrderObj.set('stockName',DataObj['stockname'])
				OrderObj.set('marketCode',DataObj['marketcode'])
				OrderObj.set('price',DataObj['Price'])
				OrderObj.set('volume',DataObj['Volume'])
				OrderObj.set('cjje',cjje)
				OrderObj.set('transType',transType)
				OrderObj.set('dealTime',dateTime)
				OrderObj.set('profitorLoss',DataObj['ProfitorLoss'])
				OrderObj.set('syl',DataObj['syl'])
				OrderObj.save()


if __name__ == "__main__":

	Order_object = Order()

	Order_object.OrderPort()
	Order_object.OrderMC()

