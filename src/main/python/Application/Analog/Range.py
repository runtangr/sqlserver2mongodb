#encoding=utf-8

'''
Modified on June 5, 2017

@author: tangr
'''
 #模拟炒股
 #排名数据同步

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

class Range:
	def RangePort(self):
		'''
		获取端口数据
		'''
		url = "http://114.80.94.175:8084/Stocks.asmx?WSDL"
		client = Client(url)
		# print (client)

		SyncControl = leancloud.Object.extend('SyncControl')
		SyncControlObj = SyncControl()
		querySyncInfo = SyncControl.query

		querySyncInfo.equal_to('type', 'range')
		count = querySyncInfo.count()
		if count == 0:
			dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
			SyncControlObj.set("type", "range")
			SyncControlObj.set("mainKeyId", 0)
			SyncControlObj.set("rsDateTime", "2004-02-02")
			SyncControlObj.save()

		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))
		rsDateTime = syncObj.get('rsDateTime')

		# 排名数据同步 WebService 测试接口Query_uimsSYPM
		response = client.service.Query_uimsSYPM(Coordinates='021525374658617185',
												 Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												 rsMainkeyID=maxKeyId,
												 rsDatetime = rsDateTime,
												 flg=1   #
												 )
		self.data = json.loads(response)

	def RangeMC(self):
		'''
		mc更新AnalogRange(成交明细)表
		'''
		RangeMC = self.data
		isChange = 0

		SyncControl = leancloud.Object.extend('SyncControl')
		querySyncInfo = SyncControl.query
		querySyncInfo.equal_to('type', 'range')
		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))

		if RangeMC["Code"] == 0:

			DataObj =  json.loads(RangeMC["DataObj"])#

			#先删除原有数据
			while True:
				queryRange = leancloud.Query('AnalogRange')
				query_list = queryRange.find()
				if len(query_list)==0:
					break
				leancloud.Object.destroy_all(query_list)

			userObjectId = ''
			headImageUrl = ''

			for DataObjArr in DataObj:


				if int(DataObjArr['rsMainkeyID']) > maxKeyId:
					isChange = 1
					maxKeyId = int(DataObjArr['rsMainkeyID'])
					rsDateTime = DataObjArr['rsDateTime']

				print ("maxKeyId:", maxKeyId, "===", "rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
					   "rsDateTime:", DataObjArr['rsDateTime'])


				try:
					AnalogRange = leancloud.Object.extend('AnalogRange')
					RangeObj = AnalogRange()

					#添加userObjectId和 头像headImageUrl
					queryMyMatch = leancloud.Query('AnalogMyMatch')
					queryMyMatch.equal_to('groupBmId', DataObjArr['vgroupid'])
					myMatchObj_list = queryMyMatch.find()
					for myMatchObj in myMatchObj_list:
						userObjectId = myMatchObj.get("userObjectId")
						headImageUrl = myMatchObj.get("headImageUrl")

						pmDay = myMatchObj.get("pmDay")
						pmWeek = myMatchObj.get("pmWeek")
						pmMonth = myMatchObj.get("pmMonth")

					RangeObj.set('userObjectId', userObjectId)
					RangeObj.set('headImageUrl', headImageUrl)

					RangeObj.set('pm',DataObjArr['pm'])
					RangeObj.set('type',DataObjArr['pmType'])
					RangeObj.set('groupBmId',DataObjArr['vgroupid'])
					RangeObj.set('groupBm',DataObjArr['groupbm'])
					RangeObj.set('userName',DataObjArr['groupbm'])
					RangeObj.set('syl',DataObjArr['ror']+'%')
					RangeObj.set('shouYiLv', float(DataObjArr['ror']))
					RangeObj.set('totalCapital',DataObjArr['EndCaptial'])
					RangeObj.set('originalCapital',DataObjArr['OriginalCapital'])
					RangeObj.set('djs',DataObjArr['djs'])
					RangeObj.set('cw',DataObjArr['cw'])
					RangeObj.set('cgl',DataObjArr['cgl'])

					RangeObj.set('pmDay', pmDay)
					RangeObj.set('pmWeek', pmWeek)
					RangeObj.set('pmMonth', pmMonth)
					RangeObj.save()
				except Exception, e:
					logging.error("排名数据更新失败: %s" % DataObjArr)

			if isChange == 1:
				syncObj.set('mainKeyId', maxKeyId)
				syncObj.set('rsDateTime', rsDateTime)
				syncObj.save()

		else:
			logging.warning("提交模拟炒股系统查询日收益排名返回失败：%s"% RangeMC)

if __name__ == "__main__":

	Range_object = Range()

	Range_object.RangePort()
	Range_object.RangeMC()

