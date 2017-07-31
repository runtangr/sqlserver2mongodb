
1、王中王老师列表
####描述####
王中王老师列表
###同步逻辑描述###

###webservice接口###
P_Z_uimsVSTC_pro
###表名###
A_DxtWZWTeacher
####字段说明####
|名称|类型|说明|缺省|
|--------|
|name|string|老师名称|无|
|photo|string|老师头像照片地址|无|
|groupBmId|number|当月王中王资金ID|无|
|djs|number|人气|无|
|isExpert|number|是否专家 0-专家 1-草根|0|
|totalCapital|number|总资产|无|
|sz|number|总市值|无|
|cw|number|当前仓位|无|
|originalCapital|number|本期起始资金|无|
|pm|number|当月排行|无|
|syl|number|收益率|无|
|certId|string|投资证书编号|无|
|desc|string|分析师介绍|无|
|motto|string|投资格言|无|
|relationId |string|同步系统关联老师ID| 无|

###webservice接口字段->MC字段###
	webservice接口字段					MC字段
	OtherDefine4			->			name
	Timage					->			photo	
	rsMainkeyID				->			groupBmId
	DJS						->			djs	
	rsProjectId				->			isExpert	   0 if rsProjectId else 1
							->			totalCapital	 # 总资产 = 剩余资金+冻结资金+总市值（） totalCapital = ResidualCapital + FrozenCapital + total_sz
							->			sz   从A_DxtWZWStock 取sz 求和
							->			cw	   # 当前仓位= 总市值/总资产    # 总资产 = 剩余资金+冻结资金+总市值（）
	OriginalCapital			->			originalCapital	  
							->			pm	  遍历所有老师  排序  获取当前排名   保存当前
							->			syl	   #收益率 = 总市值/本期起始资金 -1
	Tzsbh					->			certId
	Tfxsjs					->			desc
	Ttzgy					->			motto
							->			historyAccount   {}
	rsMainkeyID				->			relationId
																		
										
    self.totalCapital = DataObjArr["ResidualCapital"] + DataObjArr["FrozenCapital"] + self.total_sz


2、王中王赛榜
####描述####
王中王赛榜
###同步逻辑描述###

###webservice接口###
上月：Query_MNSBSYF  本月：Query_MNSB  赛季：Query_SJList
###表名###
A_DxtWZWRank
####字段说明####
|名称|类型|说明|缺省|
|--------|
|name|string|老师名称|无|
|photo|string|老师头像照片地址|无|
|groupBmId|number|当月王中王资金ID|无|
|teacherObjectId|string|王中王老师表ID。A_DxtWZWTeacher.ObjectId|无|
|djs|number|人气|无|
|totalCapital|number|总资产|无|
|sz|number|总市值|无|
|originalCapital|number|本期起始资金|无|
|pm|number|当月排行|无|
|syl|number|本月收益率|无|
|profitorLoss|number|本月盈亏|无|
|ljsy|number|累计收益|无|
|yearSyl|number|年收益率|无|
|season|number|赛季 0-本月赛季 -1 上月赛季 其他为赛季编号|无|
|relationId |string|同步系统关联ID| 无|

###上月赛榜###
###webservice接口字段->MC字段###
	webservice接口字段					MC字段
	username			->				name
	Vgroupid			->				groupBmId
	totalCapital		->				totalCapital
						->				pm   遍历  排序  获取当前排名
	ror					->				syl
	profitorLoss		->				profitorLoss
						->				season  -1
	Vgroupid			->				relationId
										
###本月赛榜###
###webservice接口字段->MC字段###
	webservice接口字段					MC字段
	nickname			->				name
	Vgroupid			->				groupBmId
	Djs					->				djs
	zjj					->				totalCapital
						->				pm   遍历  排序  获取当前排名
	YearSy				->				yearSyl
	bqsy				->				syl
						->				season   1
	Vgroupid			->				relationId
										
###赛季赛榜###
###webservice接口字段->MC字段###
	webservice接口字段					MC字段
	nickname			->				name
	Vgroupid			->				groupBmId
	counts				->				djs
	residualcapital		->				totalCapital
						->				pm		遍历  排序  获取当前排名
	bqsy				->				syl
	bqsy				->				profitorLoss
						->				season    通过 赛季列表 Query_SJLB 查询
	VGroupid			->				relationId
	

3、王中王赛季列表
####描述####
王中王赛季列表
###同步逻辑描述###

###webservice接口###
Query_SJLB
###表名###
A_DxtWZWSeason
####字段说明####
|名称|类型|说明|缺省|
|--------|
|name|string|赛季名称|无|
|season|number|赛季 0-本月赛季 -1 上月赛季 其他为赛季编号|无|
|relationId |string|同步系统关联ID| 无|

