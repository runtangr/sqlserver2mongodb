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

		SyncControl = leancloud.Object.extend('SyncControl')
		self.SyncControlObj = SyncControl()
		querySyncInfo = SyncControl.query

		querySyncInfo.equal_to('type', 'histRank')
		syncObj = querySyncInfo.find()
		if len(syncObj) == 0:
			dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
			self.SyncControlObj.set("type", "histRank")
			self.SyncControlObj.set("mainKeyId", 0)
			self.SyncControlObj.set("rsDateTime", "1990-01-01")
			self.SyncControlObj.save()

		self.SyncControlObj = querySyncInfo.first()
		self.maxKeyId = int(self.SyncControlObj.get('mainKeyId'))
		self.rsDateTime = self.SyncControlObj.get('rsDateTime')

		# 历史排名 WebService 测试接口Query_uimsLSPM
		response = client.service.Query_uimsLSPM(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												 rsMainkeyID=self.maxKeyId,
												 rsDatetime=self.rsDateTime
																  )
		try:
			self.HistRank = json.loads(response)
		except Exception, e:
			logging.error("%s  webservice 接口数据获取失败 %s" % (__file__, response))

	def HistRankMC(self):
		'''
		mc更新uimsLSPM(历史排名)表
		'''
		maxKeyId = int(self.SyncControlObj.get('mainKeyId'))

		if self.HistRank["Code"] == 0:
			self.DataObj = json.loads(self.HistRank["DataObj"])  #

			map(self.DealData, self.DataObj)

				
		else:
			logging.warning("提交模拟炒股系统历史排名数据返回失败：%s" %self.HistRank)
			

	def DealData(self, DataObjArr):
		# 判断最后一条
		if DataObjArr == self.DataObj[-1]:
			self.maxKeyId = int(DataObjArr['rsMainkeyID'])
			self.rsDateTime = DataObjArr['rsDateTime']
			self.SyncControlObj.set('mainKeyId', self.maxKeyId)
			self.SyncControlObj.set('rsDateTime', self.rsDateTime)
			self.SyncControlObj.save()
		# 打印
		print ("maxKeyId:", self.maxKeyId, "===", "rsMainKeyID:", DataObjArr['rsMainkeyID'], "===",
			   "rsDateTime:", DataObjArr['rsDateTime'])

		uimsLSPMQuery = leancloud.Query('uimsLSPM')
		uimsLSPMQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
		self.uimsLSPMList = uimsLSPMQuery.find()
		# 编辑
		if len(self.uimsLSPMList) > 0:

			self.Edit(DataObjArr)
		else:
			self.Add(DataObjArr)


	def Edit(self, DataObjArr):

		self.uimsLSPMList[0].set('rsOperateID', str(DataObjArr['rsOperateID']))
		self.uimsLSPMList[0].set('rsStatus', str(DataObjArr['rsStatus']))
		self.uimsLSPMList[0].set('rsProjectId', str(DataObjArr['rsProjectId']))
		self.uimsLSPMList[0].set('rsMainkeyID', DataObjArr['rsMainkeyID'])
		self.uimsLSPMList[0].set('rsDateTime', DataObjArr['rsDateTime'])
		self.uimsLSPMList[0].set('rsDispIndex', str(DataObjArr['rsDispIndex']))
		self.uimsLSPMList[0].set('cgl', str(DataObjArr['cgl']))
		self.uimsLSPMList[0].set('allmoney', str(DataObjArr['allmoney']))
		self.uimsLSPMList[0].set('vgroupid', str(DataObjArr['vgroupid']))
		self.uimsLSPMList[0].set('dqyl', str(DataObjArr['dqyl']))
		self.uimsLSPMList[0].set('pm', int(DataObjArr['pm']))
		self.uimsLSPMList[0].set('djs', str(DataObjArr['djs']))
		self.uimsLSPMList[0].set('groupbm', DataObjArr['groupbm'])
		self.uimsLSPMList[0].set('getedPer', DataObjArr['getedPer'])
		self.uimsLSPMList[0].set('gzz', DataObjArr['gzz'])
		self.uimsLSPMList[0].set('tradeDate', datetime.strptime(DataObjArr["tradeDate"], "%Y-%m-%d %H:%M:%S"))
		self.uimsLSPMList[0].save()


	def Add(self, DataObjArr):
		uimsLSPM = leancloud.Object.extend('uimsLSPM')
		uimsLSPMObj = uimsLSPM()

		uimsLSPMObj.set('rsOperateID', str(DataObjArr['rsOperateID']))
		uimsLSPMObj.set('rsStatus', str(DataObjArr['rsStatus']))
		uimsLSPMObj.set('rsProjectId', str(DataObjArr['rsProjectId']))
		uimsLSPMObj.set('rsMainkeyID', DataObjArr['rsMainkeyID'])
		uimsLSPMObj.set('rsDateTime', DataObjArr['rsDateTime'])
		uimsLSPMObj.set('rsDispIndex', str(DataObjArr['rsDispIndex']))
		uimsLSPMObj.set('cgl', str(DataObjArr['cgl']))
		uimsLSPMObj.set('allmoney', str(DataObjArr['allmoney']))
		uimsLSPMObj.set('vgroupid', str(DataObjArr['vgroupid']))
		uimsLSPMObj.set('dqyl', str(DataObjArr['dqyl']))
		uimsLSPMObj.set('pm', int(DataObjArr['pm']))
		uimsLSPMObj.set('djs', str(DataObjArr['djs']))
		uimsLSPMObj.set('groupbm', DataObjArr['groupbm'])
		uimsLSPMObj.set('getedPer', DataObjArr['getedPer'])
		uimsLSPMObj.set('gzz', DataObjArr['gzz'])
		uimsLSPMObj.set('tradeDate', datetime.strptime(DataObjArr["tradeDate"], "%Y-%m-%d %H:%M:%S"))
		uimsLSPMObj.save()


if __name__ == "__main__":

	HistRank_object = HistRank()

	HistRank_object.HistRankPort()
	HistRank_object.HistRankMC()

