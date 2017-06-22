#encoding=utf-8

'''
Modified on June 8, 2017

@author: tangr
'''
 #模拟炒股
 #获奖感言同步

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

class Speech:
	def SpeechPort(self):
		'''
		获取端口数据
		'''
		url = "http://114.80.94.175:8084/Stocks.asmx?WSDL"
		client = Client(url)
		# print (client)

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		self.AnalogSyncInfoObj = AnalogSyncInfo()
		querySyncInfo = AnalogSyncInfo.query

		querySyncInfo.equal_to('type', 'speech')
		syncObj = querySyncInfo.find()
		if len(syncObj) == 0:
			dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
			self.AnalogSyncInfoObj.set("type", "speech")
			self.AnalogSyncInfoObj.set("mainKeyId", 0)
			self.AnalogSyncInfoObj.set("rsDateTime", "1990-01-01")
			self.AnalogSyncInfoObj.save()

		self.AnalogSyncInfoObj = querySyncInfo.first()
		self.maxKeyId = int(self.AnalogSyncInfoObj.get('mainKeyId'))
		self.rsDateTime = self.AnalogSyncInfoObj.get('rsDateTime')


		# 获奖感言 WebService 测试接口Query_uimsHJGY
		response = client.service.Query_uimsHJGY(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												rsMainkeyID=self.maxKeyId,
												rsDatetime= self.rsDateTime,
												flg=0
												 )
		self.Speech = json.loads(response)

	def SpeechMC(self):
		'''
		mc更新uimsHJGY(获奖感言)表
		'''
		maxKeyId = int(self.AnalogSyncInfoObj.get('mainKeyId'))

		if self.Speech["Code"] == 0:
			self.DataObj = json.loads(self.Speech["DataObj"])  #

			map(self.DealData, self.DataObj)


		else:
			logging.warning("提交模拟炒股系统获奖感言数据返回失败：%s" %self.Speech)
			
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

		uimsHJGYQuery = leancloud.Query('uimsHJGY')
		uimsHJGYQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
		self.uimsHJGYList = uimsHJGYQuery.find()

		(self.Edit(DataObjArr)) if len(self.uimsHJGYList) > 0 else (self.Add(DataObjArr))


	def Edit(self, DataObjArr):

		self.uimsHJGYList[0].set('BlogAddress', DataObjArr['BlogAddress'])
		self.uimsHJGYList[0].set('rsMainkeyID', DataObjArr['rsMainkeyID'])
		self.uimsHJGYList[0].set('Ror', str(DataObjArr['Ror']))
		self.uimsHJGYList[0].set('rsOperateID', str(DataObjArr['rsOperateID']))
		self.uimsHJGYList[0].set('rsStatus', str(DataObjArr['rsStatus']))
		self.uimsHJGYList[0].set('shouyi', DataObjArr['shouyi'])
		self.uimsHJGYList[0].set('rsProjectId', str(DataObjArr['rsProjectId']))
		self.uimsHJGYList[0].set('PlatForms', DataObjArr['PlatForms'])
		self.uimsHJGYList[0].set('FbTime', DataObjArr['FbTime'])
		self.uimsHJGYList[0].set('ZhName', DataObjArr['ZhName'])
		self.uimsHJGYList[0].set('VGroupId', str(DataObjArr['VGroupId']))
		self.uimsHJGYList[0].set('rsDateTime', DataObjArr['rsDateTime'])
		self.uimsHJGYList[0].set('rsDispIndex', str(DataObjArr['rsDispIndex']))
		self.uimsHJGYList[0].set('Picture', DataObjArr['Picture'])
		self.uimsHJGYList[0].save()


	def Add(self, DataObjArr):
		uimsHJGY = leancloud.Object.extend('uimsHJGY')
		uimsHJGYObj = uimsHJGY()

		uimsHJGYObj.set('BlogAddress', DataObjArr['BlogAddress'])
		uimsHJGYObj.set('rsMainkeyID', DataObjArr['rsMainkeyID'])
		uimsHJGYObj.set('Ror', str(DataObjArr['Ror']))
		uimsHJGYObj.set('rsOperateID', str(DataObjArr['rsOperateID']))
		uimsHJGYObj.set('rsStatus', str(DataObjArr['rsStatus']))
		uimsHJGYObj.set('shouyi', DataObjArr['shouyi'])
		uimsHJGYObj.set('rsProjectId', str(DataObjArr['rsProjectId']))
		uimsHJGYObj.set('PlatForms', DataObjArr['PlatForms'])
		uimsHJGYObj.set('FbTime', DataObjArr['FbTime'])
		uimsHJGYObj.set('ZhName', DataObjArr['ZhName'])
		uimsHJGYObj.set('VGroupId', str(DataObjArr['VGroupId']))
		uimsHJGYObj.set('rsDateTime', DataObjArr['rsDateTime'])
		uimsHJGYObj.set('rsDispIndex', str(DataObjArr['rsDispIndex']))
		uimsHJGYObj.set('Picture', DataObjArr['Picture'])
		uimsHJGYObj.save()


if __name__ == "__main__":

	Speech_object = Speech()

	Speech_object.SpeechPort()
	Speech_object.SpeechMC()

