#encoding=utf-8

'''
Modified on June 27, 2017

@author: tangr
'''

 #专家投顾

import unittest
from suds.client import Client
import json
from datetime import datetime
import time
import leancloud_patch
import leancloud
from Utils import init_leancloud_client
import logging
import MarketData

logging.basicConfig(level=logging.WARNING,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S'
					)

init_leancloud_client()

class TGExpert:
    def TGExpertPort(self):
        '''
        获取端口数据
        '''
        url = "http://61.139.76.139:9527/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)



        # 专家投顾 WebService 测试接口 P_CX_uimsTZTD
        response = client.service.P_CX_uimsTZTD(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',

                                                    )
        try:
            self.TGExpert = json.loads(response)

        except Exception, e:
            logging.error("%s  webservice 接口数据获取失败 %s" %(__file__ ,response))

    def TGExpertMC(self):
        '''
        mc更新 A_DxtTGExpert(专家投顾)表
        '''

        if self.TGExpert["Code"] == 0:

            # 先删除原有数据
            queryTGExpert = leancloud.Query('A_DxtTGExpert')
            query_list = queryTGExpert.find()
            leancloud.Object.destroy_all(query_list)

            self.DataObj =  json.loads(self.TGExpert["DataObj"])#


            map(self.DealData,self.DataObj)


        else:
             logging.warning("提交专家投顾数据返回失败：%s" %self.TGExpert)

    def DealData(self,DataObjArr):

        #数据处理
        A_DxtTGExpert = leancloud.Object.extend('A_DxtTGExpert')
        A_DxtTGExpertObj = A_DxtTGExpert()
        self.Save(A_DxtTGExpertObj,DataObjArr)

    def Save(self,Obj,DataObjArr):
        Obj.set('name', DataObjArr['gw_Name'])
        Obj.set('photo', DataObjArr["gw_Image"])
        Obj.set('title', DataObjArr['gw_ZJTX'])
        Obj.set('sn', DataObjArr['gw_ZYZH'])
        Obj.set('desc', DataObjArr["gw_Content"])

        Obj.set('tel',"")
        Obj.set('type', 0)
        Obj.save()

if __name__ == "__main__":

	TGExpert_object = TGExpert()

	TGExpert_object.TGExpertPort()
	TGExpert_object.TGExpertMC()

