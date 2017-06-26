#encoding=utf-8

'''
Modified on June 23, 2017

@author: tangr
'''

 #王中王老师列表

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

class WZWTeacher:
    def WZWTeacherPort(self):
        '''
        获取端口数据
        '''
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        AnalogSyncInfo = leancloud.Object.extend('AnalogSyncInfo')
        self.AnalogSyncInfoObj = AnalogSyncInfo()
        querySyncInfo = AnalogSyncInfo.query

        querySyncInfo.equal_to('type', 'WZWTeacher')
        syncObj = querySyncInfo.find()
        if len(syncObj)== 0:
            dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
            self.AnalogSyncInfoObj.set("type","WZWTeacher")
            self.AnalogSyncInfoObj.set("mainKeyId",0)
            self.AnalogSyncInfoObj.set("rsDateTime","1990-01-01")
            self.AnalogSyncInfoObj.save()

        self.AnalogSyncInfoObj = querySyncInfo.first()
        self.maxKeyId = int(self.AnalogSyncInfoObj.get('mainKeyId'))
        self.rsDateTime = self.AnalogSyncInfoObj.get('rsDateTime')
        top = 100

        # 王中王老师列表 WebService 测试接口P_Z_uimsVSTC_pro
        response = client.service.P_Z_uimsVSTC_pro(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                rsMainkeyID=self.maxKeyId,
                                                rsDateTime=self.rsDateTime,
                                                  top=top
                                                    )
        try:
            self.WZWTeacher = json.loads(response)

        except Exception, e:
            logging.error("%s  webservice 接口数据获取失败 %s" %(__file__ ,response))

    def WZWTeacherMC(self):
        '''
        mc更新 A_DxtWZWTeacher(王中王老师列表)表
        '''

        maxKeyId = int(self.AnalogSyncInfoObj.get('mainKeyId'))

        if self.WZWTeacher["Code"] == 0:

            self.DataObj =  json.loads(self.WZWTeacher["DataObj"])#


            map(self.DealData,self.DataObj)


        else:
             logging.warning("提交王中王老师列表数据返回失败：%s" %self.WZWTeacher)

    def DealData(self,DataObjArr):

        #最后一条数据赋值
        if DataObjArr==self.DataObj[-1]:
            self.maxKeyId = int(DataObjArr['rsMainkeyID'])
            self.rsDateTime = DataObjArr['rsDateTime']
            self.AnalogSyncInfoObj.set('mainKeyId', self.maxKeyId)
            self.AnalogSyncInfoObj.set('rsDateTime', self.rsDateTime)
            self.AnalogSyncInfoObj.save()

        #打印
        print ("maxKeyId:", self.maxKeyId, "===", "rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
               "rsDateTime:", DataObjArr['rsDateTime'])

        #数据处理
        # self.NewsDate = datetime.strptime(DataObjArr['NewsDate'][:-5],'%Y-%m-%d %H:%M:%S')
        # totalCapital = DataObjArr["ResidualCapital"] + DataObjArr["ResidualCapital"]

        A_DxtWZWTeacherStockQuery = leancloud.Query('A_DxtWZWTeacher')
        A_DxtWZWTeacherStockQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
        self.A_DxtWZWTeacherStockList = A_DxtWZWTeacherStockQuery.find()

        # #查找WZWTeacher 匹配name ，取出objectid
        # A_DxtWZWTeacherQuery = leancloud.Query('A_DxtWZWTeacher')
        # A_DxtWZWTeacherQuery.equal_to('name', self.StcokPool[DataObjArr["NewsStyle"]])
        # self.A_DxtWZWTeacherList = A_DxtWZWTeacherQuery.find()
        # 编辑
        if len(self.A_DxtWZWTeacherStockList) > 0:

            self.Save(self.A_DxtWZWTeacherStockList[0],DataObjArr)
        else:
            A_DxtWZWTeacherDiary = leancloud.Object.extend('A_DxtWZWTeacherDiary')
            A_DxtWZWTeacherDiaryObj = A_DxtWZWTeacherDiary()
            self.Save(A_DxtWZWTeacherDiaryObj,DataObjArr)

    def Save(self,Obj,DataObjArr):
        Obj.set('name', DataObjArr['OtherDefine4'])
        Obj.set('photo', DataObjArr['Timage'])
        Obj.set('groupBmId', DataObjArr['rsMainkeyID'])
        Obj.set('djs', DataObjArr['DJS'])
        Obj.set('isExpert', DataObjArr["rsProjectId"])  #

        Obj.set('totalCapital', 0)  #

        # 跟行情有关 后期接口处理pb3
        Obj.set('sz', )  #
        Obj.set('cw', DataObjArr["rsProjectId"])
        Obj.set('originalCapital', DataObjArr["rsProjectId"])

        Obj.set('pm', DataObjArr['NewsTitle'])
        Obj.set('syl', DataObjArr['NewsContent'])
        Obj.set('certId', self.NewsDate)
        Obj.set('desc', str(DataObjArr["rsMainkeyID"]))
        Obj.set('motto', self.A_DxtWZWTeacherList[0].get("objectId"))
        Obj.set('historyAccount', DataObjArr['NewsTitle'])
        Obj.set('relationId', DataObjArr['NewsTitle'])

if __name__ == "__main__":

	WZWTeacher_object = WZWTeacher()

	WZWTeacher_object.WZWTeacherPort()
	WZWTeacher_object.WZWTeacherMC()

