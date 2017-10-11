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


def    remove_data():

        while True:
            A_DxtWZWRankQuery = leancloud.Query('A_DxtWZWRank')
            query_list = A_DxtWZWRankQuery.find()
            if len(query_list) == 0:
                break
            leancloud.Object.destroy_all(query_list)


   
if __name__ == '__main__':
    remove_data()