###webservice接口字段->MC字段###
	webservice接口字段					MC字段
										name
										season
										relationId
	同步接口返回
	{u'error_code': 0, u'data': [{u'SeasonId': 8}, {u'SeasonId': 7}, {u'SeasonId': 6}, {u'SeasonId': 5}, {u'SeasonId': 4}, {u'SeasonId': 3}, {u'SeasonId': 2}, {u'SeasonId': 1}], u'error': u'success'}
	

4、王中王投资列表
####描述####
王中王投资列表
###同步逻辑描述###

###webservice接口###
P_Z_uimsVSTSCD_pro
###表名###
A_DxtWZWInvest
####字段说明####
|名称|类型|说明|缺省|
|--------|
|groupBmId|number|当月王中王资金ID|无|
|teacherObjectId|string|王中王老师表ID。A_DxtWZWTeacher.ObjectId|无|
|stockCode |字符串|股票代码，例如600036| 无|
|stockName |字符串|股票名称，例如招商银行| 无|
|marketCode |字符串|市场代码，例如SH| 无|
|groupBmId|number|当月王中王资金ID|无|
|cjje|number|成交金额|无|
|price|number|成交价|无|
|syl|number|收益率|无|
|volume|number|成交股数|无|
|profitorLoss|number|本次盈亏|无|
|transType |字符串|买卖类型| 无|
|wtTime |Date|委托时间 对应otherdefine8| 无|
|dealTime |Date|成交时间 对应rsdatetime| 无|
|relationId |string|同步系统关联ID| 无|

###webservice接口字段->MC字段###
	webservice接口字段					MC字段
	VGroupID			->				groupBmId
						->				teacherObjectId   通过 VGroupID 获取老师表的 objectId
	stockcode			->				stockCode
	stockshortName		->				stockName
	MarketCode			->				marketCode
	cjje				->				cjje
	price				->				price
	syl					->				syl
	volume				->				volume
	profitorLoss		->				profitorLoss
	TransStyle			->				transType
	wtTime				->				wtTime
	CJDate				->				dealTime
	rsmainkeyid			->					relationId


	###王中王持仓列表###
####类名称####
A_DxtWZWStock
####描述####
王中王持仓列表
####字段说明####
|名称|类型|说明|缺省|
|--------|
|groupBmId|number|当月王中王资金ID|无|
|teacherObjectId|string|王中王老师表ID。A_DxtWZWTeacher.ObjectId|无|
|stockCode |字符串|股票代码，例如600036| 无|
|stockName |字符串|股票名称，例如招商银行| 无|
|marketCode |字符串|市场代码，例如SH| 无|
|marketName |字符串|市场名称，例如深证| 无|
|currentVolume|number|当前持仓股数|无|
|usevolume|number|当前可用股数|无|
|buyMonney|number|买入总价? 对应buymonney|无|
|cost|number|成本|无|
|price|number|成本价 对应cbj|无|
|stockId|number|股票Id|无|
|firstBuyDate |Date|第一次买入时间| 无|
|relationId |string|同步系统关联ID| 无|
	
	
5、王中王持仓列表
####描述####
王中王持仓列表
###同步逻辑描述###

###webservice接口###
P_Z_uimsVSTSC_pro
###表名###
A_DxtWZWStock
####字段说明####
|名称|类型|说明|缺省|
|--------|
|groupBmId|number|当月王中王资金ID|无|
|teacherObjectId|string|王中王老师表ID。A_DxtWZWTeacher.ObjectId|无|
|stockCode |字符串|股票代码，例如600036| 无|
|stockName |字符串|股票名称，例如招商银行| 无|
|marketCode |字符串|市场代码，例如SH| 无|
|marketName |字符串|市场名称，例如深证| 无|
|currentVolume|number|当前持仓股数|无|
|usevolume|number|当前可用股数|无|
|buyMonney|number|买入总价? 对应buymonney|无|
|cost|number|成本|无|
|price|number|成本价 对应cbj|无|
|stockId|number|股票Id|无|
|firstBuyDate |Date|第一次买入时间| 无|
|relationId |string|同步系统关联ID| 无|

###webservice接口字段->MC字段###
	webservice接口字段					MC字段
	VGroupID			->				groupBmId
						->				teacherObjectId   通过 VGroupID 获取老师表的 objectId
	stockcode			->				stockCode
	stockshortName		->				stockName
	MarketCode			->				marketCode
	cjje				->				currentVolume
	usevolume			->				usevolume
	BuyMonney			->				buyMonney
	Cost				->				cost
	cbj					->				price
	gpid				->				stockId
	FirstBuyDate		->				firstBuyDate
	rsmainkeyid			->				relationId
	

6、战绩快报列表
####描述####
战绩快报列表
###同步逻辑描述###

