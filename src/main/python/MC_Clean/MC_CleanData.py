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
                print 'query =',old
                retv.append(old)
            return retv
    except Exception,e:
        print 'e=',
    return []
def cleanClass(document):
          print 'cleanClass===========',len(retv)
          map(lambda item: item.destroy(),retv)

if __name__ == "__main__":

    init_leancloud_client()

    document = sys.argv[1]

    retv = getClass(document)
    cleanClass(retv)