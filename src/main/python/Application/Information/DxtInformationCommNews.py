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
		url = "http://10.30.0.122:8093/Stocks.asmx?WSDL"
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
			AnalogSyncInfoObj.set("rsDateTime", "2004-02-02")
			AnalogSyncInfoObj.save()

		syncObj = querySyncInfo.first()
		maxKeyId = int(syncObj.get('mainKeyId'))
		rsDateTime = syncObj.get('rsDateTime')
		top = 1000

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

				if DataObjArr['rsMainkeyID'] > maxKeyId:
					isChange = 1
					maxKeyId = DataObjArr['rsMainkeyID']
					rsDateTime = DataObjArr['rsDateTime']

				print ("maxKeyId:",maxKeyId, "===","rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
					 "rsDateTime:",DataObjArr['rsDateTime'])


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




					A_DxtInformationObj.set('title', DataObjArr['NewsTitle'])
					A_DxtInformationObj.set('source', DataObjArr['NewsSource'])
					A_DxtInformationObj.set('summary', DataObjArr['NewsBrief'])
					A_DxtInformationObj.set('thumbnail', DataObjArr['OtherDefine1'])
					A_DxtInformationObj.set('url', DataObjArr['OtherDefine4'])
					A_DxtInformationObj.set('content', DataObjArr['NewsContent'])
					A_DxtInformationObj.set('srcContent', DataObjArr['NewsSource'])

					if DataObjArr['NewsStyle'] in label:
						NewsStyle = DataObjArr['NewsStyle']
						A_DxtInformationObj.set('categories', label[NewsStyle])
						A_DxtInformationObj.set('labels', label[NewsStyle])

					A_DxtInformationObj.set('isDisable', DataObjArr['rsStatus'])  #-1 wei  jingyong
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
					A_DxtInformationObj.set('publishTime', DataObjArr['NewsDate'])
					A_DxtInformationObj.set('clickNumber', "")
					A_DxtInformationObj.set('likeNumber', "")
					A_DxtInformationObj.set('shareNumber', "")
					A_DxtInformationObj.set('collectNumber', "")
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

