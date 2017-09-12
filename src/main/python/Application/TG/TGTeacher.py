#encoding=utf-8

'''
Modified on June 8, 2017

@author: tangr
'''

 #投顾老师

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

		# 专家点评 WebService 测试接口AppTeacherMessage
		response = client.service.AppTeacherMessage(
															Coordinates='021525374658617185',
															Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A'
															)
		self.data = json.loads(response)

	def TeacherMC(self):
		'''
		mc更新uimsZJDP(历史排名)表
		'''
		TeacherMC = self.data
		isChange = 0

		if TeacherMC["Code"] == 0:

			DataObj =  json.loads(TeacherMC["DataObj"])#

			for DataObjArr in DataObj:

				try:
					A_DxtTGTeacherQuery = leancloud.Query('A_DxtTGTeacher')
					A_DxtTGTeacherQuery.equal_to('relationId', DataObjArr['TeacherUserid'])
					count = A_DxtTGTeacherQuery.count()
					#编辑
					if count >0:
						A_DxtTGTeacherObj = A_DxtTGTeacherQuery.first()
						A_DxtTGTeacherObj.set('photo', DataObjArr['UserPhoto'])
						A_DxtTGTeacherObj.set('name', DataObjArr['NickName'])
						A_DxtTGTeacherObj.set('sn', DataObjArr['zsbh'])
						A_DxtTGTeacherObj.set('snType', DataObjArr['zslx'])
						A_DxtTGTeacherObj.save()
					#新增
					else:
						A_DxtTGTeacher = leancloud.Object.extend('A_DxtTGTeacher')
						A_DxtTGTeacherObj = A_DxtTGTeacher()
						A_DxtTGTeacherObj.set('name', DataObjArr['NickName'])
						A_DxtTGTeacherObj.set('photo', DataObjArr['UserPhoto'])
						A_DxtTGTeacherObj.set('relationId', DataObjArr['TeacherUserid'])
						A_DxtTGTeacherObj.set('sn', DataObjArr['zsbh'])
						A_DxtTGTeacherObj.set('snType', DataObjArr['zslx'])

						A_DxtTGTeacherObj.set('title', "")
						A_DxtTGTeacherObj.set('desc', "")
						A_DxtTGTeacherObj.set('tel', "")
						A_DxtTGTeacherObj.set('isTop', 0)
						A_DxtTGTeacherObj.set('order', 0)

						A_DxtTGTeacherObj.save()
				except Exception, e:
					logging.error("投顾老师数据更新失败: %s" % DataObjArr)
		else:
			logging.warning("提交模拟炒股系统投顾老师数据返回失败：%s" %TeacherMC)

if __name__ == "__main__":

	Teacher_object = Teacher()

	Teacher_object.TeacherPort()
	Teacher_object.TeacherMC()

