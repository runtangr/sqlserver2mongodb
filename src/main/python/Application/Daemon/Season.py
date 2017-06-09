#encoding=utf-8

'''
Modified on June 8, 2017

@author: tangr
'''
 #模拟炒股
 #赛季同步

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

class Season:
    def SeasonPort(self):
        '''
        获取端口数据
        '''
        url = "http://180.169.122.18:8091/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        # 设置当前时间请求
        dataTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 赛季同步 WebService 测试接口Query_uimsSEASONSET
        response = client.service.Query_uimsSEASONSET(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												 rsMainkeyid=0,
												 # rsDatetime="2004-02-02 0:0:0"
												 rsDatetime=dataTime
																  )
        self.data = json.loads(response)

    def SeasonMC(self):
		'''
		mc更新uimsSeasonSet(赛季同步)表
		'''
		SeasonMC = self.data

		if SeasonMC["Code"] == 0:

			DataObj =  json.loads(SeasonMC["DataObj"])#

			for DataObjArr in DataObj:
				try:
					uimsSeasonSet = leancloud.Object.extend('uimsSeasonSet')
					uimsSeasonSetObj = uimsSeasonSet()

					uimsSeasonSetObj.set('rsOperateID', str(DataObjArr['rsOperateID']))
					uimsSeasonSetObj.set('rsStatus', str(DataObjArr['rsStatus']))
					uimsSeasonSetObj.set('rsProjectId', str(DataObjArr['rsProjectId']))
					uimsSeasonSetObj.set('rsMainkeyID', DataObjArr['rsMainkeyID'])
					uimsSeasonSetObj.set('rsDateTime', DataObjArr['rsDateTime'])
					uimsSeasonSetObj.set('rsDispIndex', str(DataObjArr['rsDispIndex']))
					uimsSeasonSetObj.set('SeasonId', str(DataObjArr['SeasonId']))
					uimsSeasonSetObj.set('GroupStyle', str(DataObjArr['GroupStyle']))
					uimsSeasonSetObj.set('StartDate',   datetime.strptime(DataObjArr["StartDate"],"%Y-%m-%d %H:%M:%S"))
					uimsSeasonSetObj.set('EndDate',datetime.strptime(DataObjArr["EndDate"],"%Y-%m-%d %H:%M:%S"))
					uimsSeasonSetObj.save()
				except Exception, e:
					logging.error("赛季同步数据更新失败: %s" % DataObjArr)
		else:
			logging.warning("提交模拟炒股系统赛季同步数据返回失败：%s" % SeasonMC)

if __name__ == "__main__":

	Season_object = Season()

	Season_object.SeasonPort()
	Season_object.SeasonMC()

