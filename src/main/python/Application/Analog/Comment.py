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

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		AnalogSyncInfoObj = AnalogSyncInfo()
		querySyncInfo = AnalogSyncInfo.query

		querySyncInfo.equal_to('type', 'comment')
		count = querySyncInfo.count()
		if count == 0:
			dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
			AnalogSyncInfoObj.set("type","comment")
			AnalogSyncInfoObj.set("mainKeyId",0)
			AnalogSyncInfoObj.set("rsDateTime","2004-02-02")
			AnalogSyncInfoObj.save()

		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))
		rsDateTime = syncObj.get('rsDateTime')

		# 专家点评 WebService 测试接口Query_uimsZJDP
		response = client.service.Query_uimsZJDP(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												 rsMainkeyid=maxKeyId,
												 rsDatetime=rsDateTime
																  )
		self.data = json.loads(response)

	def CommentMC(self):
		'''
		mc更新uimsZJDP(历史排名)表
		'''
		CommentMC = self.data
		isChange = 0

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		querySyncInfo = AnalogSyncInfo.query
		querySyncInfo.equal_to('type', 'comment')
		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))

		if CommentMC["Code"] == 0:

			DataObj =  json.loads(CommentMC["DataObj"])#

			for DataObjArr in DataObj:

				if int(DataObjArr['rsMainkeyID']) > maxKeyId:
					isChange = 1
					maxKeyId = int(DataObjArr['rsMainkeyID'])
					rsDateTime = DataObjArr['rsDateTime']

				print ("maxKeyId:",maxKeyId, "===","rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
					 "rsDateTime:",DataObjArr['rsDateTime'])
				try:
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
					uimsZJDPObj.set('TradeDate',  datetime.strptime(DataObjArr["TradeDate"],"%Y-%m-%d %H:%M:%S"))
					uimsZJDPObj.save()
				except Exception, e:
					logging.error("专家点评数据更新失败: %s" % DataObjArr)
			if isChange == 1:
				syncObj.set('mainKeyId', maxKeyId)
				syncObj.set('rsDateTime', rsDateTime)
				syncObj.save()

		else:
			logging.warning("提交模拟炒股系统专家点评数据返回失败：%s" %CommentMC)

if __name__ == "__main__":

	Comment_object = Comment()

	Comment_object.CommentPort()
	Comment_object.CommentMC()

