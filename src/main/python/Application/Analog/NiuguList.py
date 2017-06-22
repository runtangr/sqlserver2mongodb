#encoding=utf-8

'''
Modified on June 8, 2017

@author: tangr
'''
 #模拟炒股
 #牛股榜同步

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

class NiuguList:
	def NiuguListPort(self):
		'''
		获取端口数据
		'''
		url = "http://114.80.94.175:8084/Stocks.asmx?WSDL"
		client = Client(url)
		# print (client)

		# 牛股榜 WebService 测试接口Query_uimsNGB
		response = client.service.Query_uimsNGB(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
																  )
		self.NiuguList = json.loads(response)

	def NiuguListMC(self):
		'''
		mc更新uimsNGB(牛股榜)表
		'''

		if self.NiuguList["Code"] == 0:
			self.DataObj = json.loads(self.NiuguList["DataObj"])  #

			map(self.DealData, self.DataObj)

		else:
			logging.warning("提交模拟炒股系统牛股榜数据返回失败：%s" %self.NiuguList)

	def DealData(self, DataObjArr):

		uimsNGBQuery = leancloud.Query('uimsNGB')
		uimsNGBQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
		self.uimsNGBList = uimsNGBQuery.find()


		(self.Edit(DataObjArr)) if len(self.uimsNGBList) > 0 else (self.Add(DataObjArr))


	def Edit(self, DataObjArr):

		self.uimsNGBList[0].set('rsOperateID', str(DataObjArr['rsOperateID']))
		self.uimsNGBList[0].set('rsStatus', str(DataObjArr['rsStatus']))
		self.uimsNGBList[0].set('rsProjectId', str(DataObjArr['rsProjectId']))
		self.uimsNGBList[0].set('rsMainkeyID', DataObjArr['rsMainkeyID'])
		self.uimsNGBList[0].set('rsDateTime', DataObjArr['rsDateTime'])
		self.uimsNGBList[0].set('rsDispIndex', str(DataObjArr['rsDispIndex']))
		self.uimsNGBList[0].set('stockShortname', DataObjArr['stockShortname'])
		self.uimsNGBList[0].set('ownerCount', int(DataObjArr['ownerCount']))
		self.uimsNGBList[0].set('avgPrize', str(DataObjArr['avgPrize']))
		self.uimsNGBList[0].set('groupbm', DataObjArr['groupbm'])
		self.uimsNGBList[0].set('StockCode', DataObjArr['StockCode'])
		self.uimsNGBList[0].set('Stockid', str(DataObjArr['Stockid']))
		self.uimsNGBList[0].save()


	def Add(self, DataObjArr):

		uimsNGB = leancloud.Object.extend('uimsNGB')
		uimsNGBObj = uimsNGB()

		uimsNGBObj.set('rsOperateID', str(DataObjArr['rsOperateID']))
		uimsNGBObj.set('rsStatus', str(DataObjArr['rsStatus']))
		uimsNGBObj.set('rsProjectId', str(DataObjArr['rsProjectId']))
		uimsNGBObj.set('rsMainkeyID', DataObjArr['rsMainkeyID'])
		uimsNGBObj.set('rsDateTime', DataObjArr['rsDateTime'])
		uimsNGBObj.set('rsDispIndex', str(DataObjArr['rsDispIndex']))
		uimsNGBObj.set('stockShortname', DataObjArr['stockShortname'])
		uimsNGBObj.set('ownerCount', int(DataObjArr['ownerCount']))
		uimsNGBObj.set('avgPrize', str(DataObjArr['avgPrize']))
		uimsNGBObj.set('groupbm', DataObjArr['groupbm'])
		uimsNGBObj.set('StockCode', DataObjArr['StockCode'])
		uimsNGBObj.set('Stockid', str(DataObjArr['Stockid']))
		uimsNGBObj.save()


if __name__ == "__main__":

	NiuguList_object = NiuguList()

	NiuguList_object.NiuguListPort()
	NiuguList_object.NiuguListMC()

