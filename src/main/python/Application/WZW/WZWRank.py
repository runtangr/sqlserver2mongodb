#encoding=utf-8
'''
Created on 2017年6月30日

@author: tangr
'''
import sys
import os
#sys.path.append("../..")
#print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from suds.client import Client
import json
import logging

from core.leancloud_patch import * 
import core.leancloud_patch
import leancloud
from core.Utils import init_leancloud_client

logging.basicConfig(level=logging.WARNING,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S'
                    )

init_leancloud_client()

def   remoteSourceLastMonth(client):

        MNSBSYF = client.service.Query_MNSBSYF(Coordinates='021525374658617185',
                                                    Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                        )
        # print("response",response.encode('utf8'))
        resp = json.loads(MNSBSYF)

        # print("resp",resp)
        return resp

def   remoteSourceThisMonth(client):
        MNSB = client.service.Query_MNSB(Coordinates='021525374658617185',
                                         Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                         pagesize=100000,
                                         page=1
                                             )
        # print("response",response.encode('utf8'))
        resp= json.loads(MNSB)

        # print("resp",resp)
        return resp

def   remoteSourceSJSeason(client,SeasonId):


        SJList = client.service.Query_SJList(Coordinates='021525374658617185',
                                             Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                             SeasonId=SeasonId
                                             )

        # print("response",response.encode('utf8'))
        resp = json.loads(SJList)

        # print("resp",resp)
        return SeasonId,resp

def   remoteSourceSJSeasonId(client):

    SJLB = client.service.Query_SJLB(Coordinates='021525374658617185',
                                     Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                     )
    # print("response",response.encode('utf8'))
    resp = json.loads(SJLB)
    SeasonIdDict = json.loads(resp["DataObj"])


    # print("SeasonIdDict",SeasonIdDict)
    return SeasonIdDict

def   addRankLastMonth(A_Obj,TeacherObj,DataObjArr):

        SeasonId =-1
        syl = DataObjArr["Ror"]
        pm = CalculatePM(syl,SeasonId)

        A_Obj.set('name', DataObjArr["username"])
        A_Obj.set('groupBmId',DataObjArr["VGroupid"])
        A_Obj.set('totalCapital', DataObjArr['capital'])
        A_Obj.set('syl', )
        A_Obj.set('profitorLoss', DataObjArr['profitorloss_lj'])

        A_Obj.set('pm', pm)

        A_Obj.set('season', SeasonId)
        A_Obj.set('relationId', DataObjArr["VGroupid"])
        A_Obj.save()
        #非必要数据
        # A_Obj.set('photo', TeacherObj.get('photo'))
        # A_Obj.set('teacherObjectId', TeacherObj.get('objectId'))
        # A_Obj.set('djs', TeacherObj.get("djs"))
        # A_Obj.set('sz', TeacherObj.get("sz"))
        # A_Obj.set('originalCapital', TeacherObj.get("originalCapital"))
        # A_Obj.set('ljsy', 0)
        # A_Obj.set('yearSyl', 0)
        #
        # A_Obj.save()

def  addRankThisMonth(A_Obj, TeacherObj, DataObjArr):

    SeasonId = 0
    syl = DataObjArr["bqsy"]
    pm = CalculatePM(syl, SeasonId)

    A_Obj.set('name', DataObjArr["nickname"])
    A_Obj.set('groupBmId', DataObjArr["VGroupid"])
    A_Obj.set('djs', DataObjArr["DjS"])
    A_Obj.set('totalCapital', DataObjArr['zjj'])

    A_Obj.set('pm', pm)

    A_Obj.set('yearSyl', DataObjArr["YearSy"])
    A_Obj.set('syl', DataObjArr["bqsy"])
    A_Obj.set('season', SeasonId)
    A_Obj.set('relationId', DataObjArr["VGroupid"])
    A_Obj.save()
    # 非必要数据
    # A_Obj.set('photo', TeacherObj.get('photo'))
    # A_Obj.set('teacherObjectId', TeacherObj.get('objectId'))
    # A_Obj.set('originalCapital', TeacherObj.get("originalCapital"))
    # A_Obj.set('sz', TeacherObj.get("sz"))
    # A_Obj.set('profitorLoss', 0)
    # A_Obj.set('ljsy', 0)
    # A_Obj.save()

 #check
