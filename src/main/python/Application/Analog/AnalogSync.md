###CJS 同步程序逻辑描述文档###

1、Position
####描述####
资金持仓数据同步
###同步逻辑描述###

###webservice接口###
Query_uimsStockTransList
###表名###
AnalogStock
####字段说明####
|----|----|
|名称|类型|说明|缺省|
|userObjectId |字符串|BOSS系统用户objectid| 无|
|userName |字符串|BOSS系统用户名称| 无|
|analogUserId |数字|模拟炒股系统用户id| 无|
|matchObjectId |字符串|BOSS系统大赛的ojectid| 无|
|matchName |字符串|BOSS系统大赛名称| 无|
|analogMatchId |数字|模拟炒股系统大赛id| 无|
|groupBmId |数字|模拟炒股系统资金id| 无|
|stockCode |字符串|股票代码，例如600036| 无|
|stockName |字符串|股票名称| 无|
|stockTypeName |字符串|股票类型名称，例如A股| 无|
|marketCode |字符串|市场代码，例如SH| 无|
|marketName |字符串|市场名称，例如上海| 无|
|totalVolume |数字|持仓股数| 无|
|useVolume |数字|可用股数| 无|
|price |数字|成本价格| 无|
|cost |数字|购买成本| 无|
|profitorLoss |数字|盈亏| 无|
|buyMoney |数字|购买成本，目前以cost为准，本字段暂不使用| 无|
|headImageUrl |字符串|用户头像| 无|

###webservice接口字段->MC字段###
	webservice接口字段		MC字段
					->     userObjectId   		（由AnalogMyMatch表获取userObjectId）
	ZhName	        ->     userName
					->     analogUserId  	 	（由AnalogMyMatch表获取analogUserId）
					->     matchObjectId 		（由AnalogMyMatch表获取matchObjectId）
					->     matchName     		（由AnalogMyMatch表获取matchName）
					->     analogMatchId 		（由AnalogMyMatch表获取analogMatchId）
	VGroupid        ->     groupBmId
	StockCode       ->     stockCode
	stockname       ->     stockName
	stockTypeName   ->     stockTypeName
	marketCode      ->     marketCode
	marketName      ->     marketName
	CurrentVolume   ->     totalVolume
	UseVolume       ->     useVolume
					->     price        （计算）
	cost            ->     cost
	ProfitorLoss    ->     profitorLoss
    BuyMoney        ->     buyMoney
    headImageUrl    ->     headImageUrl

###表名###
AnalogMyMatch
####字段说明####
|----|----|
|名称|类型|说明|缺省|
|userObjectId |字符串|BOSS系统用户objectid| 无|
|userName |字符串|BOSS系统用户名称| 无|
|analogUserId |数字|模拟炒股系统用户id| 无|
|matchObjectId |字符串|BOSS系统大赛的ojectid| 无|
|matchName |字符串|BOSS系统大赛名称| 无|
|analogMatchId |数字|模拟炒股系统大赛id| 无|
|beginTime |Date|开始日期| 无|
|endTime |Date|结束日期| 无|
|groupBmId |数字|模拟炒股系统资金id| 无|
|pm |数字|排名| 无|
|pmDay |数字|日排名| 无|
|pmWeek |数字|周排名| 无|
|syl |字符串|收益率| 无|
|sylDay |字符串|日收益率| 无|
|sylWeek |字符串|周收益率| 无|
|shouYiLv |数字|收益率| 无|
|shouYiLvDay |数字|日收益率| 无|
|shouYiLvWeek |数字|周收益率| 无|
|originalCapital |数字|原始资金| 无|
|residualCapital |数字|剩余资金| 无|
|frozenCapital |数字|冻结资金| 无|
|tradeTotal |数字|操作数| 无|
|tradeCountYL |数字|盈利操作数| 无|
|myPopularity |数字|人气，即被关注数| 无|
|totalProfitorLoss |数字|总盈亏| 无|
|isDefault |字符串|模拟炒股标志 1模拟炒股 其他 炒股大赛| 无|
|headImageUrl |字符串|用户头像| 无|

