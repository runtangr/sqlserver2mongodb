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

class jx_News:
	def jx_NewsPort(self):
		'''
		获取端口数据
		'''
		url = "http://61.139.76.139:9527/Stocks.asmx?WSDL"
		client = Client(url)
		# print (client)

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		AnalogSyncInfoObj = AnalogSyncInfo()
		querySyncInfo = AnalogSyncInfo.query

		querySyncInfo.equal_to('type', 'jx_News')
		count = querySyncInfo.count()
		if count == 0:
			dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
			AnalogSyncInfoObj.set("type", "jx_News")
			AnalogSyncInfoObj.set("mainKeyId", 0)
			AnalogSyncInfoObj.set("rsDateTime", "2004-02-02")
			AnalogSyncInfoObj.save()

		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))
		rsDateTime = syncObj.get('rsDateTime')
		top = 500

		# 财富快线新闻 WebService 测试接口Query_jx_News
		response = client.service.Query_jx_News(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												 rsMainkeyid=maxKeyId,
												 rsDatetime=rsDateTime,
												 top=top
												)

		self.jx_News_EDIT = json.loads(response)

	def jx_NewsMC(self):
		'''
		mc更新 A_DxtInformation 资讯栏目更新表
		'''
		jx_NewsMC = self.jx_News_EDIT
		isChange = 0

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		querySyncInfo = AnalogSyncInfo.query
		querySyncInfo.equal_to('type', 'jx_News')
		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))

		if jx_NewsMC["Code"] == 0:

			DataObj =  json.loads(jx_NewsMC["DataObj"])#

			#label
			label = { 1001:"财富早班车",
					  1002:"资讯直通车",
					  1003:"资金全揭秘",
					  1004:"复盘进行时",
					  1005:"中线挖掘机",
					  1006:"首席及时语"
					  }


			for DataObjArr in DataObj:

				if int(DataObjArr['rsMainkeyID']) > maxKeyId:
					isChange = 1
					maxKeyId = int(DataObjArr['rsMainkeyID'])
					rsDateTime = DataObjArr['rsDateTime']

				print ("maxKeyId:",maxKeyId, "===","rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
					 "rsDateTime:",DataObjArr['rsDateTime'])

				#转换
				if DataObjArr['rsStatus'] > 0:
					isDisable = 0
				else:
					isDisable = 1
				NewsTime = datetime.strptime(DataObjArr['NewsTime'], '%Y-%m-%d %H:%M:%S')

				try:
					A_DxtInformation = leancloud.Object.extend('A_DxtInformation')
					A_DxtInformationObj = A_DxtInformation()

					A_DxtInformationObj.set('title', DataObjArr['NewsTitle'])
					A_DxtInformationObj.set('source', DataObjArr['NewsSource'])
					A_DxtInformationObj.set('summary', "") ###
					A_DxtInformationObj.set('thumbnail', DataObjArr['NewsImage'])
					A_DxtInformationObj.set('url', "")
					A_DxtInformationObj.set('content', DataObjArr['NewsContent'])
					A_DxtInformationObj.set('srcContent', DataObjArr['NewsSource'])

					if DataObjArr['CalssID'] in label:
						CalssID = DataObjArr['CalssID']
						tmp = []
						tmp.append(label[CalssID])
						A_DxtInformationObj.set('categories', tmp)
						A_DxtInformationObj.set('labels', tmp)


					A_DxtInformationObj.set('isDisable', isDisable)

					A_DxtInformationObj.set('author', DataObjArr['NewsAuthor'])
					A_DxtInformationObj.set('publishTime', NewsTime)
					A_DxtInformationObj.set('clickNumber', 0)
					A_DxtInformationObj.set('likeNumber', 0)
					A_DxtInformationObj.set('shareNumber', 0)
					A_DxtInformationObj.set('collectNumber', 0)
					A_DxtInformationObj.set('relationId', DataObjArr['rsMainkeyID'])

					A_DxtInformationObj.save()
				except Exception, e:
					logging.error("财富快线新闻数据更新失败: %s" % DataObjArr)

			if isChange == 1:
				syncObj.set('mainKeyId', maxKeyId)
				syncObj.set('rsDateTime', rsDateTime)
				syncObj.save()

		else:
			logging.warning("提交模拟炒股系统财富快线新闻数据返回失败：%s" %jx_NewsMC)

if __name__ == "__main__":

	jx_News_object = jx_News()

	jx_News_object.jx_NewsPort()
	jx_News_object.jx_NewsMC()

