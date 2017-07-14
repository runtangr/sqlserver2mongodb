#encoding=utf-8

'''
Modified on July 4, 2017

@author: tangr
'''

 #录播视频表cctv

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

class RecordVideo:
    def CreateSyncInfo(self):
        SyncControl = leancloud.Object.extend('SyncControl')
        self.SyncControlObj = SyncControl()
        querySyncInfo = SyncControl.query

        querySyncInfo.equal_to('type', 'RecordVideo')
        syncObj = querySyncInfo.find()
        if len(syncObj) == 0:
        
            self.SyncControlObj.set("type", "RecordVideo")
            self.SyncControlObj.set("mainKeyId", 0)
            self.SyncControlObj.set("rsDateTime", "1990-01-01")
            self.SyncControlObj.save()

        self.SyncControlObj = querySyncInfo.first()
        self.maxKeyId = int(self.SyncControlObj.get('mainKeyId'))
        self.rsDateTime = self.SyncControlObj.get('rsDateTime')
        
    def RecordVideoPort(self):
        '''
        获取端口数据
        '''
        url = "http://114.80.94.175:8084/Stocks.asmx?WSDL"
        client = Client(url)
        # print (client)
        top = 100

        self.CreateSyncInfo()

        # 录播视频表cctv WebService 测试接口 P_Z_video
        response = client.service.P_Z_video(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                            rsMainkeyID=self.maxKeyId,
                                                rsDateTime=self.rsDateTime,
                                                  top=top
                                                    )
        try:
            self.RecordVideo = json.loads(response)

        except Exception, e:
            logging.error("%s : webservice get data fail! data:%s" %(__file__ ,response))

    def RecordVideoMC(self):
        '''
        mc更新 A_DxtRecordVideo(录播视频表cctv)表
        '''

        maxKeyId = int(self.SyncControlObj.get('mainKeyId'))

        if self.RecordVideo["Code"] == 0:

            self.DataObj =  json.loads(self.RecordVideo["DataObj"])#


            map(self.DealData,self.DataObj)


        else:
             logging.warning("not data or data error：%s" %self.RecordVideo)

    def DealData(self,DataObjArr):

        #最后一条数据赋值
        if DataObjArr==self.DataObj[-1]:
            self.maxKeyId = int(DataObjArr['rsMainKeyId'])
            self.rsDateTime = DataObjArr['rsDateTime']
            self.SyncControlObj.set('mainKeyId', self.maxKeyId)
            self.SyncControlObj.set('rsDateTime', self.rsDateTime)
            self.SyncControlObj.save()

        #打印
        print ("maxKeyId:", self.maxKeyId, "===", "rsMainKeyId:", DataObjArr['rsMainKeyId'], "===",
               "rsDateTime:", DataObjArr['rsDateTime'])

        A_DxtRecordVideoQuery = leancloud.Query('A_DxtRecordVideo')
        A_DxtRecordVideoQuery.equal_to('relationId', DataObjArr['rsMainKeyId'])
        self.A_DxtRecordVideoList = A_DxtRecordVideoQuery.find()


        # 编辑
        if len(self.A_DxtRecordVideoList) > 0:

            self.Save(self.A_DxtRecordVideoList[0],DataObjArr)
        else:
            A_DxtRecordVideo = leancloud.Object.extend('A_DxtRecordVideo')
            A_DxtRecordVideoObj = A_DxtRecordVideo()
            self.Save(A_DxtRecordVideoObj,DataObjArr)

    def Save(self,Obj,DataObjArr):
        Obj.set('title', DataObjArr['title'])
        Obj.set('desc', DataObjArr["content"])
        Obj.set('videoType', DataObjArr['className'])
        Obj.set('videoImage', DataObjArr['pictureH5Url'])
        Obj.set('pictureH5Url', DataObjArr['pictureH5Url'])
        Obj.set('videoUrl', DataObjArr["url"])

        Obj.set('videoH5Url',DataObjArr["h5url"] )
        Obj.set('teacherName', DataObjArr["teachername"])

        Obj.set('videoSource', DataObjArr['sply'])
        Obj.set('status', DataObjArr["shzt"])
        Obj.set('isDisable', DataObjArr["sfjy"])
        Obj.set('isTop',  DataObjArr["isTop"])

        Obj.set('clickNumber', DataObjArr['hits'])
        Obj.set('collectNumber', DataObjArr['dscs'])
        Obj.set('clickNumberActual', DataObjArr["sjdjs"])
        Obj.set('collectNumberActual', DataObjArr['sjscs'])

        Obj.set('relationId', DataObjArr['rsMainKeyId'])
        Obj.save()

if __name__ == "__main__":

	RecordVideo_object = RecordVideo()

	RecordVideo_object.RecordVideoPort()
	RecordVideo_object.RecordVideoMC()