###webservice接口字段->MC字段###
	webservice接口字段		MC字段
						->     userObjectId   		（由_User表获取userId）
	ZhName	    		->     userName
						->     analogUserId  	 	（由AnalogMyMatch表获取analogUserId）
						->     matchObjectId 		（由AnalogMyMatch表获取matchObjectId）
						->     matchName     		（由AnalogMyMatch表获取matchName）
						->     analogMatchId 		（由AnalogMyMatch表获取analogMatchId）
						->	   beginTime        	（由AnalogMyMatch表获取analogMatchId）
	endTime             ->     endTime
	VGroupid            ->     groupBmId
	pm_all              ->     pm
	pm_Day              ->     pmDay
	pm_week             ->     pmWeek
	syl_all             ->     syl
	syl_day             ->     sylDay
	syl_week            ->     sylWeek
	syl_all             ->     shouYiLv
	syl_day	            ->     shouYiLvDay
	syl_week            ->     shouYiLvWeek
	OriginalCapital     ->     originalCapital
	ResidualCapital     ->     residualCapital
	FrozenCapital       ->     frozenCapital
	tradeTotal          ->     tradeTotal
	tradeCount          ->     tradeCountYL
	myPopularity        ->     myPopularity
	totalProfitorLoss   ->     totalProfitorLoss
						->     isDefault        (0)
	headImageUrl        ->     headImageUrl     	（由_User表获取headImageUrl）


2、Order
####描述####
成交数据同步
###同步逻辑描述###

###webservice接口###
Query_uimsStockTransDataSetList
###表名###
AnalogOrder
####字段说明####
|----|----|
|名称|类型|说明|缺省|
|userObjectId |字符串|BOSS系统用户objectid| 无|
|userName |字符串|BOSS系统用户名称| 无|
|analogUserId |数字|模拟炒股系统用户id| 无|
|matchObjectId |字符串|BOSS系统大赛的ojectid| 无|
|matchName |字符串|BOSS系统大赛名称| 无|
|analogMatchId |数字|模拟炒股系统大赛id| 无|
|groupBmId |数字|模拟炒股系统资金id| 无|
|mainKeyId |数字|模拟炒股系统委托id| 无|
|stockCode |字符串|股票代码，例如600036| 无|
|stockName |字符串|股票名称，例如招商银行| 无|
|marketCode |字符串|市场代码，例如SH| 无|
|price |数字|成交价格| 无|
|volume |数字|成交股数| 无|
|cjje |数字|成交价格| 无|
|transType |字符串|买卖类型| 无|
|dealTime |Date|成交时间| 无|
|profitorLoss |数字|收益值| 无|
|syl |字符串|收益率| 无|
|headImageUrl |字符串|用户头像| 无|

###webservice接口字段->MC字段###
	webservice接口字段		MC字段
					->     userObjectId   		（由AnalogMyMatch表获取userObjectId）
	ZhName	        ->     userName
					->     analogUserId  	 	（由AnalogMyMatch表获取analogUserId）
					->     matchObjectId 		（由AnalogMyMatch表获取matchObjectId）
					->     matchName     		（由AnalogMyMatch表获取matchName）
					->     analogMatchId 		（由AnalogMyMatch表获取analogMatchId）
	VGroupid        ->     groupBmId
	TransRecordId   ->     mainKeyId
	StockCode       ->     stockCode
	stockname       ->     stockName
	marketcode      ->     marketCode
	Price           ->     price
	Volume          ->     volume
					->     cjje   （计算）
	transType       ->     transType	 (转换1：买   0：卖)
	cjdatetime      ->     dealTime
	ProfitorLoss    ->     profitorLoss
	syl             ->     syl
					->     headImageUrl  （从AnalogMyMatch表获取headImageUrl）


3、Range
####描述####
排名数据同步
###同步逻辑描述###

###webservice接口###
Query_uimsSYPM
###表名###
AnalogRange
####字段说明####
|----|----|
|名称|类型|说明|缺省|
|userObjectId |字符串|BOSS系统用户objectid| 无|
|userName |字符串|BOSS系统用户名称| 无|
|headImageUrl |字符串|头像| 无|
|groupBmId |数字|模拟炒股系统资金id| 无|
|pm |数字|排名| 无|
|syl |字符串|收益率| 无|
|type |数字|排名类型 1日排名 2周排名 3总排名 | 无|
|totalCapital |数字|总资产 | 无|
|cgl |数字|持股量 | 无|
|groupBm |字符串|报名名称 | 无|
|djs |数字|点击数| 无|
|shouYiLv |数字|收益率 | 无|
|originalCapital |数字|原始资金| 无|
|cw |数字|仓位 | 无|

###webservice接口字段->MC字段###
	webservice接口字段			MC字段
						->	  	userObjectId 	 (从AnalogMyMatch表获取userObjectId)
	groupbm	            ->		userName
						->		headImageUrl      (从AnalogMyMatch表获取headImageUrl)
	vgroupid	        ->		groupBmId
	pm                  ->		pm
	ror                 ->		syl
	pmType              ->		type
	EndCaptial	        ->		totalCapital
	cgl                 ->		cgl
	groupbm             ->		groupBm
	djs                 ->		djs
	ror		            ->		shouYiLv
	originalCapital     ->		originalCapital
	cw                  ->		cw

4、Speech
####描述####
获奖感言同步
###同步逻辑描述###
每月最后一天的16点30更新 返回最新的获奖感言数据

