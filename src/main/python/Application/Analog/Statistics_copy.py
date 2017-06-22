#encoding=utf-8

'''
Modified on June 8, 2017

@author: tangr
'''
 #模拟炒股
 #大赛统计同步
# 未使用本程序！

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

class Statistics:
	def StatisticsPort(self):
		'''
		获取端口数据
		'''
		url = "http://114.80.94.175:8084/Stocks.asmx?WSDL"
		client = Client(url)
		# print (client)

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		AnalogSyncInfoObj = AnalogSyncInfo()
		querySyncInfo = AnalogSyncInfo.query

		querySyncInfo.equal_to('type', 'comment')
		count = querySyncInfo.count()
		if count == 0:
			dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
			AnalogSyncInfoObj.set("type", "comment")
			AnalogSyncInfoObj.set("mainKeyId", 0)
			AnalogSyncInfoObj.set("rsDateTime", "2004-02-02")
			AnalogSyncInfoObj.save()

		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))
		rsDateTime = syncObj.get('rsDateTime')


	# 大赛统计 WebService P_GameStatistic测试接口
		response = client.service.P_GameStatistic(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A'
												  )
		self.data = json.loads(response)

	def StatisticsMC(self):
		'''
		mc更新AnalogMatch(大赛统计)表
		'''
		StatisticsMC = self.data

		if StatisticsMC["Code"] == 0:

			DataObj =  json.loads(StatisticsMC["DataObj"])#

			for DataObjArr in DataObj:
				try:
					AnalogMatch = leancloud.Object.extend('AnalogMatch')
					AnalogMatchObj = AnalogMatch()

					AnalogMatchObj.set('totalCount', str(DataObjArr['TotalCount']))
					AnalogMatchObj.set('actualCount', str(DataObjArr['ActualCount']))

					AnalogMatchObj.save()
				except Exception, e:
					logging.error("大赛统计数据更新失败: %s" % DataObjArr)

		else:
			logging.warning("提交模拟炒股系统大赛统计数据返回失败：%s" %StatisticsMC)

if __name__ == "__main__":

	Statistics_object = Statistics()

	Statistics_object.StatisticsPort()
	Statistics_object.StatisticsMC()

