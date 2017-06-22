#encoding=utf-8

'''
Modified on June 8, 2017

@author: tangr
'''
 #模拟炒股
 #赛季同步

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

class Season:
	def SeasonPort(self):
		'''
		获取端口数据
		'''
		url = "http://114.80.94.175:8084/Stocks.asmx?WSDL"
		client = Client(url)
		# print (client)

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		self.AnalogSyncInfoObj = AnalogSyncInfo()
		querySyncInfo = AnalogSyncInfo.query

		querySyncInfo.equal_to('type', 'season')
		syncObj = querySyncInfo.find()
		if len(syncObj) == 0:
			dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
			self.AnalogSyncInfoObj.set("type", "season")
			self.AnalogSyncInfoObj.set("mainKeyId", 0)
			self.AnalogSyncInfoObj.set("rsDateTime", "1990-01-01")
			self.AnalogSyncInfoObj.save()

		self.AnalogSyncInfoObj = querySyncInfo.first()
		self.maxKeyId = int(self.AnalogSyncInfoObj.get('mainKeyId'))
		self.rsDateTime = self.AnalogSyncInfoObj.get('rsDateTime')


		# 赛季同步 WebService 测试接口Query_uimsSEASONSET
		response = client.service.Query_uimsSEASONSET(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												 rsMainkeyid=self.maxKeyId,
												 rsDatetime=self.rsDateTime
																  )
		try:
			self.Season = json.loads(response)
		except Exception, e:
			logging.error("%s  webservice 接口数据获取失败 %s" % (__file__, response))

	def SeasonMC(self):
		'''
		mc更新uimsSeasonSet(赛季同步)表
		'''

		maxKeyId = int(self.AnalogSyncInfoObj.get('mainKeyId'))

		if self.Season["Code"] == 0:
			self.DataObj = json.loads(self.Season["DataObj"])  #

			map(self.DealData, self.DataObj)
				

		else:
			logging.warning("提交模拟炒股系统赛季同步数据返回失败：%s" % self.Season)

	

	

	def DealData(self, DataObjArr):
		# 判断最后一条
		if DataObjArr == self.DataObj[-1]:
			self.maxKeyId = int(DataObjArr['rsMainkeyID'])
			self.rsDateTime = DataObjArr['rsDateTime']
			self.AnalogSyncInfoObj.set('mainKeyId', self.maxKeyId)
			self.AnalogSyncInfoObj.set('rsDateTime', self.rsDateTime)
			self.AnalogSyncInfoObj.save()
		# 打印
		print ("maxKeyId:", self.maxKeyId, "===", "rsMainKeyID:", DataObjArr['rsMainkeyID'], "===",
			   "rsDateTime:", DataObjArr['rsDateTime'])

		uimsSeasonSetQuery = leancloud.Query('uimsSeasonSet')
		uimsSeasonSetQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
		self.uimsSeasonSetList = uimsSeasonSetQuery.find()
		# 编辑
		if len(self.uimsSeasonSetList) > 0:

			self.Edit(DataObjArr)
		else:
			self.Add(DataObjArr)


	def Edit(self, DataObjArr):

		self.uimsSeasonSetList[0].set('rsOperateID', str(DataObjArr['rsOperateID']))
		self.uimsSeasonSetList[0].set('rsStatus', str(DataObjArr['rsStatus']))
		self.uimsSeasonSetList[0].set('rsProjectId', str(DataObjArr['rsProjectId']))
		self.uimsSeasonSetList[0].set('rsMainkeyID', DataObjArr['rsMainkeyID'])
		self.uimsSeasonSetList[0].set('rsDateTime', DataObjArr['rsDateTime'])
		self.uimsSeasonSetList[0].set('rsDispIndex', str(DataObjArr['rsDispIndex']))
		self.uimsSeasonSetList[0].set('SeasonId', str(DataObjArr['SeasonId']))
		self.uimsSeasonSetList[0].set('GroupStyle', str(DataObjArr['GroupStyle']))
		self.uimsSeasonSetList[0].set('StartDate', datetime.strptime(DataObjArr["StartDate"], "%Y-%m-%d %H:%M:%S"))
		self.uimsSeasonSetList[0].set('EndDate', datetime.strptime(DataObjArr["EndDate"], "%Y-%m-%d %H:%M:%S"))
		self.uimsSeasonSetList[0].save()


	def Add(self, DataObjArr):
		uimsSeasonSet = leancloud.Object.extend('uimsSeasonSet')
		uimsSeasonSetObj = uimsSeasonSet()

		uimsSeasonSetObj.set('rsOperateID', str(DataObjArr['rsOperateID']))
		uimsSeasonSetObj.set('rsStatus', str(DataObjArr['rsStatus']))
		uimsSeasonSetObj.set('rsProjectId', str(DataObjArr['rsProjectId']))
		uimsSeasonSetObj.set('rsMainkeyID', DataObjArr['rsMainkeyID'])
		uimsSeasonSetObj.set('rsDateTime', DataObjArr['rsDateTime'])
		uimsSeasonSetObj.set('rsDispIndex', str(DataObjArr['rsDispIndex']))
		uimsSeasonSetObj.set('SeasonId', str(DataObjArr['SeasonId']))
		uimsSeasonSetObj.set('GroupStyle', str(DataObjArr['GroupStyle']))
		uimsSeasonSetObj.set('StartDate', datetime.strptime(DataObjArr["StartDate"], "%Y-%m-%d %H:%M:%S"))
		uimsSeasonSetObj.set('EndDate', datetime.strptime(DataObjArr["EndDate"], "%Y-%m-%d %H:%M:%S"))
		uimsSeasonSetObj.save()

if __name__ == "__main__":

	Season_object = Season()

	Season_object.SeasonPort()
	Season_object.SeasonMC()

