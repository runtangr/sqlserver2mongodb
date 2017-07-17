#encoding=utf-8

'''
Modified on June 27, 2017

@author: tangr
'''

 #王中王投资列表

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

class WZWInvest:
    def WZWInvestPort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        SyncControl = leancloud.Object.extend('SyncControl')
        self.SyncControlObj = SyncControl()
        querySyncInfo = SyncControl.query

        querySyncInfo.equal_to('type', 'WZWInvest')
        syncObj = querySyncInfo.find()
        if len(syncObj)== 0:
            dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
            self.SyncControlObj.set("type","WZWInvest")
            self.SyncControlObj.set("mainKeyId",0)
            self.SyncControlObj.set("rsDateTime","1990-01-01")
            self.SyncControlObj.save()

        self.SyncControlObj = querySyncInfo.first()
        self.maxKeyId = int(self.SyncControlObj.get('mainKeyId'))
        self.rsDateTime = self.SyncControlObj.get('rsDateTime')
        top = 100

        # 王中王投资列表 WebService 测试接口P_Z_uimsVSTSCD_pro
        response = client.service.P_Z_uimsVSTSCD_pro(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                rsMainkeyID=self.maxKeyId,
                                                rsDateTime=self.rsDateTime,
                                                  top=top
                                                    )
        try:
            self.WZWInvest = json.loads(response)

        except Exception, e:
            logging.error("%s  webservice 接口数据获取失败 %s" %(__file__ ,response))

    def WZWInvestMC(self):
        '''
        mc更新 A_DxtWZWInvest(王中王投资列表)表
        '''

        maxKeyId = int(self.SyncControlObj.get('mainKeyId'))

        if self.WZWInvest["Code"] == 0:

            self.DataObj =  json.loads(self.WZWInvest["DataObj"])#


            map(self.DealData,self.DataObj)


        else:
             logging.warning("提交王中王投资列表数据返回失败：%s" %self.WZWInvest)

    def DealData(self,DataObjArr):

        #最后一条数据赋值
        if DataObjArr==self.DataObj[-1]:
            self.maxKeyId = int(DataObjArr['rsmainkeyid'])
            self.rsDateTime = DataObjArr['rsDateTime']
            self.SyncControlObj.set('mainKeyId', self.maxKeyId)
            self.SyncControlObj.set('rsDateTime', self.rsDateTime)
            self.SyncControlObj.save()

        #打印
        print ("maxKeyId:", self.maxKeyId, "===", "rsMainkeyID:", DataObjArr['rsmainkeyid'], "===",
               "rsDateTime:", DataObjArr['rsDateTime'])

        #数据处理
        #时间格式处理
        self.wtTime = datetime.strptime(DataObjArr["wtTime"],'%Y-%m-%d %H:%M:%S')
        self.dealTime = datetime.strptime(DataObjArr["CJDate"], '%Y-%m-%d %H:%M:%S')
        style = {
            -1: "卖",
            1: "买",
            20: "分红",
            30: "送股"
        }
        # 买卖
        if type(DataObjArr["TransStyle"])==int:
            self.TransStyle = style[DataObjArr["TransStyle"]]
        else:
            self.TransStyle = DataObjArr["TransStyle"]

        A_DxtWZWInvestQuery = leancloud.Query('A_DxtWZWInvest')
        A_DxtWZWInvestQuery.equal_to('relationId', DataObjArr['rsmainkeyid'])
        self.A_DxtWZWInvestList = A_DxtWZWInvestQuery.find()

        # 查找A_DxtWZWTeacher VGroupID，取出teacherObjectId
        A_DxtWZWTeacherQuery = leancloud.Query('A_DxtWZWTeacher')
        A_DxtWZWTeacherQuery.equal_to('groupBmId', DataObjArr["VGroupID"])
        self.A_DxtWZWTeacherList = A_DxtWZWTeacherQuery.find()
        # 编辑
        if len(self.A_DxtWZWInvestList) > 0 and len(self.A_DxtWZWTeacherList)>0:

            self.Save(self.A_DxtWZWInvestList[0],DataObjArr)
        elif len(self.A_DxtWZWTeacherList)>0:
            A_DxtWZWInvest = leancloud.Object.extend('A_DxtWZWInvest')
            A_DxtWZWInvestObj = A_DxtWZWInvest()
            self.Save(A_DxtWZWInvestObj,DataObjArr)

    def Save(self,Obj,DataObjArr):
        Obj.set('groupBmId', DataObjArr['VGroupID'])
        Obj.set('teacherObjectId', self.A_DxtWZWTeacherList[0].get("objectId"))
        Obj.set('stockCode', DataObjArr['stockcode'])
        Obj.set('stockName', DataObjArr['stockshortName'])
        Obj.set('marketCode', DataObjArr["MarketCode"])

        Obj.set('cjje',DataObjArr["cjje"] )
        Obj.set('price', DataObjArr["price"])
        Obj.set('syl', DataObjArr["syl"])

        Obj.set('volume', DataObjArr['volume'])
        Obj.set('profitorLoss', DataObjArr['profitorLoss'])
        Obj.set('transType', self.TransStyle)
        Obj.set('wtTime', self.wtTime)
        Obj.set('dealTime',  self.dealTime)

        Obj.set('relationId', DataObjArr['rsmainkeyid'])
        Obj.save()

if __name__ == "__main__":

	WZWInvest_object = WZWInvest()

	WZWInvest_object.WZWInvestPort()
	WZWInvest_object.WZWInvestMC()