###webservice接口###
Query_uimsHJGY
###表名###
uimsHJGY
####字段说明####

###webservice接口字段->MC字段###
	webservice接口字段			MC字段
		BlogAddress		->	  BlogAddress
		rsMainkeyID     ->    rsMainkeyID
		Ror             ->    Ror
		rsOperateID     ->    rsOperateID
		rsStatus        ->    rsStatus
		shouyi          ->    shouyi
		rsProjectId     ->    rsProjectId
		PlatForms       ->    PlatForms
		FbTime          ->    FbTime
		ZhName          ->    ZhName
		VGroupId        ->    VGroupId
		rsDateTime      ->    rsDateTime
		rsDispIndex     ->    rsDispIndex
		Picture         ->    Picture

5、HistRank
####描述####
历史排名同步
###同步逻辑描述###
每月最后一天的16点30更新最新的历史排名数据

###webservice接口###
Query_uimsLSPM
###表名###
uimsLSPM
####字段说明####

###webservice接口字段->MC字段###
	webservice接口字段			MC字段
	rsOperateID			->	  rsOperateID
	rsStatus            ->    rsStatus
	rsProjectId         ->    rsProjectId
	rsMainkeyID         ->    rsMainkeyID
	rsDateTime          ->    rsDateTime
	rsDispIndex         ->    rsDispIndex
	cgl                 ->    cgl
	allmoney            ->    allmoney
	vgroupid            ->    vgroupid
	dqyl                ->    dqyl
	pm                  ->    pm
	djs                 ->    djs
	groupbm             ->    groupbm
	getedPer            ->    getedPer
	gzz                 ->    gzz
	tradeDate			->	  tradeDate


6、Comment
####描述####
专家点评同步
###同步逻辑描述###
每天16点30更新专家点评数据

###webservice接口###
Query_uimsZJDP
###表名###
uimsZJDP
####字段说明####

###webservice接口字段->MC字段###
	webservice接口字段			MC字段
	rsOperateID		->		rsOperateID
	rsStatus        ->      rsStatus
	rsProjectId     ->      rsProjectId
	getedPer        ->      getedPer
	rsMainkeyID     ->      rsMainkeyID
	pm              ->      pm
	groupbm         ->      groupbm
	JudgeConten     ->      JudgeConten
	rsDateTime      ->      rsDateTime
	rsDispIndex     ->      rsDispIndex
	TradeDate       ->      TradeDate

7、Season
####描述####
赛季同步
###同步逻辑描述###
每月最后一天的16点30更新最新赛季数据

###webservice接口###
Query_uimsSEASONSET
###表名###
uimsSeasonSet
####字段说明####

###webservice接口字段->MC字段###
	webservice接口字段			MC字段
	rsOperateID		->		 rsOperateID
	rsStatus        ->       rsStatus
	rsProjectId     ->       rsProjectId
	rsMainkeyID     ->       rsMainkeyID
	rsDateTime      ->       rsDateTime
	rsDispIndex     ->       rsDispIndex
	SeasonId        ->       SeasonId
	GroupStyle      ->       GroupStyle
	StartDate       ->       StartDate
	EndDate         ->       EndDate


8、NiuguList
牛股榜同步
###同步逻辑描述###
每天16点30更新最新牛股榜数据

###webservice接口###
Query_uimsNGB
###表名###
uimsNGB
####字段说明####

###webservice接口字段->MC字段###
	webservice接口字段			MC字段
	rsOperateID 	->		 rsOperateID
	rsStatus        ->       rsStatus
    rsProjectId     ->       rsProjectId
    rsMainkeyID     ->       rsMainkeyID
    rsDateTime      ->       rsDateTime
    rsDispIndex     ->       rsDispIndex
    stockShortname  ->       stockShortname
    ownerCount      ->       ownerCount
    avgPrize        ->       avgPrize
    groupbm         ->       groupbm
    StockCode       ->       StockCode
    Stockid         ->       Stockid

9、RecordVideo
CCTV同步
###同步逻辑描述###


###webservice接口###
P_Z_video
###表名###
A_DxtRecordVideo
####字段说明####

###webservice接口字段->MC字段###
	webservice接口字段			MC字段
	title				->	   title
	desc                ->     content
	videoType           ->     className
	sourceType          ->     classId
	videoImage          ->     pictureH5Url
    pictureH5Url        ->     pictureH5Url
    videoUrl            ->  	url
    videoH5Url          ->     h5url
    teacherName         ->     teachername
    videoSource         ->     sply
    status              ->     shzt
    isDisable           ->     sfjy
    isTop               ->     isTop
    clickNumber         ->     hits
    collectNumber       ->     dscs
    clickNumberActual   ->     sjdjs
    collectNumberActual ->     sjscs
    relationId          ->     rsMainKeyId