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

class CommNewsEdit:
	def CommNewsEditPort(self):
		'''
		获取端口数据
		'''
		url = "http://61.139.76.139:9527/Stocks.asmx?WSDL"
		client = Client(url)
		# print (client)

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		AnalogSyncInfoObj = AnalogSyncInfo()
		querySyncInfo = AnalogSyncInfo.query

		querySyncInfo.equal_to('type', 'CommNews')
		count = querySyncInfo.count()
		if count == 0:
			dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
			AnalogSyncInfoObj.set("type", "CommNews")
			AnalogSyncInfoObj.set("mainKeyId", 0)
			AnalogSyncInfoObj.set("rsDateTime", "1990-01-01")
			AnalogSyncInfoObj.save()

		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))
		rsDateTime = syncObj.get('rsDateTime')
		top = 10

		# 自主新闻 WebService 测试接口Query_CommNews_EDIT
		response = client.service.Query_CommNews_EDIT(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												 rsMainkeyid=maxKeyId,
												 rsDatetime=rsDateTime,
												 top=top
													)

		self.CommNews_EDIT = json.loads(response)

	def CommNewsEditMC(self):
		'''
		mc更新 A_DxtInformation 资讯栏目更新表
		'''
		CommNewsEditMC = self.CommNews_EDIT
		isChange = 0

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		querySyncInfo = AnalogSyncInfo.query
		querySyncInfo.equal_to('type', 'CommNews')
		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))

		if CommNewsEditMC["Code"] == 0:

			DataObj =  json.loads(CommNewsEditMC["DataObj"])#

			#label
			label = { 21056:"大盘分析",
					 23790:"钱坤观点",
					 33310:"要闻点评",
					 24612:"今日热点",
					 23787:"午间解盘",
					 24762:"重大事件点评",
					 23788:"早盘风向标"	,
					 33312:"深入研究",
					 39866:"每日点评",
					 33311:"公司公告"}


			for DataObjArr in DataObj:

				if int(DataObjArr['rsMainkeyID']) > maxKeyId:
					isChange = 1
					maxKeyId = int(DataObjArr['rsMainkeyID'])
					rsDateTime = DataObjArr['rsDateTime']

				print ("maxKeyId:",maxKeyId, "===","rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
					 "rsDateTime:",DataObjArr['rsDateTime'])

				# 转换
				if DataObjArr['rsStatus'] > 0:
					isDisable = 0
				else:
					isDisable = 1


				NewsDate = datetime.strptime(DataObjArr['NewsDate'], '%Y-%m-%d %H:%M:%S')

				try:
					A_DxtInformation = leancloud.Object.extend('A_DxtInformation')
					A_DxtInformationObj = A_DxtInformation()

					A_DxtInformationObj.set('title', DataObjArr['NewsTitle'])
					A_DxtInformationObj.set('source', DataObjArr['OtherDefine2'])
					A_DxtInformationObj.set('summary', DataObjArr['NewsBrief'])
					A_DxtInformationObj.set('thumbnail', DataObjArr['OtherDefine1'])
					A_DxtInformationObj.set('url', DataObjArr['OtherDefine4'])
					A_DxtInformationObj.set('content', DataObjArr['NewsContent'])
					A_DxtInformationObj.set('srcContent', DataObjArr['NewsContent'])

					if int(DataObjArr['NewsStyle']) in label:
						NewsStyle = int(DataObjArr['NewsStyle'])
						tmp =[]
						tmp.append(label[NewsStyle])
						A_DxtInformationObj.set('categories', tmp)
						A_DxtInformationObj.set('labels', tmp)

					A_DxtInformationObj.set('isDisable', isDisable)
					# correlatedStocks =[]
					# Stocks_dict = {'code':'','name':'','market':''}
					# if  DataObjArr['xggg']!=None:
					# 	pattern_data = re.split("、",DataObjArr['xggg'])
					#     for pattern_list in pattern_data:
					# 		    Stocks_dict['code'] = re.search("\d+",pattern_list)
					# 	        if
					# 	        	Stocks_dict['name'] = pattern_name.search(DataObjArr['xggg'])
					# 			else:
					# 				Stocks_dict['name'] = DataObjArr['xggg']
                    #
					# 				correlatedStocks.append(Stocks_dict)
                    #
					# A_DxtInformationObj.set('correlatedStocks', correlatedStocks)


					A_DxtInformationObj.set('author', DataObjArr['OtherDefine2'])
					A_DxtInformationObj.set('publishTime', NewsDate)
					A_DxtInformationObj.set('clickNumber', 0)
					A_DxtInformationObj.set('likeNumber', 0)
					A_DxtInformationObj.set('shareNumber', 0)
					A_DxtInformationObj.set('collectNumber', 0)
					A_DxtInformationObj.set('relationId', DataObjArr['rsMainkeyID'])

					A_DxtInformationObj.save()
				except Exception, e:
					logging.error("资讯表 自主新闻数据更新失败: %s" % DataObjArr)

			if isChange == 1:
				syncObj.set('mainKeyId', maxKeyId)
				syncObj.set('rsDateTime', rsDateTime)
				syncObj.save()

		else:
			logging.warning("提交模拟炒股系统资讯表 自主新闻数据返回失败：%s" %CommNewsEditMC)

if __name__ == "__main__":

	CommNewsEdit_object = CommNewsEdit()

	CommNewsEdit_object.CommNewsEditPort()
	CommNewsEdit_object.CommNewsEditMC()

