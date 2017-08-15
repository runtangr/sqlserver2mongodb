
1、股票池列表
####描述####
股票池列表同步
###同步逻辑描述###

###webservice接口###
P_Z_CommStockZB
###表名###
A_DxtStockPool
####字段说明####
|名称|类型|说明|缺省|
|--------|
|name|string|股票池名称|无|
|stockCLFG|array|策略风格，同步时将“强势,长线,激进,主题跟踪”拆分成数组|无|
|stockCLFKYL|string|策略风控盈利，由“止盈:盈利≥30%,止损：止损≥15%” 这样的数据进行拆分|无|
|stockCLFKZS|string|策略风控止损，由“止盈:盈利≥30%,止损：止损≥15%” 这样的数据进行拆分|无|
|stockType|string|类型|无|
|stockTP|string|图片，暂存不处理|无|
|stockPJSY|number|平均收益|无|
|stockZGZF|number|最高涨幅，接口暂无该字段，需要接口进行补充|无|
|stockXGMX|string|选股模型，暂存不处理|无|
|relationId |string|同步系统关联ID| 无|
|rsProjectId |int|0显示 -1 不显示

###webservice接口字段->MC字段###
	webservice接口字段					MC字段
	StockZBName					->		name
	StockCLFK.split(',')		->		stockCLFG
	StockCLFK.split(',')[0]		->		stockCLFKYL
	StockCLFK.split(',')[1]		->		stockCLFKZS
	StockType					->		stockType
	StockTP						->		stockTP
	StockPJSY					->		stockPJSY
	StockPJSY					->		stockZGZF
	StockSGMX					->		stockXGMX
	isDisable					->		isDisable
	rsMainkeyID					->		relationId


2、股票池股票
####描述####
股票池股票同步
###同步逻辑描述###

###webservice接口###
P_Z_CommStockPool
###表名###
A_DxtStockPoolStock
####字段说明####
|名称|类型|说明|缺省|
|--------|
|stockPoolObjectId|string|股票池ID|无|
|stockCode|string|股票代码|无|
|stockName|string|股票名称|无|
|marketCode|string|市场代码|无|
|cqPrice|number|除权价格|无|
|targetPrice|number|目标价格|无|
|zsPrice|number|止损价格|无|
|inPrice|number|入池价格|无|
|bestAvail|number|最高收益|无|
|stockComeFrom|string|推荐机构|无|
|stockId|number|股票ID|无|
|inTime |datetime|发布时间，对应websercie的AccessDateTime| 无|
|relationId |string|同步系统关联ID| 无|
|rsStatus | int	|状态  10入池 20 出池


###webservice接口字段->MC字段###
	webservice接口字段					MC字段
						->			stockPoolObjectId     PoolStyle 匹配A_DxtStockPool relationId  查询objiectid
	StockCode			->			stockCode
	StockShortName		->			stockName
	MarketCode			->			marketCode
	CQPrice				->			cqPrice
	TargetPrice			->			targetPrice
	ZSPrice				->			zsPrice
	AccessPrice			->			inPrice
	Dqsy				->			bestAvail
	StockComeFrom		->			stockComeFrom
	stockId 			->			stockId
	AccessDateTime		->			inTime
	rsMainkeyID			->			relationId
	rsStatus			->			rsStatus



3、月最高涨幅榜
####描述####
月最高涨幅榜同步
###同步逻辑描述###

###webservice接口###
Query_YZGZF
###表名###
A_DxtStockPoolMonthRank
####字段说明####
|名称|类型|说明|缺省|
|--------|
|stockPoolObjectId|string|股票池ID|无|
|stockCode|string|股票代码|无|
|stockName|string|股票名称|无|
|marketCode|string|市场代码|无|
|cqPrice|number|除权价格|无|
|dqsy|number|区间最高收益|无|
|inPrice|number|入池价格|无|
|stockComeFrom|string|推荐机构|无|
|inTime |datetime|发布时间，对应websercie的AccessDateTime| 无|
|relationId |string|同步系统关联ID| 无|


###webservice接口字段->MC字段###
	webservice接口字段					MC字段
						->			stockPoolObjectId     PoolStyle 匹配A_DxtStockPool relationId  查询objiectid
	StockCode			->			stockCode
	StockShortName		->			stockName
	MarketCode			->			marketCode
	CQPrice				->			cqPrice
	Dqsy				->			dqsy
	AccessPrice			->			inPrice
	StockComeFrom		->			stockComeFrom
	AccessDateTime		->			inTime
	rsMainkeyID			->			relationId


###年最高涨幅榜###
####类名称####
A_DxtStockPoolYearRank
####描述####
年最高涨幅榜
####字段说明####
|名称|类型|说明|缺省|
|--------|
|stockPoolObjectId|string|股票池ID|无|
|stockCode|string|股票代码|无|
|stockName|string|股票名称|无|
|marketCode|string|市场代码|无|
|cqPrice|number|除权价格|无|
|dqsy|number|区间最高收益|无|
|inPrice|number|入池价格|无|
|stockComeFrom|string|推荐机构|无|
|inTime |datetime|发布时间，对应websercie的AccessDateTime| 无|
|relationId |string|同步系统关联ID| 无|


3、年最高涨幅榜
####描述####
年最高涨幅榜同步
###同步逻辑描述###

###webservice接口###
Query_NZGZF
###表名###
A_DxtStockPoolYearRank
####字段说明####
|名称|类型|说明|缺省|
|--------|
|stockPoolObjectId|string|股票池ID|无|
|stockCode|string|股票代码|无|
|stockName|string|股票名称|无|
|marketCode|string|市场代码|无|
|cqPrice|number|除权价格|无|
|dqsy|number|区间最高收益|无|
|inPrice|number|入池价格|无|
|stockComeFrom|string|推荐机构|无|
|inTime |datetime|发布时间，对应websercie的AccessDateTime| 无|
|relationId |string|同步系统关联ID| 无|


