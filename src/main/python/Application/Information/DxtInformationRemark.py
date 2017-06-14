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
		url = "http://10.30.0.122:8093/Stocks.asmx?WSDL"
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
			AnalogSyncInfoObj.set("rsDateTime", "2004-02-02")
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

		self.sirsReportRemark = json.loads(response)

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

				if DataObjArr['rsMainkeyID'] > maxKeyId:
					isChange = 1
					maxKeyId = DataObjArr['rsMainkeyID']
					rsDateTime = DataObjArr['rsDateTime']

				print ("maxKeyId:", maxKeyId, "===", "rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
					   "rsDateTime:", DataObjArr['rsDateTime'])

				try:
					A_DxtInformation = leancloud.Object.extend('A_DxtInformation')
					A_DxtInformationObj = A_DxtInformation()
# news:
# |title|string|资讯标题|无|		1
# |source|string|资讯来源|无|
# |summary|string|资讯摘要|无|   0:content
# |thumbnail|string|缩略图url地址|无| 1
# |url|string|网页跳转地址|无| 1
# |content|string|处理过后的内容，填充为同步过来  1/srcContent
# |srcContent|string|源内容，填充为同步过来的原始 1
# |categories|array|渠道或类型，如为二级分类则用  1
# |labels|array|标签数组|无|   1/categories
# |isDisable |number|是否禁用 0不禁用 1禁用|0|
# |correlatedStocks|array|相关股票数组|无|
# |correlatedStocks.code|string|股票代码|无|
# |correlatedStocks.name|string|股票名称|无|
# |correlatedStocks.market|string|股票市场|无|
# |author|string|作者|无|  1
# |publishTime |datetime|发布时间| 无|   1
# |clickNumber |number|点击数|0|
# |likeNumber |number|好评数|0|
# |shareNumber |number|分享数|0|
# |collectNumber |number|收藏数|0|
# |relationId |string|同步系统关联ID| 无|  1




					A_DxtInformationObj.set('title', DataObjArr['AttachTitle'])
					A_DxtInformationObj.set('source', "")
					A_DxtInformationObj.set('summary', "")  ##content
					A_DxtInformationObj.set('thumbnail', DataObjArr["OtherDefine8"])
					A_DxtInformationObj.set('url', DataObjArr['OtherDefine4'])
					A_DxtInformationObj.set('content', DataObjArr['AttachContent'])
					A_DxtInformationObj.set('srcContent', DataObjArr['AttachContent'])

					if DataObjArr['RemarkClass'] in label:
						RemarkClass = DataObjArr['RemarkClass']
						A_DxtInformationObj.set('categories', label[RemarkClass])
						A_DxtInformationObj.set('labels', label[RemarkClass])

					A_DxtInformationObj.set('isDisable', DataObjArr['rsStatus'])  #-1 wei  jingyong


					# correlatedStocks =[]
					# Stocks_dict = {'code':'','name':'','market':''}
					# if  DataObjArr['xggg']!=None:
					# 	pattern_code = re.compile("\w")
					# 	Stocks_dict['code'] = pattern_code.search(DataObjArr['xggg'])
					# 	pattern_name = re.compile("、")
					# 	Stocks_dict['name'] = pattern_name.search(DataObjArr['xggg'])
					# 	correlatedStocks.append(Stocks_dict)
					# A_DxtInformationObj.set('correlatedStocks', correlatedStocks)


					A_DxtInformationObj.set('author', DataObjArr['RemarkMan'])
					A_DxtInformationObj.set('publishTime', DataObjArr['RemarkTime'])
					A_DxtInformationObj.set('clickNumber', "")
					A_DxtInformationObj.set('likeNumber', "")
					A_DxtInformationObj.set('shareNumber', "")
					A_DxtInformationObj.set('collectNumber', "")
					A_DxtInformationObj.set('relationId', DataObjArr['rsMainkeyID'])

					A_DxtInformationObj.save()
				except Exception, e:
					logging.error("钱坤晨会更新失败: %s" % DataObjArr)

			if isChange == 1:
				syncObj.set('mainKeyId', maxKeyId)
				syncObj.set('rsDateTime', rsDateTime)
				syncObj.save()

		else:
			logging.warning("提交模拟炒股系统钱坤晨会数据返回失败：%s" %sirsReportRemarkMC)

if __name__ == "__main__":

	sirsReportRemark_object = sirsReportRemark()

	sirsReportRemark_object.sirsReportRemarkPort()
	sirsReportRemark_object.sirsReportRemarkMC()

