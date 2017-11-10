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

def   addRankLastMonth(A_Obj,TeacherObj,DataObjArr,SeasonId):

        SeasonId =-1
        syl = DataObjArr["ror"]
        pm = CalculatePM(syl,SeasonId)

        A_Obj.set('name', DataObjArr["username"])
        A_Obj.set('groupBmId',DataObjArr["Vgroupid"])
        A_Obj.set('totalCapital', DataObjArr['capital'])

        A_Obj.set('profitorLoss', DataObjArr['profitorloss_lj'])
        A_Obj.set('syl', DataObjArr['ror'])
        A_Obj.set('pm', pm)

        A_Obj.set('season', SeasonId)
        A_Obj.set('relationId', DataObjArr["Vgroupid"])
        A_Obj.save()
        #非必要数据
        # A_Obj.set('syl', )
        # A_Obj.set('photo', TeacherObj.get('photo'))
        # A_Obj.set('teacherObjectId', TeacherObj.get('objectId'))
        # A_Obj.set('djs', TeacherObj.get("djs"))
        # A_Obj.set('sz', TeacherObj.get("sz"))
        # A_Obj.set('originalCapital', TeacherObj.get("originalCapital"))
        # A_Obj.set('ljsy', 0)
        # A_Obj.set('yearSyl', 0)
        #
        # A_Obj.save()

def  addRankThisMonth(A_Obj, TeacherObj, DataObjArr,SeasonId):

    SeasonId = 0
    syl = DataObjArr["bqsy"]
    pm = CalculatePM(syl, SeasonId)

    A_Obj.set('name', DataObjArr["nickname"])
    A_Obj.set('groupBmId', DataObjArr["VGroupid"])
    A_Obj.set('djs', DataObjArr["DjS"])
    A_Obj.set('totalCapital', DataObjArr['zjj'])

    A_Obj.set('pm', DataObjArr['row']) #add

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

    syl = DataObjArr["bqsy"]
    pm = CalculatePM(syl, SeasonId)

    A_Obj.set('name', DataObjArr["nickname"])
    A_Obj.set('groupBmId', DataObjArr["VGroupid"])
    A_Obj.set('djs', DataObjArr["counts"])
    A_Obj.set('totalCapital', DataObjArr['residualcapital'])

    A_Obj.set('profitorLoss', DataObjArr['bqyk'])
    A_Obj.set('pm', pm)

    A_Obj.set('syl', DataObjArr["bqsy"])
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


def  RankTeacher(Data,save_select):
    A_DxtWZWTeacherQuery = leancloud.Query('A_DxtWZWTeacher')
    if save_select==addRankLastMonth:
        A_DxtWZWTeacherQuery.equal_to('groupBmId', Data["Vgroupid"])
    else:
        A_DxtWZWTeacherQuery.equal_to('groupBmId', Data["VGroupid"])
    A_DxtWZWTeacherList = A_DxtWZWTeacherQuery.find()
    # print("item objectId ",item.get('objectId'))
    return A_DxtWZWTeacherList

def  CalculatePM(syl,SeasonId):
    #月收益计算 本赛季排名
    A_DxtWZWRankQuery = leancloud.Query('A_DxtWZWRank')
    A_DxtWZWRankQuery.equal_to("season",SeasonId)
    A_DxtWZWRankQueryAll = A_DxtWZWRankQuery.find()

    syl_all = []
    if len(A_DxtWZWRankQueryAll) == 0:
        pm = 1
    else:
        # 遍历
        for WZWRank in A_DxtWZWRankQueryAll:
            syl_all.append(WZWRank.get("syl"))

        if syl not in syl_all:
            syl_all.append(syl)

        # 排序
        syl_all.sort()
        syl_all.reverse()
        # 获取当前排名
        pm = syl_all.index(syl) + 1

    return pm


def    DealData(relationId, TeacherObj , DataObjArr, save_select,SeasonId):

        A_DxtWZWRankQuery = leancloud.Query('A_DxtWZWRank')

        A_DxtWZWRankQuery.equal_to('relationId', relationId)

        season = SeasonId
        A_DxtWZWRankQuery.equal_to('season', season)

        A_DxtWZWRankList = A_DxtWZWRankQuery.find()

        # 编辑  这里不匹配老师，每个赛季老师可能不存在老师表
        #需要匹配 season id
        if len(A_DxtWZWRankList) > 0 :

            print("len>1")
            A_Obj = A_DxtWZWRankList[0]
        else:
            print("len=0")
            A_DxtWZWRankDiary = leancloud.Object.extend('A_DxtWZWRank')


            A_Obj = A_DxtWZWRankDiary()


        save_select(A_Obj,TeacherObj, DataObjArr,SeasonId)

def   processSource(item,save_select,SeasonId):
    # print("item",item)
    # print("rsMainkeyID",item["rsMainkeyID"] )
    if save_select==addRankLastMonth:
        relationid = item["Vgroupid"]
    else:
        relationid = item["VGroupid"]

    TeacherObj = RankTeacher(item,save_select)
    # print("poolobjectid", teacherobjectid)
    #没有匹配到老师数据，不存储数据


    DealData(relationid, TeacherObj , item ,save_select,SeasonId)
    

def  Rank(retv,save_select,SeasonId):

    try:
        DataObj = json.loads(retv['DataObj'])

    except Exception, e:
        logging.warning("data format error :%s" % retv)
        return

    
    try:
        map(lambda item: processSource(item,save_select,SeasonId), DataObj)
    except Exception, e:
        logging.warning("data format error :%s" % retv)
   
   
if __name__ == '__main__':

     url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
     client = Client(url)

     while True:
         queryWZWRank = leancloud.Query('A_DxtWZWRank')
         queryWZWRank.not_equal_to("season", 0)
         query_list = queryWZWRank.find()
         if len(query_list) == 0:
             break
         leancloud.Object.destroy_all(query_list)

     # ThisMonth
     # retv = remoteSourceThisMonth(client)
     # save_select = addRankThisMonth
     # SeasonId = 0
     # Rank(retv, save_select,SeasonId)

     # LastMonth
     retv = remoteSourceLastMonth(client)
     save_select = addRankLastMonth
     SeasonId = -1
     Rank(retv,save_select,SeasonId)

     # Season

     SeasonIdList = remoteSourceSJSeasonId(client)
     save_select = addRankSeason

     remote = lambda SeasonId:remoteSourceSJSeason(client,SeasonId)

     for data in SeasonIdList:
         SeasonId, retv = remote(int(data.values()[0]))
        #check
         Rank(retv, save_select,SeasonId)



    