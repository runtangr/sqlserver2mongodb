#encoding=utf-8

'''
Modified on July 6, 2017

@author: tangr
'''

 #技术学堂表

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

class CommNewsExtract_cp:
    def CreateSyncInfo(self,*args):
        SyncControl = leancloud.Object.extend('SyncControl')
        self.SyncControlObj = SyncControl()
        querySyncInfo = SyncControl.query

        querySyncInfo.equal_to('type', 'CommNewsExtract_cp')
        syncObj = querySyncInfo.find()
        if len(syncObj) == 0:
            self.SyncControlObj.set("type", "CommNewsExtract_cp")
            self.SyncControlObj.set("mainKeyId", 0)
            self.SyncControlObj.set("rsDateTime", "1990-01-01")
            self.SyncControlObj.save()

        self.SyncControlObj = querySyncInfo.first()
        self.maxKeyId = int(self.SyncControlObj.get('mainKeyId'))
        self.rsDateTime = self.SyncControlObj.get('rsDateTime')

    def CommNewsExtract_cpPort(self):
        '''
        获取端口数据
        '''
        url = "http://61.139.76.139:9527/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)

        self.CreateSyncInfo()
        top =100
        # 技术学堂表 WebService 测试接口 Query_CommNews_Extract
        response = client.service.Query_CommNews_Extract(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                rsMainkeyid=self.maxKeyId,
                                              rsDatetime=self.rsDateTime,
                                              #   rsDatetime=    "2016-05-20 18:43:00.000",
                                                  top=top
                                                    )
        try:
            self.CommNewsExtract_cp = json.loads(response)

        except Exception, e:
            logging.error("%s :webservice get data error! %s" %(__file__ ,response))

    def CommNewsExtract_cpMC(self):
        '''
        mc更新 A_DxtInformation(技术学堂表)表
        '''

        maxKeyId = int(self.SyncControlObj.get('mainKeyId'))

        if self.CommNewsExtract_cp["Code"] == 0:

            self.DataObj =  json.loads(self.CommNewsExtract_cp["DataObj"])#


            map(self.DealData,self.DataObj)


        else:
            logging.warning("%s:data return fail!：%s" %(__file__ ,self.CommNewsExtract_cp))

    def DealData(self,DataObjArr):

        #最后一条数据赋值
        if DataObjArr==self.DataObj[-1]:
            self.maxKeyId = int(DataObjArr['rsMainkeyID'])
            self.rsDateTime = DataObjArr['rsDateTime']
            self.SyncControlObj.set('mainKeyId', self.maxKeyId)
            self.SyncControlObj.set('rsDateTime', self.rsDateTime)
            self.SyncControlObj.save()

        #打印
        print ("maxKeyId:", self.maxKeyId, "===", "rsMainkeyID:", DataObjArr['rsMainkeyID'], "===",
               "rsDateTime:", DataObjArr['rsDateTime'])

        #数据处理
        # 转换
        if DataObjArr['rsStatus'] > 0:
            self.isDisable = 0
        else:
            self.isDisable = 1

        self.publishTime = datetime.strptime(DataObjArr['NewsDate'][:-5], '%Y-%m-%d %H:%M:%S')

        A_DxtInformationQuery = leancloud.Query('A_DxtInformation')
        A_DxtInformationQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
        # 同步判断
        A_DxtInformationQuery.equal_to('sync', 4)
        self.A_DxtInformationList = A_DxtInformationQuery.find()
        # 编辑
        if len(self.A_DxtInformationList) > 0:
            if int(DataObjArr['rsStatus']) <0:
                print("rsStatus <0")
                return

            print ("len>1")
            self.Save(self.A_DxtInformationList[0],DataObjArr)

        else:
            A_DxtInformation = leancloud.Object.extend('A_DxtInformation')
            A_DxtInformationObj = A_DxtInformation()
            if int(DataObjArr['rsStatus']) <0:
                print("rsStatus <0")
                return

            print ("len<1")
            # print ("DataObjArr = ",DataObjArr)
            self.Save(A_DxtInformationObj,DataObjArr)


    def Save(self,Obj,DataObjArr):
        Obj.set('sync', 4)
        Obj.set('title', DataObjArr['NewsTitle'])
        Obj.set('source', DataObjArr["NewsSource"])
        Obj.set('summary', DataObjArr["NewsBrief"])
        Obj.set('thumbnail', "")

        Obj.set('url', DataObjArr['OtherDefine4'])  #静态页|
        Obj.set('pcUrl', DataObjArr['OtherDefine4'])  # 静态页|
        if len(DataObjArr['NewsContent'])<64*1024:

            Obj.set('content', DataObjArr['NewsContent'])
            Obj.set('srcContent', DataObjArr['NewsContent'])
        else:
            Obj.set('content', "")
            print ("rsMainkeyID = ",DataObjArr['rsMainkeyID'])
            print ("data len >64k")
        # print ("NewsContent = ",DataObjArr['NewsContent'])
        # print ("NewsContent len = ", len(DataObjArr['NewsContent']))


        Obj.set('NewsStyle', DataObjArr['NewsStyle'])   #add

        tmp_categories = []
        tmp_categories.append(DataObjArr['ClassName'])
        Obj.set('categories', tmp_categories)
        Obj.set('labels', tmp_categories)

        Obj.set('isDisable', self.isDisable)

        Obj.set('author', DataObjArr['NewsAuthor'])
        Obj.set('publishTime', self.publishTime)
        Obj.set('clickNumber', DataObjArr["OtherDefine1"])
        Obj.set('likeNumber', DataObjArr['OtherDefine3'])
        Obj.set('shareNumber', 0)
        Obj.set('collectNumber', DataObjArr["OtherDefine2"])
        Obj.set('relationId', DataObjArr['rsMainkeyID'])
        #
        Obj.set('contentDealStatus', 0)
        Obj.set('CDNStatus', 0)
        Obj.set('imgCDNStatus', 0)
        print ("obj = ",Obj)
        print("object=", Obj.get("objectId"))

        Obj.save()

if __name__ == "__main__":

	CommNewsExtract_cp_object = CommNewsExtract_cp()

	CommNewsExtract_cp_object.CommNewsExtract_cpPort()
	CommNewsExtract_cp_object.CommNewsExtract_cpMC()

