#encoding=utf-8

'''
Modified on June 5, 2017

@author: tangr
'''
 #模拟炒股
 #排名数据同步

import unittest
from suds.client import Client
import json
from datetime import datetime
import time
from core import leancloud_patch
import leancloud
from core.Utils import init_leancloud_client

init_leancloud_client()

class Range:
    def RangePort(self):
        '''
        获取端口数据
        '''
        url = "http://180.169.122.18:8091/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

		#设置当前时间请求
        dataTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        # 排名数据同步 WebService 测试接口Query_uimsSYPM
        response = client.service.Query_uimsSYPM(Coordinates='021525374658617185',
												 Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
												 rsMainkeyID=0,
												 rsDatetime = dataTime,
												 flg=0
												 )
        self.data = json.loads(response)

    def RangeMC(self):
		'''
		mc更新AnalogRange(成交明细)表
		'''
		RangeMC = self.data
		AnalogRange = leancloud.Object.extend('AnalogRange')
		RangeObj = AnalogRange()
		queryRange = AnalogRange.query

		AnalogMyMatch = leancloud.Object.extend('AnalogMyMatch')
		queryMyMatch = AnalogMyMatch.query

		if RangeMC["Code"] == 0:

			DataObj =  json.loads(RangeMC["DataObj"])#

			#先删除原有数据
			query_list = queryRange.find()
			AnalogRange.destroy_all(query_list)

			userObjectId = ''
			headImageUrl = ''


			for DataObjArr in DataObj:

				#添加userObjectId和 头像headImageUrl
				queryMyMatch.equal_to('groupBmId', DataObjArr['vgroupid'])
				myMatchObj_list = queryMyMatch.find()
				for myMatchObj in myMatchObj_list:
					userObjectId = myMatchObj.get("userObjectId")
					headImageUrl = myMatchObj.get("headImageUrl")

				RangeObj.set('userObjectId', userObjectId)
				RangeObj.set('headImageUrl', headImageUrl)

				RangeObj.set('pm',DataObjArr['pm'])
				RangeObj.set('type',DataObjArr['pmType'])
				RangeObj.set('groupBmId',DataObjArr['vgroupid'])
				RangeObj.set('groupBm',DataObjArr['groupbm'])
				RangeObj.set('userName',DataObjArr['groupbm'])
				RangeObj.set('syl',DataObjArr['ror']+'%')
				RangeObj.set('shouYiLv', float(DataObjArr['ror']))
				RangeObj.set('totalCapital',DataObjArr['EndCaptial'])
				RangeObj.set('originalCapital',DataObjArr['OriginalCapital'])
				RangeObj.set('djs',DataObjArr['djs'])
				RangeObj.set('cw',DataObjArr['cw'])
				RangeObj.set('cgl',DataObjArr['cgl'])
				RangeObj.save()
		else:
			print("提交模拟炒股系统查询日收益排名返回失败：",RangeMC["DataObj"])




if __name__ == "__main__":

	Range_object = Range()

	Range_object.RangePort()
	Range_object.RangeMC()

