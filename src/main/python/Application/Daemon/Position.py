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
        url = "http://10.30.0.122:8091/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

		# 设置当前时间请求
        dataTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

	# 资金持仓 WebService 测试接口Query_uimsStockTransList
        response = client.service.Query_uimsStockTransList(Coordinates='021525374658617185',
														   Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
														   rsMainkeyID=0,
														   # rsDatetime=dataTime,
														   rsDatetime="2012-06-02 10:15:0", #测试使用
														   SYN_CAT_REF=2,
														   Top=1000  # 获取的条数  后期需设置环境变量
														   )

        self.data = json.loads(response)

    def OrderMC(self):
		'''
		mc更新AnalogStock和AnalogMyMatch表
		'''

		OrderMC = self.data

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		querySyncInfo = AnalogSyncInfo.query
		querySyncInfo.equal_to('type', 'account')
		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))

		isChange = 0

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

				try:
					queryMyMatch = leancloud.Query('AnalogMyMatch')
					queryMyMatch.equal_to('groupBmId', DataObjArr['VGroupid'])
					myMatchObj = queryMyMatch.find()
					if myMatchObj:
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
							userObj.sign_up()

						#大赛记录
						queryMatch = leancloud.Query('AnalogMatch')
						matchObject = queryMatch.first()

						syl = '%.2f'%(DataObjArr['syl_all'] * 100)
						sylday = '%.2f'%(DataObjArr['syl_day'] * 100)
						sylweek = '%.2f'%(DataObjArr['syl_week'] * 100)

						AnalogMyMatch = leancloud.Object.extend('AnalogMyMatch')
						MyMatchObj = AnalogMyMatch()

						MyMatchObj.set('userObjectId',userObj.id)
						MyMatchObj.set('headImageUrl',userObj.get('headImageUrl'))
						MyMatchObj.set('userName', DataObjArr['ZhName'])
						MyMatchObj.set('analogUserId', DataObjArr['UserId'])
						MyMatchObj.set('matchObjectId',matchObject.id)
						MyMatchObj.set('matchName',matchObject.get('matchName'))
						MyMatchObj.set('analogMatchId',matchObject.get('analogMatchId'))
						MyMatchObj.set('beginTime',matchObject.get('beginTime'))
						MyMatchObj.set('endTime',matchObject.get('endTime'))
						MyMatchObj.set('groupBmId', DataObjArr['VGroupid'])
						MyMatchObj.set('originalCapital', DataObjArr['OriginalCapital'])
						MyMatchObj.set('residualCapital', DataObjArr['ResidualCapital'])
						MyMatchObj.set('frozenCapital', DataObjArr['FrozenCapital'])
						MyMatchObj.set('syl', syl+"%")
						MyMatchObj.set('sylDay', sylday+"%")
						MyMatchObj.set('sylWeek', sylweek+"%")
						MyMatchObj.set('shouYiLv', round(DataObjArr['syl_all'] * 100, 2))
						MyMatchObj.set('shouYiLvDay', round(DataObjArr['syl_day'] * 100, 2))
						MyMatchObj.set('shouYiLvWeek', round(DataObjArr['syl_week'] * 100, 2))
						MyMatchObj.set('pm', DataObjArr['pm_all'])
						MyMatchObj.set('pmDay', DataObjArr['pm_Day'])
						MyMatchObj.set('pmWeek', DataObjArr['pm_week'])
						MyMatchObj.set('tradeTotal', DataObjArr['tradeTotal'])
						MyMatchObj.set('tradeCountYL', DataObjArr['tradeCount'])
						MyMatchObj.set('myPopularity', DataObjArr['djs'])
						MyMatchObj.set('totalProfitorLoss', DataObjArr['sy_all'])
						MyMatchObj.set('isDefault', '0')
						MyMatchObj.save()
						myMatchObj[0] = MyMatchObj

						#如果stockcode不等于000000则更新持仓数据
					if DataObjArr['StockCode'] != "000000":
						queryStock = leancloud.Query('AnalogStock')
						queryStock.equal_to('groupBmId', DataObjArr['VGroupid'])
						queryStock.equal_to('marketCode', DataObjArr['marketcode'].strip())
						queryStock.equal_to('stockCode', DataObjArr['StockCode'].strip())
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
							stockObj.set('stockCode', (DataObjArr['StockCode']).strip())
							stockObj.set('marketCode', (DataObjArr['marketcode']).strip())
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
				except Exception,e:
					logging.error("账户持仓数据更新失败: %s"%DataObjArr)

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