###webservice接口字段->MC字段###
	webservice接口字段					MC字段
						->			stockPoolObjectId     PoolStyle 匹配A_DxtStockPool relationId  查询objiectid
	StockCode			->			stockCode
	StockShortName		->			stockName
	MarketCode			->			marketCode
	CQPrice				->			cqPrice
	Dqsy				->			dqsy
	AccessPrice			->			inPrice
	StockComeFrom		->			stockComeFrom
	AccessDateTime		->			inTime
	rsMainkeyID			->			relationId

	###股票池日总结###
####类名称####
A_DxtStockPoolDiary
####描述####
股票池日总结
####字段说明####
|名称|类型|说明|缺省|
|--------|
|stockPoolObjectId|string|股票池ID|无|
|title|string|标题|无|
|content|string|内容|无|
|publishTime |datetime|发布时间，对应websercie的NewsDate| 无|
|relationId |string|同步系统关联ID| 无|

4、股票池日总结
####描述####
股票池日总结同步
###同步逻辑描述###

###webservice接口###
Query_CommNews_EDIT
###表名###
A_DxtStockPoolDiary
####字段说明####
|名称|类型|说明|缺省|
|--------|
|stockPoolObjectId|string|股票池ID|无|
|title|string|标题|无|
|content|string|内容|无|
|publishTime |datetime|发布时间，对应websercie的NewsDate| 无|
|relationId |string|同步系统关联ID| 无|

## 通过 NewsStyle
###webservice接口字段->MC字段###
	webservice接口字段					MC字段
						->			stockPoolObjectId     PoolStyle 匹配A_DxtStockPool relationId  查询objiectid
	NewsTitle			->			title
	NewsContent			->			content
	NewsDate[:-5]		->			publishTime
	rsMainkeyID			->			relationId



5、股票池最近出池
####描述####
股票池最近出池同步
###同步逻辑描述###

###webservice接口###
Query_ZJCC
###表名###
A_DxtStockPoolOut
####字段说明####
|名称|类型|说明|缺省|
|--------|
|stockPoolObjectId|string|股票池ID|无|
|stockCode|string|股票代码|无|
|stockName|string|股票名称|无|
|marketCode|string|市场代码|无|
|cqPrice|number|除权价格|无|
|outPrice|number|入池价格|无|
|dqsy|number|区间最高收益|无|
|inPrice|number|入池价格|无|
|stockComeFrom|string|推荐机构|无|
|inDateTime |datetime|发布时间，对应websercie的AccessDateTime| 无|
|outDateTime |datetime|发布时间，对应websercie的OutDateTime| 无|
|stockId|number|股票ID|无|
|relationId |string|同步系统关联ID| 无|


###webservice接口字段->MC字段###
	webservice接口字段					MC字段
						->			stockPoolObjectId     PoolStyle 匹配A_DxtStockPool relationId  查询objiectid
	StockCode			->			stockCode
	StockShortName		->			stockName
	MarketCode			->			marketCode
	CQPrice				->			cqPrice
	OutPrice			->			outPrice
	Dqsy				->			dqsy
	AccessPrice			->			inPrice
	StockComeFrom		->			stockComeFrom
	AccessDateTime		->			inDateTime
	OutDateTime			->			outDateTime
	stockId				->			stockId
	rsMainkeyID			->			relationId


###股票池近期更新(操作日志)###
####类名称####
A_DxtStockPoolOptLog
####描述####
股票池近期更新(操作日志)
####字段说明####
|名称|类型|说明|缺省|
|--------|
|stockPoolObjectId|string|股票池ID|无|
|stockCode|string|股票代码|无|
|stockName|string|股票名称|无|
|marketCode|string|市场代码|无|
|title|string|标题|无|
|content|string|内容|无|
|optType|number|类型(10.买入 20.持有 30.卖出)|无|
|optTypeStr|string|类型(买入/持有/卖出)|无|
|publishTime |datetime|发布时间，对应websercie的rsDateTime| 无|
|relationId |string|同步系统关联ID| 无|


5、股票池近期更新(操作日志)
####描述####
股票池近期更新(操作日志)同步
###同步逻辑描述###

###webservice接口###
A_DxtStockPoolOptLog
###表名###
A_DxtStockPoolOut
####字段说明####
|名称|类型|说明|缺省|
|--------|
|stockPoolObjectId|string|股票池ID|无|
|stockCode|string|股票代码|无|
|stockName|string|股票名称|无|
|marketCode|string|市场代码|无|
|title|string|标题|无|
|content|string|内容|无|
|optType|number|类型(10.买入 20.持有 30.卖出)|无|
|optTypeStr|string|类型(买入/持有/卖出)|无|
|publishTime |datetime|发布时间，对应websercie的rsDateTime| 无|
|relationId |string|同步系统关联ID| 无|


###webservice接口字段->MC字段###
	webservice接口字段					MC字段
						->			stockPoolObjectId     PoolStyle 匹配A_DxtStockPool relationId  查询objiectid
	StockCode			->			stockCode
	StockShortName		->			stockName
	LogTitle			->			title
	LogContent			->			content
	LogStyle			->			optType
	LogStyle 转换		->			optTypeStr   { 10:"买入",20:"持有",30:"卖出"}
	rsDateTime			->			publishTime
	rsMainkeyID			->			relationId








