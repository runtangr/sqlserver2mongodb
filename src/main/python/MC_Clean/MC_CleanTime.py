import leancloud_patch
import leancloud
from Utils import init_leancloud_client
from leancloud import Query
from leancloud import Object
from leancloud import GeoPoint
import sys

def getClass(classname):
    try:
            mytest = Object.extend(classname)
            olds = Query(mytest).find()
            retv =[]
            for old in olds:

                retv.append(old)
            return retv
    except Exception,e:
        print 'e=',
    return []

def cleandata(item):
    datatype =  item.get("type")
    if datatype == sys.argv[2]:
        item.destroy()
        print 'query =', item
        print 'cleanClass===========1'

def cleanClass(document):
          retv = getClass(document)

          map(lambda item: cleandata(item),retv)

if __name__ == "__main__":

    init_leancloud_client()
    document = sys.argv[1]
    cleanClass(document)