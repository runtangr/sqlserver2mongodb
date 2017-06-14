#encoding=utf-8
import re
a= "我的（300334）、他的（1423234）、其他（12313）"


c= re.split("、",a)
print (c)
for data in c:
    numer = re.search(r"\d+",data)
    print (numer)