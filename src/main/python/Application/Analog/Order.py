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
import sys
import leancloud_patch
import leancloud
from Utils import init_leancloud_client
import logging

logging.basicConfig(level=logging.WARNING,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S'
					)

init_leancloud_client()

class Order:
	def OrderPort(self):
		'''
		获取端口数据
		'''
		url = "http://114.80.94.175:8084/Stocks.asmx?WSDL"
		client = Client(url)
		# print (client)
		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		AnalogSyncInfoObj = AnalogSyncInfo()
		querySyncInfo = AnalogSyncInfo.query

		querySyncInfo.equal_to('type', 'order')
		count = querySyncInfo.count()
		if count == 0:
			AnalogSyncInfoObj.set("type", "order")
			AnalogSyncInfoObj.set("mainKeyId", 0)
			AnalogSyncInfoObj.set("rsDateTime", "1990-00-00")
			AnalogSyncInfoObj.save()

		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))
		rsDateTime = syncObj.get('rsDateTime')
		top = 500
		type = 2
		# 成交明细 WebService 测试接口Query_uimsStockTransDetailList
		response = client.service.Query_uimsStockTransDetailList(Coordinates='021525374658617185',
																 Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
																 rsMainkeyID=maxKeyId,
																 rsDatetime=rsDateTime,  # 测试使用
																 SYN_CAT_REF=type,
																 Top=top  # 获取的条数  后期需设置环境变量
																 )
		self.data = json.loads(response)

	def OrderMC(self):
		'''
		mc更新AnalogOrder(成交明细)表
		'''
		OrderMC = self.data
		isChange = 0

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		querySyncInfo = AnalogSyncInfo.query
		querySyncInfo.equal_to('type', 'order')
		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))

		if OrderMC["Code"] == 0:

			MCDataObj = json.loads(OrderMC["DataObj"])
			DataObj =  json.loads(MCDataObj["Data"])#

			style = {
					-1:"卖",
					1:"买",
					20:"分红",
					30:"送股"
					}

			for DataObjArr in DataObj:

				if DataObjArr['rsMainkeyID'] > maxKeyId:
					isChange = 1
					maxKeyId = DataObjArr['rsMainkeyID']
					rsDateTime = DataObjArr['rsDateTime']

				print ("maxKeyId:",maxKeyId, "===","rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
					 "rsDateTime:",DataObjArr['rsDateTime'])

				AnalogOrder = leancloud.Object.extend('AnalogOrder')
				queryOrder = AnalogOrder.query

				#计算
				cjje = DataObjArr['Volume'] * DataObjArr['Price'] - DataObjArr['Commission'] - DataObjArr['Commission1']


				transType =  style[DataObjArr['TransStyle']]
				dateTime = datetime.strptime(DataObjArr["cjdatetime"],"%Y-%m-%d %H:%M:%S")  #转换

				queryOrder.equal_to('mainKeyId',int(DataObjArr["TransRecordId"])) ####注意转换 int
				count = queryOrder.count()
				try:
					if count > 0:
						queryMyMatch = leancloud.Query('AnalogMyMatch')
						queryMyMatch.equal_to('groupBmId', DataObjArr['VGroupid'])
						myMatchObj = queryMyMatch.find()

						if myMatchObj:
							OrderObj = queryOrder.first()

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
						queryMyMatch = leancloud.Query('AnalogMyMatch')
						queryMyMatch.equal_to('groupBmId', DataObjArr['VGroupid'])
						myMatchObj = queryMyMatch.find()
						#新增
						if myMatchObj:
							AnalogOrder = leancloud.Object.extend('AnalogOrder')
							OrderObj = AnalogOrder()

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
				except Exception, e:
					logging.error("成交数据更新失败: %s" % DataObjArr)

			if isChange == 1:
				syncObj.set('mainKeyId', maxKeyId)
				syncObj.set('rsDateTime', rsDateTime)
				syncObj.save()
		else:
			logging.warning("提交模拟炒股系统账户查询返回失败：%s" %OrderMC)

if __name__ == "__main__":

	Order_object = Order()

	Order_object.OrderPort()
	Order_object.OrderMC()

