# coding:utf-8

import os
import datetime
import sys
import commands
import shutil
'''
自动创建index
并导入数据
'''

indexDate = sys.argv[1] # 20161001
path = sys.argv[2]      # /tagData
ipPort = "192.168.77.2:9210"

index = "tag" + indexDate
type = "taglib"

print path

if len(sys.argv) == 4 and sys.argv[3] == "1":
    create = "curl -XDELETE " + ipPort + "/" + index
    result = commands.getstatusoutput(create)
    print result[0]

create = "curl -XPOST " + ipPort + "/" + index
commands.getstatusoutput(create)

# 最后面不能以'结束
mapp = "curl -XPOST " + ipPort + "/" + index + "/" + type + "/_mapping?pretty -d '{\
    \"taglib\": {\
            \"properties\": {\
                \"keys\": {\
                    \"type\": \"string\",\
                    \"index\": \"not_analyzed\"\
                   },\
                \"keysSearch\": {\
                   \"type\": \"string\",\
                   \"analyzer\": \"smartcn\"\
                   },\
                \"province\": {\
                    \"type\": \"string\",\
                    \"index\": \"not_analyzed\"\
                   }, \
                \"city\": {\
                    \"type\": \"string\",\
                    \"index\": \"not_analyzed\"\
                   }\
                }\
         }\
  }\
'"

result = commands.getstatusoutput(mapp)
print result[0]

# sys.exit()



nowtime = datetime.datetime.now().strftime('%Y-%m-%d')
# bakpath="/data1/szdatacenter/bak/" + nowtime
bakpath = "/data1/szdatacenter/bak/" + indexDate
if not os.path.exists(bakpath):
    os.makedirs(bakpath)
for dirpath, dirnames, filenames in os.walk(path):
    for file in filenames:
        fullpath = os.path.join(dirpath, file)
        print fullpath
        print("********")
        patho = "curl -XPOST " + ipPort + "/" + index + "/" + type + "/_bulk?pretty' --data-binary " + '"@' + fullpath + '"'
        os.system(patho)
        # shutil.move(fullpath,bakpath)
        print "move" + fullpath + " to " + bakpath