###webservice接口###
P_N_SSZJBB_WZW
###表名###
A_DxtWZWNews
####字段说明####
|名称|类型|说明|缺省|
|--------|
|groupBmId|number|当月王中王资金ID|无|
|teacherObjectId|string|王中王老师表ID。A_DxtWZWTeacher.ObjectId|无|
|stockCode |字符串|股票代码，例如600036| 无|
|stockName |字符串|股票名称，例如招商银行| 无|
|marketCode |字符串|市场代码，例如SH| 无|
|zdf |number|最大涨跌幅| 无|
|publishTime |datetime|发布时间 对应rsdatetime| 无|
|relationId |string|同步系统关联ID| 无|

###webservice接口字段->MC字段###
	webservice接口字段					MC字段
	VgroupID			->				groupBmId
						->				teacherObjectId	    通过 VGroupID 获取老师表的 objectId
	stockcode			->				stockCode
	stockshortName		->				stockName
	MarketCode			->				marketCode
	Price_ZDF			->				zdf
	rsdatetime			->				publishTime
	rsMainkeyID			->				relationId
    			
				
###王中王高手动态###
####类名称####
A_DxtWZWPlayerDyna
####描述####
王中王高手动态
####字段说明####
|名称|类型|说明|缺省|
|--------|
|groupBmId|number|当月王中王资金ID|无|
|stockCode |字符串|股票代码，例如600036| 无|
|stockName |字符串|股票名称，例如招商银行| 无|
|marketCode |字符串|市场代码，例如SH| 无|
|teacherName|字符串|选手名称|无|
|price|number|成交价|无|
|transType |字符串|买卖类型 ('买' '卖')| 无|
|dealTime |Date|成交时间 对应rsdatetime| 无|
|relationId |string|同步系统关联ID| 无|
			
			
7、王中王高手动态
####描述####
王中王高手动态
###同步逻辑描述###

###webservice接口###
P_Z_CommUserAlert_dx
###表名###
A_DxtWZWPlayerDyna
####字段说明####
|名称|类型|说明|缺省|
|--------|
|groupBmId|number|当月王中王资金ID|无|
|stockCode |字符串|股票代码，例如600036| 无|
|stockName |字符串|股票名称，例如招商银行| 无|
|marketCode |字符串|市场代码，例如SH| 无|
|teacherName|字符串|选手名称|无|
|price|number|成交价|无|
|transType |字符串|买卖类型 ('买' '卖')| 无|
|dealTime |Date|成交时间 对应rsdatetime| 无|
|relationId |string|同步系统关联ID| 无|

###webservice接口字段->MC字段###
	webservice接口字段					MC字段
	stockshortName		->				stockName
	UserName			->				teacherName
	cjj					->				price
	UserCZ				->				transType
	AlertNewsDate		->				dealTime
	rsMainkeyID			->				relationId
	


8、王中王实时战绩播报
####描述####
王中王实时战绩播报
###同步逻辑描述###

###webservice接口###
P_N_SSZJBB_WZW
###表名###
A_DxtWZWRealTimeReport
####字段说明####
|名称|类型|说明|缺省|
|--------|
|groupBmId|number|当月王中王资金ID|无|
|stockCode |字符串|股票代码，例如600036| 无|
|stockName |字符串|股票名称，例如招商银行| 无|
|marketCode |字符串|市场代码，例如SH| 无|
|teacherName|字符串|选手名称|无|
|profitorLoss|number|盈利|无|
|transType |字符串|买卖类型 ('买' '卖')| 无|
|dealTime |Date|成交时间 对应rsdatetime| 无|
|relationId |string|同步系统关联ID| 无|

###webservice接口字段->MC字段###
	webservice接口字段					MC字段
	stockcode			->				stockCode
	stockshortName		->				stockName
	NickName			->				teacherName
	OtherDefine3						profitorLoss
	Price_ZDF			->				transType    "买" if OtherDefine2 > 0 else "卖
	rsDateTime			->				dealTime
	

9、王中王牛股英雄榜
####描述####
王中王牛股英雄榜
###同步逻辑描述###

###webservice接口###
Query_StockNGB
###表名###
A_DxtWZWBestStockRange
####字段说明####
|名称|类型|说明|缺省|
|--------|
|stockCode |字符串|股票代码，例如600036| 无|
|stockName |字符串|股票名称，例如招商银行| 无|
|marketCode |字符串|市场代码，例如SH| 无|
|inPrice|number|买入价|无|
|zdf |number|最大涨跌幅| 无|
|dealTime |Date|时间| 无|
|relationId |string|同步系统关联ID| 无|

###webservice接口字段->MC字段###
	webservice接口字段					MC字段
	stockcode			->				stockCode
	stockshortName		->				stockName
	Price				->				inPrice
	Price_ZDF							zdf
	StockID				->				StockID
	TransDate			->				dealTime




    		