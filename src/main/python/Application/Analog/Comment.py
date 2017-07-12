#encoding=utf-8

'''
Modified on June 8, 2017

@author: tangr
'''
 #模拟炒股
 #专家点评同步

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

class Comment:
	def CommentPort(self):
		'''
		获取端口数据
		'''
		url = "http://114.80.94.175:8084/Stocks.asmx?WSDL"
		client = Client(url)
		# print (client)

		SyncControl = leancloud.Object.extend('SyncControl')
		self.SyncControlObj = SyncControl()
		querySyncInfo = SyncControl.query

		querySyncInfo.equal_to('type', 'comment')
		syncObj = querySyncInfo.find()
		if len(syncObj) == 0:
			dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
			self.SyncControlObj.set("type", "comment")
			self.SyncControlObj.set("mainKeyId", 0)
			self.SyncControlObj.set("rsDateTime", "1990-01-01")
			self.SyncControlObj.save()

		self.SyncControlObj = querySyncInfo.first()
		self.maxKeyId = int(self.SyncControlObj.get('mainKeyId'))
		self.rsDateTime = self.SyncControlObj.get('rsDateTime')

		# 专家点评 WebService 测试接口Query_uimsZJDP
		response = client.service.Query_uimsZJDP(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												 rsMainkeyid=self.maxKeyId,
												 rsDatetime=self.rsDateTime
																  )
		self.Comment = json.loads(response)

	def CommentMC(self):
		'''
		mc更新uimsZJDP(专家点评同步)表
		'''
		maxKeyId = int(self.SyncControlObj.get('mainKeyId'))

		if self.Comment["Code"] == 0:
			self.DataObj = json.loads(self.Comment["DataObj"])  #

			map(self.DealData, self.DataObj)


		else:
			logging.warning("提交模拟炒股系统专家点评数据返回失败：%s" %self.Comment)
			
			

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

		uimsZJDPQuery = leancloud.Query('uimsZJDP')
		uimsZJDPQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
		self.uimsZJDPList = uimsZJDPQuery.find()
		# 编辑
		if len(self.uimsZJDPList) > 0:

			self.Edit(DataObjArr)
		else:
			self.Add(DataObjArr)


	def Edit(self, DataObjArr):

		self.uimsZJDPList[0].set('rsOperateID', str(DataObjArr['rsOperateID']))
		self.uimsZJDPList[0].set('rsStatus', str(DataObjArr['rsStatus']))
		self.uimsZJDPList[0].set('rsProjectId', str(DataObjArr['rsProjectId']))
		self.uimsZJDPList[0].set('getedPer', str(DataObjArr['getedPer']))
		self.uimsZJDPList[0].set('rsMainkeyID', DataObjArr['rsMainkeyID'])
		self.uimsZJDPList[0].set('pm', str(DataObjArr['pm']))
		self.uimsZJDPList[0].set('groupbm', DataObjArr['groupbm'])
		self.uimsZJDPList[0].set('JudgeContent', DataObjArr['JudgeContent'])
		self.uimsZJDPList[0].set('rsDateTime', DataObjArr['rsDateTime'])
		self.uimsZJDPList[0].set('rsDispIndex', str(DataObjArr['rsDispIndex']))
		self.uimsZJDPList[0].set('TradeDate', datetime.strptime(DataObjArr["TradeDate"], "%Y-%m-%d %H:%M:%S"))
		self.uimsZJDPList[0].save()


	def Add(self, DataObjArr):
		uimsZJDP = leancloud.Object.extend('uimsZJDP')
		uimsZJDPObj = uimsZJDP()

		uimsZJDPObj.set('rsOperateID', str(DataObjArr['rsOperateID']))
		uimsZJDPObj.set('rsStatus', str(DataObjArr['rsStatus']))
		uimsZJDPObj.set('rsProjectId', str(DataObjArr['rsProjectId']))
		uimsZJDPObj.set('getedPer', str(DataObjArr['getedPer']))
		uimsZJDPObj.set('rsMainkeyID', DataObjArr['rsMainkeyID'])
		uimsZJDPObj.set('pm', str(DataObjArr['pm']))
		uimsZJDPObj.set('groupbm', DataObjArr['groupbm'])
		uimsZJDPObj.set('JudgeContent', DataObjArr['JudgeContent'])
		uimsZJDPObj.set('rsDateTime', DataObjArr['rsDateTime'])
		uimsZJDPObj.set('rsDispIndex', str(DataObjArr['rsDispIndex']))
		uimsZJDPObj.set('TradeDate', datetime.strptime(DataObjArr["TradeDate"], "%Y-%m-%d %H:%M:%S"))
		uimsZJDPObj.save()

if __name__ == "__main__":

	Comment_object = Comment()

	Comment_object.CommentPort()
	Comment_object.CommentMC()

