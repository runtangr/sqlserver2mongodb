#encoding=utf-8

'''
Modified on June 5, 2017

@author: tangr
'''
 #模拟炒股
 #资金持仓数据同步

import unittest
from suds.client import Client
import json
from datetime import datetime
import time
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

		# 设置当前时间请求
        dataTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 资金持仓 WebService 测试接口Query_uimsStockTransList
        response = client.service.Query_uimsStockTransList(Coordinates='021525374658617185',
														   Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
														   rsMainkeyID=0,
														   rsDatetime=dataTime,
														   SYN_CAT_REF=2,
														   Top=1000  # 获取的条数  后期需设置环境变量
														   )

        self.data = json.loads(response)


    def OrderMC(self):
		'''
		mc更新AnalogStock和AnalogMyMatch表
		'''

		OrderMC = self.data
		AnalogStock = leancloud.Object.extend('AnalogStock')
		StockObj = AnalogStock()
		queryStock = AnalogStock.query

		AnalogMyMatch = leancloud.Object.extend('AnalogMyMatch')
		queryMyMatch = AnalogMyMatch.query

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		querySyncInfo = AnalogSyncInfo.query
		querySyncInfo.equal_to('type', 'account')
		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))

		if OrderMC["Code"] == 0:

			DataObj =  json.loads(OrderMC["DataObj"])#
			dataList = json.loads(DataObj['Data'])

			for DataObjArr in dataList:
				if DataObjArr['rsMainkeyID'] > maxKeyId:
					isChange = 1
					maxKeyId = DataObjArr['rsMainkeyID']
					rsDateTime = DataObjArr['rsDateTime']

				print (maxKeyId,"===",DataObjArr['rsMainkeyID'],"===",
					   DataObjArr['VGroupid'],"===",DataObjArr['rsDateTime'],"\r\n")

				# try{
				# $myMatchQuery = new LeanQuery('AnalogMyMatch');
				queryMyMatch.equal_to('groupBmId', DataObjArr['VGroupid'])
				myMatchObj = queryMyMatch.find()
				if myMatchObj:
					# syl = number_format(DataObjArr['syl_all'] * 100, 2)
					# sylday = number_format(DataObjArr['syl_day'] * 100, 2)
					# sylweek = number_format(DataObjArr['syl_week'] * 100, 2)
					myMatchObj[0].set('originalCapital', DataObjArr['OriginalCapital'])
					myMatchObj[0].set('residualCapital', DataObjArr['ResidualCapital'])
					myMatchObj[0].set('frozenCapital', DataObjArr['FrozenCapital'])
					myMatchObj[0].set('syl', "{$syl}%")
					myMatchObj[0].set('sylDay', "{$sylday}%")
					myMatchObj[0].set('sylWeek', "{$sylweek}%")
					myMatchObj[0].set('shouYiLv', round(DataObjArr['syl_all'] * 100, 2))
					myMatchObj[0].set('shouYiLvDay', round(DataObjArr['syl_day'] * 100, 2))
					myMatchObj[0].set('shouYiLvWeek', round(DataObjArr['syl_week'] * 100, 2))
					myMatchObj[0].set('pm', DataObjArr['pm_all'])
					myMatchObj[0].set('pmDay', DataObjArr['pm_Day'])
					myMatchObj[0].set('pmWeek', DataObjArr['pm_week'])
					myMatchObj[0].set('tradeTotal', DataObjArr['tradeTotal'])
					myMatchObj[0].set('tradeCountYL', DataObjArr['tradeCount'])
					myMatchObj[0].set('myPopularity', DataObjArr['djs'])
					myMatchObj[0].set('totalProfitorLoss', DataObjArr['sy_all'])
					myMatchObj[0].set('userName', DataObjArr['ZhName'])
					myMatchObj[0].save()
				#计算
				# cjje = DataObjArr['Volume'] * DataObjArr['Price'] - DataObjArr['Commission'] - DataObjArr['Commission1']
				# transType =  "买" if DataObjArr['TransStyle'] == 1 else "卖"
				# dateTime = datetime.strptime(DataObjArr["cjdatetime"],"%Y-%m-%d %H:%M:%S")  #转换


				# queryOrder.equal_to('mainKeyId',int(DataObjArr["TransRecordId"])) ####注意转换 int
				# count = queryOrder.count()



if __name__ == "__main__":

	Order_object = Order()

	Order_object.OrderPort()
	Order_object.OrderMC()

