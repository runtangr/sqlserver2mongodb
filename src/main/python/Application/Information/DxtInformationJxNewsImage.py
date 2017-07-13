#encoding=utf-8

'''
Modified on June 12, 2017

@author: tangr
'''
 #资讯
 #资讯表

import unittest
from suds.client import Client
import json
from datetime import datetime
import time
import leancloud_patch
import leancloud
from Utils import init_leancloud_client
import logging
import re

logging.basicConfig(level=logging.WARNING,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S'
					)

init_leancloud_client()

class jxNewsImage:
	def CreateSyncInfo(self):
		SyncControl = leancloud.Object.extend('SyncControl')
		self.SyncControlObj = SyncControl()
		querySyncInfo = SyncControl.query

		querySyncInfo.equal_to('type', 'jxNewsImage')
		syncObj = querySyncInfo.find()
		if len(syncObj) == 0:
			self.SyncControlObj.set("type", "jxNewsImage")
			self.SyncControlObj.set("mainKeyId", 0)
			self.SyncControlObj.set("rsDateTime", "1990-01-01")
			self.SyncControlObj.save()

		self.SyncControlObj = querySyncInfo.first()
		self.maxKeyId = int(self.SyncControlObj.get('mainKeyId'))
		self.rsDateTime = self.SyncControlObj.get('rsDateTime')

	def jxNewsImagePort(self):
		'''
		获取端口数据
		'''
		url = "http://61.139.76.139:9527/Stocks.asmx?WSDL"
		client = Client(url)
		# print (client)

		top = 100
		self.CreateSyncInfo()

		# 财富快线新闻 WebService 测试接口 Query_jx_News_Image
		response = client.service.Query_jx_News_Image(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												 rsMainkeyid=self.maxKeyId,
												 rsDatetime=self.rsDateTime,
												 top=top
												)
		try:
			self.jxNewsImage = json.loads(response)
		except Exception, e:
			logging.error("%s  webservice 接口数据获取失败 %s" % (__file__, response))

	def jxNewsImageMC(self):
		'''
		mc更新 A_DxtInformation 资讯栏目更新表
		'''
		maxKeyId = int(self.SyncControlObj.get('mainKeyId'))

		if self.jxNewsImage["Code"] == 0:
			self.DataObj = json.loads(self.jxNewsImage["DataObj"])  #

			map(self.DealData, self.DataObj)

		else:
			logging.warning("not data or data error：%s" % self.jxNewsImage)


	def DealData(self, DataObjArr):
		# 最后一条数据赋值
		if DataObjArr == self.DataObj[-1]:
			self.maxKeyId = int(DataObjArr['rsMainkeyID'])
			self.rsDateTime = DataObjArr['rsDateTime']
			self.SyncControlObj.set('mainKeyId', self.maxKeyId)
			self.SyncControlObj.set('rsDateTime', self.rsDateTime)
			self.SyncControlObj.save()

		# 打印
		print ("maxKeyId:", self.maxKeyId, "===", "rsMainKeyId:", DataObjArr['rsMainkeyID'], "===",
			   "rsDateTime:", DataObjArr['rsDateTime'])

		A_DxtInformationQuery = leancloud.Query('A_DxtInformation')
		A_DxtInformationQuery.equal_to('relationId', DataObjArr['NewsID'])
		# 同步判断
		A_DxtInformationQuery.equal_to('sync', 2)
		self.A_DxtInformationList = A_DxtInformationQuery.find()

		# 编辑
		if len(self.A_DxtInformationList) > 0:

			self.Save(self.A_DxtInformationList[0], DataObjArr)
		else:
			pass

	def Save(self, Obj, DataObjArr):

		if DataObjArr['rsStatus'] >0:
			rsDateTime = datetime.strptime(DataObjArr['rsDateTime'][:-4], '%Y-%m-%d %H:%M:%S')
			Data = []
			Data.append(DataObjArr['Images'])
			# Data["NewsID"] = DataObjArr['NewsID']
			# Data["rsDateTime"] = DataObjArr['rsDateTime']
			# Data["rsDispIndex"] = DataObjArr['rsDispIndex']
			# Data["rsStatus"] = DataObjArr['rsStatus']
			# print("data=",Data)
			# print("object=", Obj.get("objectId"))

			# Obj.set('rsDispIndex', )
			Obj.set('images', Data)
			Obj.save()

if __name__ == "__main__":

	jxNewsImage_object = jxNewsImage()

	jxNewsImage_object.jxNewsImagePort()
	jxNewsImage_object.jxNewsImageMC()

