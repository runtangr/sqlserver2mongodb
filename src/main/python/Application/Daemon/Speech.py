#encoding=utf-8

'''
Modified on June 8, 2017

@author: tangr
'''
 #模拟炒股
 #获奖感言同步

import unittest
from suds.client import Client
import json
from datetime import datetime
import time
from core import leancloud_patch
import leancloud
from core.Utils import init_leancloud_client
import logging

logging.basicConfig(level=logging.WARNING,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S'
					)

init_leancloud_client()

class Speech:
    def SpeechPort(self):
        '''
        获取端口数据
        '''
        url = "http://180.169.122.18:8091/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        # 设置当前时间请求
        dataTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 获奖感言 WebService 测试接口Query_uimsHJGY
        response = client.service.Query_uimsHJGY(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												rsMainkeyID=0,
												# rsDatetime="2004-02-02 0:0:0",
												rsDatetime= dataTime,
												flg=0
												 )
        self.data = json.loads(response)

    def SpeechMC(self):
		'''
		mc更新uimsHJGY(获奖感言)表
		'''
		SpeechMC = self.data

		if SpeechMC["Code"] == 0:

			DataObj =  json.loads(SpeechMC["DataObj"])#

			for DataObjArr in DataObj:
				try:
					uimsHJGY = leancloud.Object.extend('uimsHJGY')
					uimsHJGYObj = uimsHJGY()

					uimsHJGYObj.set('BlogAddress', DataObjArr['BlogAddress'])
					uimsHJGYObj.set('rsMainkeyID', DataObjArr['rsMainkeyID'])
					uimsHJGYObj.set('Ror', str(DataObjArr['Ror']))
					uimsHJGYObj.set('rsOperateID', str(DataObjArr['rsOperateID']))
					uimsHJGYObj.set('rsStatus', str(DataObjArr['rsStatus']))
					uimsHJGYObj.set('shouyi', DataObjArr['shouyi'])
					uimsHJGYObj.set('rsProjectId', str(DataObjArr['rsProjectId']))
					uimsHJGYObj.set('PlatForms', DataObjArr['PlatForms'])
					uimsHJGYObj.set('FbTime', DataObjArr['FbTime'])
					uimsHJGYObj.set('ZhName', DataObjArr['ZhName'])
					uimsHJGYObj.set('VGroupId', str(DataObjArr['VGroupId']))
					uimsHJGYObj.set('rsDateTime', DataObjArr['rsDateTime'])
					uimsHJGYObj.set('rsDispIndex', str(DataObjArr['rsDispIndex']))
					uimsHJGYObj.set('Picture', DataObjArr['Picture'])
					uimsHJGYObj.save()
				except Exception, e:
					logging.error("获奖感言数据更新失败: %s" % DataObjArr)
		else:
			logging.warning("提交模拟炒股系统获奖感言数据返回失败：%s" %SpeechMC)

if __name__ == "__main__":

	Speech_object = Speech()

	Speech_object.SpeechPort()
	Speech_object.SpeechMC()

