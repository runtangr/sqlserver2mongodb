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

		querySyncInfo.equal_to('type', 'position')
		count = querySyncInfo.count()
		if count == 0:
			AnalogSyncInfoObj.set("type", "position")
			AnalogSyncInfoObj.set("mainKeyId", 0)
			AnalogSyncInfoObj.set("rsDateTime", "1990-00-00")
			AnalogSyncInfoObj.save()

		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))
		rsDateTime = syncObj.get('rsDateTime')
		top = 200
		type = 2

	# 资金持仓 WebService 测试接口Query_uimsStockTransList
		response = client.service.Query_uimsStockTransList(Coordinates='021525374658617185',
														   Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
														   rsMainkeyID=maxKeyId,
														   rsDatetime=rsDateTime, #测试使用
														   SYN_CAT_REF=type,
														   Top=top  # 获取的条数  后期需设置环境变量
														   )

		self.data = json.loads(response)

	def OrderMC(self):
		'''
		mc更新AnalogStock和AnalogMyMatch表
		'''

		OrderMC = self.data

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		querySyncInfo = AnalogSyncInfo.query
		querySyncInfo.equal_to('type', 'position')
		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))

		isChange = 0

		if OrderMC["Code"] == 0:

			DataObj =  json.loads(OrderMC["DataObj"])#
			dataList = json.loads(DataObj['Data'])

			for DataObjArr in dataList:
				if int(DataObjArr['rsMainkeyID']) > maxKeyId:
					isChange = 1
					maxKeyId = int(DataObjArr['rsMainkeyID'])
					rsDateTime = DataObjArr['rsDateTime']

				print ("maxKeyId:", maxKeyId, "===", "rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
					   "VGroupid:", DataObjArr['VGroupid'], "===", "rsDateTime:", DataObjArr['rsDateTime'], "\r\n")


				queryMyMatch = leancloud.Query('AnalogMyMatch')
				queryMyMatch.equal_to('groupBmId', DataObjArr['VGroupid'])
				myMatchObj = queryMyMatch.find()
				if myMatchObj:

					queryUser = leancloud.Query('_User')
					queryUser.equal_to('userId', DataObjArr['UserId'])
					try:
						userObj = queryUser.first()
					except Exception, e:
						userObj = leancloud.User()
						userObj.set_username(DataObjArr['CountName'])
						userObj.set_password('a123456')
						userObj.set('userId', DataObjArr['UserId'])
						userObj.set('nickname', DataObjArr['ZhName'])
						userObj.sign_up()

					myMatchObj[0].set('userObjectId', userObj.id)
					myMatchObj[0].set('headImageUrl', userObj.get('headImageUrl'))

					syl = '%.2f' %(DataObjArr['syl_all'] * 100)
					sylday = '%.2f' %(DataObjArr['syl_day'] * 100)
					sylweek = '%.2f' %(DataObjArr['syl_week'] * 100)
					myMatchObj[0].set('originalCapital', DataObjArr['OriginalCapital']) #ok
					myMatchObj[0].set('residualCapital', DataObjArr['ResidualCapital'])
					myMatchObj[0].set('frozenCapital', DataObjArr['FrozenCapital'])
					myMatchObj[0].set('syl', syl+'%')
					myMatchObj[0].set('sylDay', sylday+"%")
					myMatchObj[0].set('sylWeek', sylweek+"%")
					myMatchObj[0].set('shouYiLv', round(DataObjArr['syl_all'] * 100, 2))#
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

				else:
					#补齐用户
					queryUser = leancloud.Query('_User')

					queryUser.equal_to('userId',DataObjArr['UserId'])
					try:
						userObj = queryUser.first()
					except Exception, e:
						userObj = leancloud.User()
						userObj.set_username(DataObjArr['CountName'])
						userObj.set_password('a123456')
						userObj.set('userId', DataObjArr['UserId'])
						userObj.set('nickname', DataObjArr['ZhName'])
						continue
						userObj.sign_up()

					#大赛记录
					queryMatch = leancloud.Query('AnalogMatch')
					matchObject = queryMatch.first()

					syl = '%.2f'%(DataObjArr['syl_all'] * 100)
					sylday = '%.2f'%(DataObjArr['syl_day'] * 100)
					sylweek = '%.2f'%(DataObjArr['syl_week'] * 100)

					AnalogMyMatch = leancloud.Object.extend('AnalogMyMatch')
					myMatchObject = AnalogMyMatch()

					# User = leancloud.Object.extend('_User')
					# queryUser =leancloud.Query(User)
					# queryUser.equal_to('userId', DataObjArr['UserId'])
					# queryUser.equal_to('userId', 2504655)
					# queryUser.equal_to('userId', 96553)
					# queryUser.limit(10)
					# planList = queryUser.find()
					# for plan in planList:
					# 	print plan.dump()
					# print len(planList)

					# userObj = queryUser.first()

					myMatchObject.set('userObjectId',userObj.id)
					myMatchObject.set('headImageUrl',userObj.get('headImageUrl'))
					myMatchObject.set('userName', DataObjArr['ZhName'])
					myMatchObject.set('analogUserId', DataObjArr['UserId'])
					myMatchObject.set('matchObjectId',matchObject.id)
					myMatchObject.set('matchName',matchObject.get('matchName'))
					myMatchObject.set('analogMatchId',matchObject.get('analogMatchId'))
					myMatchObject.set('beginTime',matchObject.get('beginTime'))
					myMatchObject.set('endTime',matchObject.get('endTime'))
					myMatchObject.set('groupBmId', DataObjArr['VGroupid'])
					myMatchObject.set('originalCapital', DataObjArr['OriginalCapital'])
					myMatchObject.set('residualCapital', DataObjArr['ResidualCapital'])
					myMatchObject.set('frozenCapital', DataObjArr['FrozenCapital'])
					myMatchObject.set('syl', syl+"%")
					myMatchObject.set('sylDay', sylday+"%")
					myMatchObject.set('sylWeek', sylweek+"%")
					myMatchObject.set('shouYiLv', round(DataObjArr['syl_all'] * 100, 2))
					myMatchObject.set('shouYiLvDay', round(DataObjArr['syl_day'] * 100, 2))
					myMatchObject.set('shouYiLvWeek', round(DataObjArr['syl_week'] * 100, 2))
					myMatchObject.set('pm', DataObjArr['pm_all'])
					myMatchObject.set('pmDay', DataObjArr['pm_Day'])
					myMatchObject.set('pmWeek', DataObjArr['pm_week'])
					myMatchObject.set('tradeTotal', DataObjArr['tradeTotal'])
					myMatchObject.set('tradeCountYL', DataObjArr['tradeCount'])
					myMatchObject.set('myPopularity', DataObjArr['djs'])
					myMatchObject.set('totalProfitorLoss', DataObjArr['sy_all'])
					myMatchObject.set('isDefault', '0')
					myMatchObject.save()
					myMatchObj.append(myMatchObject)
					# myMatchObj[0] = myMatchObject

					#如果stockcode不等于000000则更新持仓数据
				if DataObjArr['StockCode'] != "000000":
						queryStock = leancloud.Query('AnalogStock')
						queryStock.equal_to('groupBmId', DataObjArr['VGroupid'])
						queryStock.equal_to('marketCode', DataObjArr['marketcode'])
						queryStock.equal_to('stockCode', DataObjArr['StockCode'])
						count = queryStock.count()
						if count > 0:
							stockObj = queryStock.first()
							#编辑
							if DataObjArr['CurrentVolume'] == 0:
								stockObj.destroy()
							else:
								stockObj.set('totalVolume', DataObjArr['CurrentVolume']) #
								stockObj.set('useVolume', DataObjArr['UseVolume'])
								stockObj.set('cost', DataObjArr['cost'])
								stockObj.set('profitorLoss', DataObjArr['ProfitorLoss'])

								if DataObjArr['CurrentVolume'] == 0:
									stockObj.set('price', 0)
								else:
									stockObj.set('price', round(DataObjArr['cost'] / DataObjArr['CurrentVolume'], 2))

								stockObj.set('stockTypeName', DataObjArr['stockTypeName'])
								stockObj.set('marketName', DataObjArr['marketName'])
								stockObj.set('buyMoney', DataObjArr['BuyMonney'])
								stockObj.set('userName', DataObjArr['ZhName'])
								stockObj.set('headImageUrl',myMatchObj[0].get('headImageUrl'))
								stockObj.save()
						else:
							#新增
							AnalogStock = leancloud.Object.extend('AnalogStock')
							stockObj = AnalogStock()
							for myMatchObjList in myMatchObj:
								userObjectId = myMatchObjList.get('userObjectId')
								analogUserId = myMatchObjList.get('analogUserId')
								headImageUrl = myMatchObjList.get('headImageUrl')
								matchObjectId = myMatchObjList.get('matchObjectId')
								matchName = myMatchObjList.get('matchName')
								analogMatchId = myMatchObjList.get('analogMatchId')

							stockObj.set('userObjectId',userObjectId)
							stockObj.set('userName', DataObjArr['ZhName'])
							stockObj.set('analogUserId',analogUserId)
							stockObj.set('headImageUrl',headImageUrl)
							stockObj.set('matchObjectId',matchObjectId)
							stockObj.set('matchName',matchName)
							stockObj.set('analogMatchId',analogMatchId)
							stockObj.set('groupBmId', DataObjArr['VGroupid'])
							stockObj.set('stockCode', (DataObjArr['StockCode']))
							stockObj.set('marketCode', (DataObjArr['marketcode']))
							stockObj.set('stockName', DataObjArr['stockname'])
							stockObj.set('totalVolume', DataObjArr['CurrentVolume'])
							stockObj.set('useVolume', DataObjArr['UseVolume'])
							#加判断
							if DataObjArr['CurrentVolume'] == 0:
								stockObj.set('price', 0)
							else:
								stockObj.set('price', round(DataObjArr['cost'] / DataObjArr['CurrentVolume'], 2))

							stockObj.set('cost', DataObjArr['cost'])
							stockObj.set('profitorLoss', DataObjArr['ProfitorLoss'])
							stockObj.set('stockTypeName', DataObjArr['stockTypeName'])
							stockObj.set('marketName', DataObjArr['marketName'])
							stockObj.set('buyMoney', DataObjArr['BuyMonney'])
							stockObj.save()
				# except Exception,e:
				# 	logging.error("账户持仓数据更新失败: %s"%DataObjArr)

			if isChange == 1:
				syncObj.set('mainKeyId', maxKeyId)
				syncObj.set('rsDateTime', rsDateTime)
				syncObj.save()

		else:
			logging.warning ("提交模拟炒股系统账户查询返回失败：%s"%OrderMC)

if __name__ == "__main__":

	Order_object = Order()

	Order_object.OrderPort()
	Order_object.OrderMC()

