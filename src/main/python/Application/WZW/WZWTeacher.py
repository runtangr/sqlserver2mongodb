#encoding=utf-8

'''
Modified on June 26, 2017

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

import MarketData

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

        SyncControl = leancloud.Object.extend('SyncControl')
        self.SyncControlObj = SyncControl()
        querySyncInfo = SyncControl.query

        querySyncInfo.equal_to('type', 'WZWTeacher')
        syncObj = querySyncInfo.find()
        if len(syncObj)== 0:
            dataTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
            self.SyncControlObj.set("type","WZWTeacher")
            self.SyncControlObj.set("mainKeyId",0)
            self.SyncControlObj.set("rsDateTime","1990-01-01")
            self.SyncControlObj.save()

        self.SyncControlObj = querySyncInfo.first()
        self.maxKeyId = int(self.SyncControlObj.get('mainKeyId'))
        self.rsDateTime = self.SyncControlObj.get('rsDateTime')
        top = 200

        # 王中王老师列表 WebService 测试接口P_Z_uimsVSTC_pro
        response = client.service.P_Z_uimsVSTC_pro(Coordinates='021525374658617185',
                                                Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                rsMainkeyID=self.maxKeyId,
                                                rsDateTime="2017-08-01 00:00:00",
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

        maxKeyId = int(self.SyncControlObj.get('mainKeyId'))

        if self.WZWTeacher["Code"] == 0:

            self.DataObj =  json.loads(self.WZWTeacher["DataObj"])


            map(self.DealData,self.DataObj)


        else:
             logging.warning("提交王中王老师列表数据返回失败：%s" %self.WZWTeacher)

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
        # self.NewsDate = datetime.strptime(DataObjArr['NewsDate'][:-5],'%Y-%m-%d %H:%M:%S')
        # totalCapital = DataObjArr["ResidualCapital"] + DataObjArr["ResidualCapital"]
        #专家
        self.isExpert = 0 if  DataObjArr["rsProjectId"] else 1




        A_DxtWZWTeacherQuery = leancloud.Query('A_DxtWZWTeacher')
        A_DxtWZWTeacherQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
        self.A_DxtWZWTeacherList = A_DxtWZWTeacherQuery.find()

        # 查找WZWRank 本月 匹配 rsMainkeyID ，取出pm
        A_DxtWZWRankQuery = leancloud.Query('A_DxtWZWRank')
        A_DxtWZWRankQuery.equal_to('groupBmId', DataObjArr["rsMainkeyID"])
        A_DxtWZWRankQuery.equal_to('season', 0)
        self.A_DxtWZWStockList = A_DxtWZWRankQuery.find()
        if len(self.A_DxtWZWStockList) == 0 :
            return
        WZWStockData = self.A_DxtWZWStockList[0]
        self.pm = WZWStockData.get("pm")
        self.yearSyl = WZWStockData.get("yearSyl")

        #查找WZWStock 匹配name ，取出objectid
        A_DxtWZWZWStockQuery = leancloud.Query('A_DxtWZWStock')
        A_DxtWZWZWStockQuery.equal_to('groupBmId', DataObjArr["rsMainkeyID"])
        self.A_DxtWZWStockList = A_DxtWZWZWStockQuery.find()
        # 总市值
        self.total_sz = 0
        if len(self.A_DxtWZWStockList)!=0:

            # 总市值 = 所有 持仓市价（持仓市价 = 行情接口 获取当前价 *当前持仓股数）
            for PositionPrice in self.A_DxtWZWStockList:
                jduge_time = PositionPrice.get("firstBuyDate")
                year = datetime.today().year
                date_cp = int(str(datetime.today().month))
                if date_cp <10:
                    date = int(str(datetime.today().year)+"0"+str(datetime.today().month)+"01")
                else:
                    date = int(str(datetime.today().year) + str(datetime.today().month) + "01")
                jduge_time_cp = int(time.strftime("%Y%m%d",jduge_time.timetuple()))
                # data.astimezone(timezone.utc).replace(tzinfo=None)
                if jduge_time_cp >= date:
                    self.total_sz += PositionPrice.get("total_sz")
        # 总资产 = 剩余资金+冻结资金+总市值（）
        self.totalCapital = DataObjArr["ResidualCapital"] + DataObjArr["FrozenCapital"] + self.total_sz
        # 当前仓位= (总市值/总资产) *100
        self.cw = (self.total_sz/self.totalCapital)*100
        #收益率 = (总资产/本期起始资金 -1)*100
        self.syl = (self.totalCapital/DataObjArr["OriginalCapital"]-1)*100

        if (DataObjArr['rsMainkeyID'] == 73761):
            a=1

        # #排名初始化
        # self.pm = 0

        self.historyAccount={}  ###########

            # 编辑 存储
        if len(self.A_DxtWZWTeacherList) > 0:

            self.Save(self.A_DxtWZWTeacherList[0],DataObjArr)
        else:
            A_DxtWZWTeacher = leancloud.Object.extend('A_DxtWZWTeacher')
            A_DxtWZWTeacherObj = A_DxtWZWTeacher()
            self.Save(A_DxtWZWTeacherObj,DataObjArr)

        # 排行 相关数据处理
        A_DxtWZWTeacherQuery = leancloud.Query('A_DxtWZWTeacher')
        self.A_DxtWZWTeacherAll = A_DxtWZWTeacherQuery.find()

        TeacherProperty = []
        # if len(self.A_DxtWZWTeacherAll) == 0:
        #     self.pm = 0
        # else:
        #     # 遍历所有老师
        #     for Teacher in self.A_DxtWZWTeacherAll:
        #         TeacherProperty.append(Teacher.get("totalCapital"))
        #     # 排序
        #     TeacherProperty.sort()
        #     TeacherProperty.reverse()
        #     # 获取当前排名
        #     self.pm = TeacherProperty.index(self.totalCapital)+1
        #     # 保存当前
        #
        #     #######save  可完善
        #
        #     A_DxtWZWTeacherQuery = leancloud.Query('A_DxtWZWTeacher')
        #     A_DxtWZWTeacherQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
        #     self.A_DxtWZWTeacherList = A_DxtWZWTeacherQuery.find()

        # 编辑 存储
        if len(self.A_DxtWZWTeacherList) > 0:

            self.Save(self.A_DxtWZWTeacherList[0], DataObjArr)
        else:
            A_DxtWZWTeacher = leancloud.Object.extend('A_DxtWZWTeacher')
            A_DxtWZWTeacherObj = A_DxtWZWTeacher()
            self.Save(A_DxtWZWTeacherObj, DataObjArr)

    def Save(self,Obj,DataObjArr):

        Obj.set('name', DataObjArr['OtherDefine4'])
        Obj.set('photo', DataObjArr['Timage'])
        Obj.set('groupBmId', DataObjArr['rsMainkeyID'])
        Obj.set('djs', DataObjArr['DJS'])
        Obj.set('isExpert', self.isExpert)

        Obj.set('totalCapital', self.totalCapital)

        Obj.set('sz', self.total_sz)
        Obj.set('cw', self.cw)
        Obj.set('originalCapital', DataObjArr["OriginalCapital"])

        # Obj.set('pm',self.pm)  #|当月排行|无|
        Obj.set('pm', self.pm)
        Obj.set('syl', self.syl)
        Obj.set('yearSyl', self.yearSyl)

        Obj.set('certId', DataObjArr["Tzsbh"])
        Obj.set('desc', DataObjArr["Tfxsjs"])
        Obj.set('motto', DataObjArr["Ttzgy"])
        Obj.set('historyAccount', self.historyAccount)  #历史账目-资金ID|无|
        Obj.set('relationId', str(DataObjArr["rsMainkeyID"]))
        Obj.set('residualCapital', DataObjArr["ResidualCapital"])
        Obj.set('frozenCapital', DataObjArr["FrozenCapital"])
        Obj.save()

if __name__ == "__main__":

	WZWTeacher_object = WZWTeacher()

	WZWTeacher_object.WZWTeacherPort()
	WZWTeacher_object.WZWTeacherMC()

