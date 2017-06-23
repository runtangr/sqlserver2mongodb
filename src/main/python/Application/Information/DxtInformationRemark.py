#encoding=utf-8

'''
Modified on June 13, 2017

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

class sirsReportRemark:
	def sirsReportRemarkPort(self):
		'''
		获取端口数据
		'''
		url = "http://61.139.76.139:9527/Stocks.asmx?WSDL"
		client = Client(url)
		# print (client)

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		AnalogSyncInfoObj = AnalogSyncInfo()
		querySyncInfo = AnalogSyncInfo.query

		querySyncInfo.equal_to('type', 'Remark')
		count = querySyncInfo.count()
		if count == 0:
			dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
			AnalogSyncInfoObj.set("type", "Remark")
			AnalogSyncInfoObj.set("mainKeyId", 0)
			AnalogSyncInfoObj.set("rsDateTime", "1990-01-01")
			AnalogSyncInfoObj.save()

		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))
		rsDateTime = syncObj.get('rsDateTime')
		top = 100

		# 钱坤晨会 WebService 测试接口Query_sirsReportRemark
		response = client.service.Query_sirsReportRemark(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												 rsMainkeyid=maxKeyId,
												 rsDatetime=rsDateTime,
												 top=top
													)
		try:
			self.sirsReportRemark = json.loads(response)
		except Exception, e:
			logging.error("%s  webservice 接口数据获取失败 %s" % (__file__, response))

	def sirsReportRemarkMC(self):
		'''
		mc更新 A_DxtInformation 资讯栏目更新表
		'''
		sirsReportRemarkMC = self.sirsReportRemark
		isChange = 0

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		querySyncInfo = AnalogSyncInfo.query
		querySyncInfo.equal_to('type', 'Remark')
		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))

		if sirsReportRemarkMC["Code"] == 0:

			DataObj =  json.loads(sirsReportRemarkMC["DataObj"])#

			#label
			label = { 21058:"钱坤晨会",
					  23784:"数据选股",
					  21057:"热点前瞻"}


			for DataObjArr in DataObj:

				if DataObjArr==DataObj[-1]:
					maxKeyId = int(DataObjArr['rsMainkeyID'])
					rsDateTime = DataObjArr['rsDateTime']
					syncObj.set('mainKeyId', maxKeyId)
					syncObj.set('rsDateTime', rsDateTime)
					syncObj.save()

				print ("maxKeyId:", maxKeyId, "===", "rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
					   "rsDateTime:", DataObjArr['rsDateTime'])

				# 转换
				if DataObjArr['rsStatus'] > 0:
					isDisable = 0
				else:
					isDisable = 1

				RemarkTime = datetime.strptime(DataObjArr['RemarkTime'][:-5], '%Y-%m-%d %H:%M:%S')

				try:
					A_DxtInformationQuery = leancloud.Query('A_DxtInformation')
					A_DxtInformationQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))

					# 同步判断
					A_DxtInformationQuery.equal_to('sync', 3)
					A_DxtInformationList = A_DxtInformationQuery.find()
					# 编辑
					if len(A_DxtInformationList) > 0:

						A_DxtInformationList[0].set('sync', 3)
						A_DxtInformationList[0].set('title', DataObjArr['AttachTitle'])
						A_DxtInformationList[0].set('source', "")
						A_DxtInformationList[0].set('summary', "")  ##content
						A_DxtInformationList[0].set('thumbnail', DataObjArr["OtherDefine8"])
						A_DxtInformationList[0].set('url', DataObjArr['OtherDefine4'])
						A_DxtInformationList[0].set('content', DataObjArr['AttachContent'])
						A_DxtInformationList[0].set('srcContent', DataObjArr['AttachContent'])

						if int(DataObjArr['RemarkClass']) in label:
							RemarkClass = int(DataObjArr['RemarkClass'])
							tmp = []
							tmp.append(label[RemarkClass])
							A_DxtInformationList[0].set('categories', tmp)
							A_DxtInformationList[0].set('labels', tmp)

						A_DxtInformationList[0].set('isDisable',isDisable)

						A_DxtInformationList[0].set('author', DataObjArr['RemarkMan'])
						A_DxtInformationList[0].set('publishTime', RemarkTime)
						A_DxtInformationList[0].set('clickNumber', 0)
						A_DxtInformationList[0].set('likeNumber', 0)
						A_DxtInformationList[0].set('shareNumber', 0)
						A_DxtInformationList[0].set('collectNumber', 0)
						A_DxtInformationList[0].set('relationId', DataObjArr['rsMainkeyID'])

						A_DxtInformationList[0].save()
					else:
						A_DxtInformation = leancloud.Object.extend('A_DxtInformation')
						A_DxtInformationObj = A_DxtInformation()

						A_DxtInformationObj.set('sync', 3)

						A_DxtInformationObj.set('title', DataObjArr['AttachTitle'])
						A_DxtInformationObj.set('source', "")
						A_DxtInformationObj.set('summary', "")  ##content
						A_DxtInformationObj.set('thumbnail', DataObjArr["OtherDefine8"])
						A_DxtInformationObj.set('url', DataObjArr['OtherDefine4'])
						A_DxtInformationObj.set('content', DataObjArr['AttachContent'])
						A_DxtInformationObj.set('srcContent', DataObjArr['AttachContent'])

						if int(DataObjArr['RemarkClass']) in label:
							RemarkClass = int(DataObjArr['RemarkClass'])
							tmp = []
							tmp.append(label[RemarkClass])
							A_DxtInformationObj.set('categories', tmp)
							A_DxtInformationObj.set('labels', tmp)

						A_DxtInformationObj.set('isDisable', isDisable)

						A_DxtInformationObj.set('author', DataObjArr['RemarkMan'])
						A_DxtInformationObj.set('publishTime', RemarkTime)
						A_DxtInformationObj.set('clickNumber', 0)
						A_DxtInformationObj.set('likeNumber', 0)
						A_DxtInformationObj.set('shareNumber', 0)
						A_DxtInformationObj.set('collectNumber', 0)
						A_DxtInformationObj.set('relationId', DataObjArr['rsMainkeyID'])

						A_DxtInformationObj.save()

				except Exception, e:
					logging.error("钱坤晨会更新失败: %s" % DataObjArr)


		else:
			logging.warning("提交模拟炒股系统钱坤晨会数据返回失败：%s" %sirsReportRemarkMC)

if __name__ == "__main__":

	sirsReportRemark_object = sirsReportRemark()

	sirsReportRemark_object.sirsReportRemarkPort()
	sirsReportRemark_object.sirsReportRemarkMC()

