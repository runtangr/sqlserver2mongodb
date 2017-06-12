
#1、资金持仓数据同步
python  /app/src/main/python/Application/Daemon/Position.py  &

#2、成交数据同步
python  /app/src/main/python/Application/Daemon/Order.py  &

#3、大赛统计同步
#python  /app/src/main/python/Application/Daemon/Statistics.py  &

#4、排名数据同步
python  /app/src/main/python/Application/Daemon/Range.py  &

#5、获奖感言同步
python  /app/src/main/python/Application/Daemon/Speech.py  &

#6、历史排名同步
python  /app/src/main/python/Application/Daemon/HistRank.py  &

#7、专家点评同步
python  /app/src/main/python/Application/Daemon/Comment.py  &

#8、赛季同步
python  /app/src/main/python/Application/Daemon/Season.py  &

#9、牛股榜同步
python  /app/src/main/python/Application/Daemon/NiuguList.py  &
