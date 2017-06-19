#encoding=utf-8

'''
Modified on June 8, 2017

@author: tangr
'''
 #模拟炒股
 #历史排名同步

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

class HistRank:
	def HistRankPort(self):
		'''
		获取端口数据
		'''
		url = "http://114.80.94.175:8084/Stocks.asmx?WSDL"
		client = Client(url)
		# print (client)

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		AnalogSyncInfoObj = AnalogSyncInfo()
		querySyncInfo = AnalogSyncInfo.query

		querySyncInfo.equal_to('type', 'histRank')
		count = querySyncInfo.count()
		if count == 0:
			dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
			AnalogSyncInfoObj.set("type", "histRank")
			AnalogSyncInfoObj.set("mainKeyId", 0)
			AnalogSyncInfoObj.set("rsDateTime", "2004-02-02")
			AnalogSyncInfoObj.save()

		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))
		rsDateTime = syncObj.get('rsDateTime')

		# 历史排名 WebService 测试接口Query_uimsLSPM
		response = client.service.Query_uimsLSPM(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												 rsMainkeyID=maxKeyId,
												 rsDatetime=rsDateTime
																  )
		self.data = json.loads(response)

	def HistRankMC(self):
		'''
		mc更新uimsLSPM(历史排名)表
		'''
		HistRankMC = self.data

		isChange = 0

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		querySyncInfo = AnalogSyncInfo.query
		querySyncInfo.equal_to('type', 'histRank')
		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))

		if HistRankMC["Code"] == 0:

			DataObj =  json.loads(HistRankMC["DataObj"])#

			for DataObjArr in DataObj:

				if int(DataObjArr['rsMainkeyID']) > maxKeyId:
					isChange = 1
					maxKeyId = int(DataObjArr['rsMainkeyID'])
					rsDateTime = DataObjArr['rsDateTime']

				print ("maxKeyId:", maxKeyId, "===", "rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
					   "rsDateTime:", DataObjArr['rsDateTime'])

				try:
					uimsLSPM = leancloud.Object.extend('uimsLSPM')
					uimsLSPMObj = uimsLSPM()

					uimsLSPMObj.set('rsOperateID', str(DataObjArr['rsOperateID']))
					uimsLSPMObj.set('rsStatus', str(DataObjArr['rsStatus']))
					uimsLSPMObj.set('rsProjectId', str(DataObjArr['rsProjectId']))
					uimsLSPMObj.set('rsMainkeyID', DataObjArr['rsMainkeyID'])
					uimsLSPMObj.set('rsDateTime', DataObjArr['rsDateTime'])
					uimsLSPMObj.set('rsDispIndex', str(DataObjArr['rsDispIndex']))
					uimsLSPMObj.set('cgl',str(DataObjArr['cgl']))
					uimsLSPMObj.set('allmoney',str(DataObjArr['allmoney']))
					uimsLSPMObj.set('vgroupid',str(DataObjArr['vgroupid']))
					uimsLSPMObj.set('dqyl',str(DataObjArr['dqyl']))
					uimsLSPMObj.set('pm',int(DataObjArr['pm']))
					uimsLSPMObj.set('djs',str(DataObjArr['djs']))
					uimsLSPMObj.set('groupbm',DataObjArr['groupbm'])
					uimsLSPMObj.set('getedPer',DataObjArr['getedPer'])
					uimsLSPMObj.set('gzz',DataObjArr['gzz'])
					uimsLSPMObj.set('tradeDate', datetime.strptime(DataObjArr["tradeDate"],"%Y-%m-%d %H:%M:%S"))
					uimsLSPMObj.save()
				except Exception, e:
					logging.error("历史排名更新失败: %s" % DataObjArr)

			if isChange == 1:
				syncObj.set('mainKeyId', maxKeyId)
				syncObj.set('rsDateTime', rsDateTime)
				syncObj.save()
		else:
			logging.warning("提交模拟炒股系统历史排名数据返回失败：%s" %HistRankMC)

if __name__ == "__main__":

	HistRank_object = HistRank()

	HistRank_object.HistRankPort()
	HistRank_object.HistRankMC()

