#encoding=utf-8
'''
Created on 2017年6月22日

@author: aadebuger
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

def   remoteSource(PoolStyleValue):
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        response = client.service.Query_YZGZF(Coordinates='021525374658617185',
                                                    Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                  PoolStyle=PoolStyleValue
                                                        )
        print("response",response.encode('utf8'))
        resp = json.loads(response)
        print("resp",resp)
        return resp
def  StockPoll(PoolStyle):
        A_DxtStockPoolQuery = leancloud.Query('A_DxtStockPool')
        A_DxtStockPoolQuery.equal_to('relationId', str(PoolStyle))
        item = A_DxtStockPoolQuery.first()
        print("item objectId ",item.get('objectId'))
        return item.get('objectId')
def   addMonthRank(A_Obj,objectid,DataObjArr):

        inTime = datetime.strptime(DataObjArr['AccessDateTime'],"%Y-%m-%d %H:%M:%S")

        A_Obj.set('stockPoolObjectId', objectid )
        A_Obj.set('stockCode', DataObjArr['StockCode'])
        A_Obj.set('stockName', DataObjArr['StockShortName'])
        A_Obj.set('marketCode', DataObjArr['MarketCode'])

        A_Obj.set('cqPrice', DataObjArr['CQPrice'])
        A_Obj.set('dqsy', DataObjArr['Dqsy'])
        A_Obj.set('inPrice', DataObjArr['AccessPrice'])

        A_Obj.set('stockComeFrom', DataObjArr['StockComeFrom'])
        A_Obj.set('inTime', inTime)

        A_Obj.set('relationId', str(DataObjArr["rsMainkeyID"]))
        A_Obj.save()
def    DealData(relationId, poolobjectid , DataObjArr):

        # A_DxtStockPoolMonthRankQuery = leancloud.Query('A_DxtStockPoolMonthRank')
#    A_DxtStockPoolMonthRankQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
#         A_DxtStockPoolMonthRankQuery.equal_to('relationId', str(relationId))


        # A_DxtStockPoolMonthRankList = A_DxtStockPoolMonthRankQuery.find()

#         # 编辑
#         if len(A_DxtStockPoolMonthRankList) > 0:
#
# #            self.Edit(DataObjArr)
#             print("len>1")
#             A_Obj = A_DxtStockPoolMonthRankList[0]
#         else:
#             print("len=0")
        #全量同步
        A_DxtStockPoolMonthRankDiary = leancloud.Object.extend('A_DxtStockPoolMonthRank')


        A_Obj = A_DxtStockPoolMonthRankDiary()


        addMonthRank(A_Obj,poolobjectid, DataObjArr)

def   processSource(item,poolobjectid):
    print("item",item)  
    print("rsMainkeyID",item["rsMainkeyID"] )  
    relationid =  item["rsMainkeyID"]
    DealData(relationid, poolobjectid , item )
    

def  monthrank(poolvalue):
    poolobjectid = StockPoll(poolvalue)
    print("poolobjectid",poolobjectid)
    retv= remoteSource(poolvalue)
    try:
        map(lambda item:processSource(item,poolobjectid),json.loads(retv['DataObj']))
    except Exception, e:
        logging.warning("提交股票池年最高涨幅榜数据返回失败：%s" % retv)
   
if __name__ == '__main__':

    # 先删除原有数据
    while True:
        queryStockPoolMonthRank = leancloud.Query('A_DxtStockPoolMonthRank')
        query_list = queryStockPoolMonthRank.find()
        if len(query_list) == 0:
            break
        leancloud.Object.destroy_all(query_list)

    monthrank(1)
    monthrank(2)
    monthrank(3)