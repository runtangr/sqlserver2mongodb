#encoding=utf-8

'''
Modified on June 8, 2017

@author: tangr
'''
 #模拟炒股
 #专家点评同步

import unittest
from suds.client import Client
import json
from datetime import datetime
import time
from core import leancloud_patch
import leancloud
from core.Utils import init_leancloud_client

init_leancloud_client()

class Comment:
    def CommentPort(self):
        '''
        获取端口数据
        '''
        url = "http://180.169.122.18:8091/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        # 设置当前时间请求
        dataTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 专家点评 WebService 测试接口Query_uimsZJDP
        response = client.service.Query_uimsZJDP(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												 rsMainkeyid=0,
												 # rsDatetime="2004-02-02 0:0:0"
												 rsDatetime=dataTime
																  )
        self.data = json.loads(response)

    def CommentMC(self):
		'''
		mc更新uimsLSPM(历史排名)表
		'''
		CommentMC = self.data
		uimsZJDP = leancloud.Object.extend('uimsZJDP')
		uimsZJDPObj = uimsZJDP()
		uimsZJDP_query = uimsZJDP.query

		uimsZJDP_query.add_ascending('rsMainkeyID')
		count = uimsZJDP_query.count()
		# if count > 0:
		# zjdpObj = uimsZJDP_query.first()
		# 	mainKeyId = int(zjdpObj.get('rsMainkeyID'))
		# else:
		# 	mainKeyId = 0

		if CommentMC["Code"] == 0:

			DataObj =  json.loads(CommentMC["DataObj"])#

			for DataObjArr in DataObj:

				uimsZJDPObj.set('rsOperateID', str(DataObjArr['rsOperateID']))
				uimsZJDPObj.set('rsStatus', str(DataObjArr['rsStatus']))
				uimsZJDPObj.set('rsProjectId', str(DataObjArr['rsProjectId']))
				uimsZJDPObj.set('getedPer', str(DataObjArr['getedPer']))
				uimsZJDPObj.set('rsMainkeyID', DataObjArr['rsMainkeyID'])
				uimsZJDPObj.set('pm', str(DataObjArr['pm']))
				uimsZJDPObj.set('groupbm', DataObjArr['groupbm'])
				uimsZJDPObj.set('JudgeContent', DataObjArr['JudgeContent'])
				uimsZJDPObj.set('rsDateTime', DataObjArr['rsDateTime'])
				uimsZJDPObj.set('rsDispIndex', str(DataObjArr['rsDispIndex']))
				uimsZJDPObj.set('TradeDate',  datetime.strptime(DataObjArr["TradeDate"],"%Y-%m-%d %H:%M:%S"))
				uimsZJDPObj.save()
				
						


if __name__ == "__main__":

	Comment_object = Comment()

	Comment_object.CommentPort()
	Comment_object.CommentMC()