def  addRankSeason(A_Obj, TeacherObj, DataObjArr,SeasonId):

    SeasonId = 0
    syl = DataObjArr["bqsy"]
    pm = CalculatePM(syl, SeasonId)

    A_Obj.set('name', DataObjArr["nickname"])
    A_Obj.set('groupBmId', DataObjArr["VGroupid"])
    A_Obj.set('djs', DataObjArr["counts"])
    A_Obj.set('totalCapital', DataObjArr['residualcapital'])

    A_Obj.set('profitorLoss', DataObjArr['bqyk'])
    A_Obj.set('pm', pm)

    A_Obj.set('syl', DataObjArr["Bqsy"])
    A_Obj.set('season', SeasonId)
    A_Obj.set('relationId', DataObjArr["VGroupid"])
    A_Obj.save()
    # 非必要数据
    # A_Obj.set('photo', TeacherObj.get('photo'))
    # A_Obj.set('teacherObjectId', TeacherObj.get('objectId'))
    # A_Obj.set('originalCapital', TeacherObj.get("originalCapital"))
    # A_Obj.set('sz', TeacherObj.get("sz"))
    #
    # A_Obj.set('ljsy', 0)
    # A_Obj.save()


def  RankTeacher(Data):
    A_DxtWZWTeacherQuery = leancloud.Query('A_DxtWZWTeacher')
    A_DxtWZWTeacherQuery.equal_to('groupBmId', Data["VGroupid"])
    item = A_DxtWZWTeacherQuery.first()
    # print("item objectId ",item.get('objectId'))
    return item

def  CalculatePM(syl,SeasonId):
    #月收益计算 本赛季排名
    A_DxtWZWRankQuery = leancloud.Query('A_DxtWZWRank')
    A_DxtWZWRankQuery.equal_to("season",SeasonId)
    A_DxtWZWRankQueryAll = A_DxtWZWRankQuery.find()

    syl_all = []
    if len(A_DxtWZWRankQueryAll) == 0:
        pm = 0
    else:
        # 遍历
        for WZWRank in A_DxtWZWRankQueryAll:
            syl_all.append(WZWRank.get("pm"))
        # 排序
        syl_all.sort()
        syl_all.reverse()
        # 获取当前排名
        pm = syl_all.index(syl) + 1

    return pm

def    DealData(relationId, TeacherObj , DataObjArr, save_select):

        A_DxtWZWRankQuery = leancloud.Query('A_DxtWZWRank')

        A_DxtWZWRankQuery.equal_to('relationId', relationId)

        A_DxtWZWRankList = A_DxtWZWRankQuery.find()

        # 编辑
        if len(A_DxtWZWRankList) > 0:

            print("len>1")
            A_Obj = A_DxtWZWRankList[0]
        else:
            print("len=0")
            A_DxtWZWRankDiary = leancloud.Object.extend('A_DxtWZWRank')


            A_Obj = A_DxtWZWRankDiary()


            save_select(A_Obj,TeacherObj, DataObjArr)

def   processSource(item,save_select):
    # print("item",item)
    # print("rsMainkeyID",item["rsMainkeyID"] )
    relationid = item["VGroupid"]

    TeacherObj = RankTeacher(item)
    # print("poolobjectid", teacherobjectid)
    #没有匹配到老师数据，不存储数据


    DealData(relationid, TeacherObj , item ,save_select)
    

def  Rank(retv,save_select):

    try:
        DataObj = json.loads(retv['DataObj'])

    except Exception, e:
        logging.warning("data format error :%s" % retv)
        return

    
    try:
        map(lambda item: processSource(item,save_select), DataObj)
    except Exception, e:
        logging.warning("data format error :%s" % retv)
   
   
if __name__ == '__main__':

     url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
     client = Client(url)
     #LastMonth
     retv = remoteSourceLastMonth(client)
     save_select = addRankLastMonth
     Rank(retv,save_select)

     # ThisMonth
     retv = remoteSourceThisMonth(client)
     save_select = addRankThisMonth
     Rank(retv, save_select)

     # Season
     SeasonIdDict = remoteSourceSJSeasonId(client)
     save_select = addRankSeason

     x = lambda SeasonId:remoteSourceSJSeason(SeasonId, client)
     for data in SeasonIdDict.values():
         SeasonId, resp = x(data)
        #check
         Rank(retv, save_select(SeasonId=SeasonId))



    