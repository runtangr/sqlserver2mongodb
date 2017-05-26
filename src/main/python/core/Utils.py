# -*- coding: utf-8 -*-
__author__ = "Sommily"
import leancloud
from collections import OrderedDict

def init_leancloud_client():
    import os
    LEANCLOUD_APP_ID = os.environ.get("LEANCLOUD_APP_ID", "3G47drEAaXtmQas7U4WxEmx4-gzGzoHsz")
    LEANCLOUD_APP_KEY = os.environ.get("LEANCLOUD_APP_KEY", "x3cl6OYR2mC6dDQsW0dMeceJ")
    LEANCLOUD_REGION = os.environ.get("LEANCLOUD_REGION", "CN")
    leancloud.init(app_id=LEANCLOUD_APP_ID, app_key=LEANCLOUD_APP_KEY)
    leancloud.use_region(LEANCLOUD_REGION)
    print("leancloud init success with app_id: {}, app_key: {}, region: {}".format(LEANCLOUD_APP_ID, LEANCLOUD_APP_KEY,
                                                                                   LEANCLOUD_REGION))


def getIso8601(dt):
    if dt in (None, ""):
        return None
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

def getDateTime(dt):
    #return {"iso": dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z", "__type":"Date"}
    if dt in (None, ""):
        return None
    result = OrderedDict()
    result["__type"] = "Date"
    result["iso"] = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return result

def tree(data, pid):
    ret = []
    for i in data:
        if i.get("fatherObjectId") == pid:
            t = {}
            t["objectId"] = i.id
            t["name"] = i.get("name")
            t["type"] = i.get("type")
            t["child"] = []
            t["child"] = tree(data, i.id)
            if t["child"]:
                t["hasChild"] = 1
            else:
                t["hasChild"] = 0
            ret.append(t)
    return ret