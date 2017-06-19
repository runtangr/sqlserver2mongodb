#encoding=utf-8
import re
a= "我的（300334）、他的（1423234）、其他（12313）"


c= re.split("、",a)
print (c)
for data in c:
    numer = re.search(r"\d+",data)
    print (numer)

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