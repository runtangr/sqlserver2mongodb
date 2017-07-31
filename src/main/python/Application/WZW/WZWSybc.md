#王中王相关#

##1.资金表同步##
###调用存储###
P_Z_uimsVSTC_pro
###调用接口###
P_Z_uimsVSTC_pro
####传入参数####
	@rsMainkeyID int
	@rsDateTime datetime
	@top int
####返回数据####
	rsMainkeyID         自增ID
	rsStatus			默认状态
	rsDateTime			默认时间
	rsOperateID			默认
	rsDispIndex			默认
	rsProjectId			是否专家 10专家 0草根
	UserId				用户ID
	GroupStyle			参赛类别
	GroupBM				参赛账号
	OriginalCapital		当前赛季初始资金
	ResidualCapital		剩余资金
	FrozenCapital		冻结资金
	OtherDefine1		
	OtherDefine2		默认
	OtherDefine3		
	OtherDefine4		名称
	OtherDefine5		
	OtherDefine6 
	OtherDefine7 
	OtherDefine8 
	Timage				头像
	Tzsbh				证书编号	
	Ttzgy				投资格言
	Tfxsjs				分析师介绍
	DJS                 人气
	
##2.持仓表同步##
###调用存储###
P_Z_uimsVSTSC_pro
###调用接口###
P_Z_uimsVSTSC_pro
####传入参数####
	@rsMainkeyID int
	@rsDateTime datetime
	@top int
####返回数据####
	VGroupid  		资金ID
	BuyMonney   	买入金额
	FirstBuyDate	第一购买时间
	usevolume		可用数量
	Cost			成本
	cbj				成本价
	gpid			股票ID
	currentVolume	总数量
	stockshortname	股票名称
	stockcode		股票代码
	marketName		市场名称
	marketcode		市场代码
	rsmainkeyid		持仓ID
	rsDateTime		持仓默认时间

##3.交易记录表同步##
###调用存储###
P_Z_uimsVSTSCD_pro
###调用接口###
P_Z_uimsVSTSCD_pro
####传入参数####
	@rsMainkeyID int
	@rsDateTime datetime
	@top int

####返回数据####
	rsmainkeyid     自增ID
	rsDateTime		默认时间
	VGroupID        资金ID
	MarketCode		市场代码
	syl				收益率
	wtTime			委托时间
	profitorLoss    本次盈亏
	gpid			股票ID
	LogID			操作日志ID
	TransStyle		交易类型
	CJDate			成交时间
	volume			成交数量
	price			成交价
	cjje			成交金额
	stockcode		股票代码
	stockshortName	股票名称


##4.操作日志同步##
###调用存储###
P_Z_uimsVSTL
###调用接口###
P_Z_uimsVSTL
####传入参数####
	@rsMainkeyID int
	@rsDateTime datetime
	@top int
####返回数据####
	rsmainkeyid			自增长ID(操作日志ID)
	rsdatetime			默认时间
	logstyle			日志分类  ---1.日志 6博文
	rzlx				日志类型
	logdatetime			日志时间
	stockid				股票Id
	StockName			股票名称
	transrecordid		交易记录ID
	Logtitle			日志标题
	VGroupid			资金ID
	LogContent			日志内容

##5.高手动态同步##
###调用存储###
P_Z_CommUserAlert_dx
###调用接口###
P_Z_CommUserAlert_dx
####传入参数####
	@rsMainkeyID int
	@rsDateTime datetime
	@top int
####返回数据####
	rsMainkeyID			自增ID   
	rsDateTime          默认时间    
	AlertNewsDate		时间
	UserName			高手 
	UserCZ				操作
	cjj					成交价
	StockShortName		股票名称

##6.模拟大赛榜##

###调用存储###
P_W_Sel_MNSB
###调用接口###
Query_MNSB
####传入参数####
	@pagesize int,   --每页条数    同步传100000      
	@page  int,    --第几页        同步传1
	@TotalNum int  Output 
####返回数据####
	VGroupid		资金ID 
	nickname		选手名称
	YearSy			总收益
	bqsy			月收益，
	DjS				人气
	zjj				总资产

##6.模拟大赛榜-上月份##
###说明###
由于本月份数据实时计算 可用资金表数据进行相应计算 
或直接沿用老接口   此同步频率 每月最后一天四点同步即可
###调用存储###
P_W_Sel_MNSBSYF 此接口为老接口
###调用接口###
Query_MNSBSYF
####传入参数####

####返回数据####
	username		姓名，
	capital			总资产，
	profitorloss_lj	本月盈亏，
	ror				本月收益率
	Vgroupid        资金ID

##7.赛季ID列表##
###说明###
根据赛季ID在界面显示第几赛季。如SeasonId=1 第一赛季  每月同步一次即可
###调用存储###
P_W_Sel_SJLB    老接口
###调用接口###
Query_SJLB
###返回数据###
	SeasonId 赛季ID

##8.历史赛季数据##
###说明###
根据赛季ID列表循环同步数据
###调用存储###
P_W_Sel_SJList  老接口
###调用接口###
Query_SJList
####传入参数####
	@SeasonId bigint  --赛季ID

###返回数据###
	nickname		选手
	residualcapital	总资产
	bqyk			本期盈亏
	Bqsy			本期收益率
	counts			人气
	VGroupid		资金ID

##9.牛股榜##
###说明###
数据每日下午4点更新
###调用存储###
P_W_Sel_StockNGB   老接口
###调用接口###
Query_StockNGB
####传入参数####
	@Userid bigint=0,      --同步不传
	@WebIP  nvarchar(20)='' --同步不传 
	@PageSize  int,      --此传10000                                 
	@Page   int,    --传1  
	@TotalNum  int  Output  
###返回数据###
	StockShortName股票名称
	stockCode股票代码
	Price买入价
	StockID股票ID 
	Price_ZDF涨幅


##10.战绩快报##
###调用存储###
P_Z_uimsVSGG_Pro   
###调用接口###
P_Z_uimsVSGG_Pro
####传入参数####
	@rsMainkeyID int
	@rsDateTime datetime
	@top int
###返回数据###
	rsMainkeyID 	自增ID	
	rsdatetime 		时间
	Price_ZDF 		最大涨幅
	username 		姓名
	stockshortname 	股票名称
	stockcode 		股票代码
	MarketCode 		市场代码
	VgroupID		资金ID


##11.实时战绩播报##
同步逻辑:全量同步(删除老数据,同步新数据),每30分钟同步一次
###调用存储###
P_N_SSZJBB_WZW  
###调用接口###
P_N_SSZJBB_WZW	老接口
###传入参数###
###返回数据###
	rsDateTime    时间,
	OtherDefine2  买卖标识,
	OtherDefine3  赢利,
	NickName      姓名,
	StockShortName 股票名称,
	StockCode    股票代码

##12.持仓操作理由##
同步逻辑:增量同步  同步频率:10分钟同步一次
###调用存储###
P_Z_CZLY_WZW
###调用接口###
P_Z_CZLY_WZW
####传入参数####
	@rsMainkeyID int
	@rsDateTime datetime
	@top int
####返回数据####

	rsMainkeyID		自增ID
	rsDateTime		默认时间
	TransRecordId    持仓ID
	Logtitle		标题
	logcontent		内容
	stockshortname	股票名称
	stockcode		股票代码
	logdatetime		时间
	MarketCode		市场代码



