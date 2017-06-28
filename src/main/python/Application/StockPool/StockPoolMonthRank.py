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

def   remoteSource():
        url = "http://stock.cjs.com.cn/Stocks.asmx?WSDL"
        client = Client(url)
        response = client.service.Query_NZGZF(Coordinates='021525374658617185',
                                                    Encryptionchar='F5AC95F60BBEDAA9372AE29B84F5E67A',
                                                  PoolStyle=1
                                                        )
        print("response",response.encode('utf8'))
        resp = json.loads(response)
        print("resp",resp)
def  StockPoll(PoolStyle):
        A_DxtStockPoolQuery = leancloud.Query('A_DxtStockPool')
        A_DxtStockPoolQuery.equal_to('relationId', str(PoolStyle))
        A_DxtStockPoolList = A_DxtStockPoolQuery.find()
        print("A_DxtStockPoolList",A_DxtStockPoolList)
        for item in A_DxtStockPoolList:
            print("item",item )
            print("item objectId ",item.get('objectId'))

def   addMonthRank(A_Obj,objectid,DataObjArr):
#        A_DxtStockPoolYearRankDiary = leancloud.Object.extend('A_DxtStockPoolMonthRank')


#        A_Obj = A_DxtStockPoolYearRankDiary()

        A_Obj.set('stockPoolObjectId', objectid )
        A_Obj.set('stockCode', DataObjArr['StockCode'])
        A_Obj.set('stockName', DataObjArr['StockShortName'])
        A_Obj.set('marketCode', DataObjArr['MarketCode'])  ########

        A_Obj.set('cqPrice', DataObjArr['CQPrice'])
        A_Obj.set('dqsy', DataObjArr['Dqsy'])
        A_Obj.set('inPrice', DataObjArr['AccessPrice'])

        A_Obj.set('stockComeFrom', DataObjArr['StockComeFrom'])
#        A_Obj.set('inTime', self.inTime)

        A_Obj.set('relationId', str(DataObjArr["rsMainkeyID"]))
        A_Obj.save()
def    DealData(self,relationId, DataObjArr):

        A_DxtStockPoolYearRankQuery = leancloud.Query('A_DxtStockPoolYearRank')
#    A_DxtStockPoolYearRankQuery.equal_to('relationId', str(DataObjArr['rsMainkeyID']))
        A_DxtStockPoolYearRankQuery.equal_to('relationId', relationId)


        A_DxtStockPoolYearRankList = A_DxtStockPoolYearRankQuery.find()



        # 编辑
        if len(A_DxtStockPoolYearRankList) > 0:
            
#            self.Edit(DataObjArr)
            A_Obj = A_DxtStockPoolYearRankList[0]
        else:
            A_DxtStockPoolYearRankDiary = leancloud.Object.extend('A_DxtStockPoolMonthRank')


            A_Obj = A_DxtStockPoolYearRankDiary()


            self.Add(DataObjArr)
              
if __name__ == '__main__':
    StockPoll(1)