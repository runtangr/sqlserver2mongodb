#encoding=utf-8

'''
Modified on June 8, 2017

@author: tangr
'''
 #模拟炒股
 #牛股榜同步

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

class NiuguList:
    def NiuguListPort(self):
        '''
        获取端口数据
        '''
        url = "http://10.30.0.122:8091/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        # 牛股榜 WebService 测试接口Query_uimsNGB
        response = client.service.Query_uimsNGB(Coordinates='021525374658617185',
												Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
																  )
        self.data = json.loads(response)

    def NiuguListMC(self):
		'''
		mc更新uimsLSPM(牛股榜)表
		'''
		NiuguListMC = self.data

		if NiuguListMC["Code"] == 0:

			DataObj =  json.loads(NiuguListMC["DataObj"])#

			for DataObjArr in DataObj:
				uimsNGB_query = leancloud.Query('uimsNGB')

				uimsNGB_query.equal_to('rsMainkeyID',DataObjArr['rsMainkeyID'])
				countTmp = uimsNGB_query.count()
				try:
					if countTmp > 0:

						ngbObjTmp = uimsNGB_query.first()
						ngbObjTmp.set('rsOperateID', str(DataObjArr['rsOperateID']))
						ngbObjTmp.set('rsStatus', str(DataObjArr['rsStatus']))
						ngbObjTmp.set('rsProjectId', str(DataObjArr['rsProjectId']))
						ngbObjTmp.set('rsDateTime', DataObjArr['rsDateTime'])
						ngbObjTmp.set('rsDispIndex', str(DataObjArr['rsDispIndex']))
						ngbObjTmp.set('stockShortname', DataObjArr['stockShortname'])
						ngbObjTmp.set('ownerCount', int(DataObjArr['ownerCount']))
						ngbObjTmp.set('avgPrize', str(DataObjArr['avgPrize']))
						ngbObjTmp.set('groupbm', DataObjArr['groupbm'])
						ngbObjTmp.set('StockCode', DataObjArr['StockCode'])
						ngbObjTmp.set('Stockid', str(DataObjArr['Stockid']))
						ngbObjTmp.save()

					else:
						uimsNGB = leancloud.Object.extend('uimsNGB')
						uimsNGBObj = uimsNGB()

						uimsNGBObj.set('rsOperateID', str(DataObjArr['rsOperateID']))
						uimsNGBObj.set('rsStatus', str(DataObjArr['rsStatus']))
						uimsNGBObj.set('rsProjectId', str(DataObjArr['rsProjectId']))
						uimsNGBObj.set('rsMainkeyID', DataObjArr['rsMainkeyID'])
						uimsNGBObj.set('rsDateTime', DataObjArr['rsDateTime'])
						uimsNGBObj.set('rsDispIndex', str(DataObjArr['rsDispIndex']))
						uimsNGBObj.set('stockShortname', DataObjArr['stockShortname'])
						uimsNGBObj.set('ownerCount', int(DataObjArr['ownerCount']))
						uimsNGBObj.set('avgPrize', str(DataObjArr['avgPrize']))
						uimsNGBObj.set('groupbm', DataObjArr['groupbm'])
						uimsNGBObj.set('StockCode', DataObjArr['StockCode'])
						uimsNGBObj.set('Stockid', str(DataObjArr['Stockid']))
						uimsNGBObj.save()
				except Exception, e:
					logging.error("牛股榜数据更新失败: %s" % DataObjArr)
		else:
			logging.warning("提交模拟炒股系统牛股榜数据返回失败：%s" %NiuguListMC)

if __name__ == "__main__":

	NiuguList_object = NiuguList()

	NiuguList_object.NiuguListPort()
	NiuguList_object.NiuguListMC()

