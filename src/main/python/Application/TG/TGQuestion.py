#encoding=utf-8

'''
Modified on June 8, 2017

@author: tangr
'''

 #问股列表

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

class Teacher:
	def TeacherPort(self):
		'''
		获取端口数据
		'''
		url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
		client = Client(url)
		# print (client)

		AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
		self.AnalogSyncInfoObj = AnalogSyncInfo()
		querySyncInfo = AnalogSyncInfo.query

		querySyncInfo.equal_to('type', 'TGQuestion')
		syncObj = querySyncInfo.find()
		if len(syncObj) == 0:

			self.AnalogSyncInfoObj.set("type", "TGQuestion")
			self.AnalogSyncInfoObj.set("mainKeyId", 0)
			self.AnalogSyncInfoObj.set("rsDateTime", "1990-01-01")
			self.AnalogSyncInfoObj.save()

		self.AnalogSyncInfoObj = querySyncInfo.first()
		self.maxKeyId = int(self.AnalogSyncInfoObj.get('mainKeyId'))
		self.rsDateTime = self.AnalogSyncInfoObj.get('rsDateTime')
		top = 100

		# 问股列表 WebService 测试接口P_SynCommAskOnline
		response = client.service.P_SynCommAskOnline(
													Coordinates='021525374658617185',
													Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
													rsMainkeyID=self.maxKeyId,
													rsDateTime=self.rsDateTime,
													top=top
													)
		self.data = json.loads(response)

	def TeacherMC(self):
		'''
		mc更新A_DxtTGQuestion(问股列表)表
		'''
		TeacherMC = self.data


		if TeacherMC["Code"] == 0:

			DataObj =  json.loads(TeacherMC["DataObj"])#

			for DataObjArr in DataObj:

				# 最后一条数据赋值
				if DataObjArr == DataObj[-1]:
					self.maxKeyId = int(DataObjArr['rsMainkeyID'])
					self.rsDateTime = DataObjArr['rsDateTime']
					self.AnalogSyncInfoObj.set('mainKeyId', self.maxKeyId)
					self.AnalogSyncInfoObj.set('rsDateTime', self.rsDateTime)
					self.AnalogSyncInfoObj.save()

				# 打印
				print ("maxKeyId:", self.maxKeyId, "===", "rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
					   "rsDateTime:", DataObjArr['rsDateTime'])

				#时间转换
				questionTime = datetime.strptime(DataObjArr['AskDateTime'], '%Y-%m-%d %H:%M:%S')
				answerTime = datetime.strptime(DataObjArr['AnsDateTime'], '%Y-%m-%d %H:%M:%S')

				try:
					A_DxtTGQuestionQuery = leancloud.Query('A_DxtTGQuestion')
					A_DxtTGQuestionQuery.equal_to('relationId', DataObjArr['rsMainkeyID'])
					count = A_DxtTGQuestionQuery.count()

					#编辑
					if count >0:
						A_DxtTGQuestionObj = A_DxtTGQuestionQuery.first()
						A_DxtTGQuestionObj.set('userObjectId', DataObjArr['UserId'])
						A_DxtTGQuestionObj.set('userNickName', DataObjArr['OtherIM'])
						A_DxtTGQuestionObj.set('userPhoto', DataObjArr['UserPhoto'])
						A_DxtTGQuestionObj.set('question', DataObjArr['AskContent'])
						A_DxtTGQuestionObj.set('answer', DataObjArr["AnsContent"])
						A_DxtTGQuestionObj.set('questionTime',questionTime )
						A_DxtTGQuestionObj.set('answerTime', answerTime)

						A_DxtTGQuestionObj.save()
					#新增
					else:
						A_DxtTGQuestion = leancloud.Object.extend('A_DxtTGQuestion')
						A_DxtTGQuestionObj = A_DxtTGQuestion()

						A_DxtTGQuestionObj.set('userObjectId', DataObjArr['UserId'])
						A_DxtTGQuestionObj.set('userNickName', DataObjArr['OtherIM'])
						A_DxtTGQuestionObj.set('userPhoto', DataObjArr['UserPhoto'])
						A_DxtTGQuestionObj.set('question', DataObjArr['AskContent'])
						A_DxtTGQuestionObj.set('answer', DataObjArr["AnsContent"])
						A_DxtTGQuestionObj.set('questionTime', questionTime)
						A_DxtTGQuestionObj.set('answerTime', answerTime)
						A_DxtTGQuestionObj.set('relationId', DataObjArr['rsMainkeyID'])

						A_DxtTGQuestionObj.save()
				except Exception, e:
					logging.error("投顾老师数据更新失败: %s" % DataObjArr)
		else:
			logging.warning("提交模拟炒股系统投顾老师数据返回失败：%s" %TeacherMC)

if __name__ == "__main__":

	Teacher_object = Teacher()

	Teacher_object.TeacherPort()
	Teacher_object.TeacherMC()

