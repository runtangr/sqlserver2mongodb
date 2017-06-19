#encoding=utf-8

'''
Modified on June 14, 2017

@author: tangr
'''
 #资讯
 #资讯表
 #  未使用此程序 ！！

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

class CommNewsExtract:
	def CommNewsExtractPort(self):
		'''
		获取端口数据
		'''
		url = "http://61.139.76.139:9527/Stocks.asmx?WSDL"
		client = Client(url)
		# print (client)


		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		AnalogSyncInfoObj = AnalogSyncInfo()
		querySyncInfo = AnalogSyncInfo.query

		querySyncInfo.equal_to('type', 'CommNews_Extract')
		count = querySyncInfo.count()
		if count == 0:
			dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
			AnalogSyncInfoObj.set("type", "CommNews_Extract")
			AnalogSyncInfoObj.set("mainKeyId", 0)
			AnalogSyncInfoObj.set("rsDateTime", "2004-02-02")
			AnalogSyncInfoObj.save()

		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))
		rsDateTime = syncObj.get('rsDateTime')
		top = 1000

		#  技术学堂表WebService 测试接口Query_CommNews_Extract
		response = client.service.Query_CommNews_Extract(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												 rsMainkeyid=maxKeyId,
												rsDatetime=rsDateTime,
												 top=top
													)

		self.CommNews_Extract = json.loads(response)

	def CommNewsExtractMC(self):
		'''
		mc更新 A_DxtInformation 资讯栏目更新表
		'''
		CommNewsExtractMC = self.CommNews_Extract
		isChange = 0

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		querySyncInfo = AnalogSyncInfo.query
		querySyncInfo.equal_to('type', 'CommNews_Extract')
		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))

		if CommNewsExtractMC["Code"] == 0:

			DataObj =  json.loads(CommNewsExtractMC["DataObj"])#

			for DataObjArr in DataObj:

				if DataObjArr['rsMainkeyID'] > maxKeyId:
					isChange = 1
					maxKeyId = DataObjArr['rsMainkeyID']
					rsDateTime = DataObjArr['rsDateTime']

				print ("maxKeyId:",maxKeyId, "===","rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
					 "rsDateTime:",DataObjArr['rsDateTime'])

				try:
					A_DxtInformation = leancloud.Object.extend('A_DxtInformation')
					A_DxtInformationObj = A_DxtInformation()

					A_DxtInformationObj.set('title', DataObjArr['NewsTitle'])
					A_DxtInformationObj.set('source', DataObjArr['NewsSource'])
					A_DxtInformationObj.set('summary', DataObjArr['NewsBrief'])
					A_DxtInformationObj.set('thumbnail', DataObjArr["OtherDefine4"])
					A_DxtInformationObj.set('url', "")
					A_DxtInformationObj.set('content', DataObjArr['NewsContent'])
					A_DxtInformationObj.set('srcContent', DataObjArr['NewsContent'])

					A_DxtInformationObj.set('isDisable', DataObjArr['rsStatus'])  #-1 wei  jingyong

					A_DxtInformationObj.set('author', DataObjArr['NewsAuthor'])
					A_DxtInformationObj.set('publishTime', DataObjArr['NewsDate'])
					A_DxtInformationObj.set('clickNumber', DataObjArr["OtherDefine1"])
					A_DxtInformationObj.set('likeNumber', "")
					A_DxtInformationObj.set('shareNumber', "")
					A_DxtInformationObj.set('collectNumber', DataObjArr["OtherDefine2"])
					A_DxtInformationObj.set('relationId', DataObjArr['rsMainkeyID'])

					A_DxtInformationObj.save()
				except Exception, e:
					logging.error("资讯表 技术学堂表数据更新失败: %s" % DataObjArr)

			if isChange == 1:
				syncObj.set('mainKeyId', maxKeyId)
				syncObj.set('rsDateTime', rsDateTime)
				syncObj.save()

		else:
			logging.warning("提交模拟炒股系统资讯表 技术学堂表数据返回失败：%s" %CommNewsExtractMC)

if __name__ == "__main__":

	CommNewsExtract_object = CommNewsExtract()

	CommNewsExtract_object.CommNewsExtractPort()
	CommNewsExtract_object.CommNewsExtractMC()

