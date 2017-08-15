
1、自主新闻查询
####描述####
资讯数据同步
###同步逻辑描述###

###webservice接口###
Query_CommNews_EDIT
###表名###
A_DxtInformation
####字段说明####
|名称|类型|说明|缺省|
|--------|
|title|string|资讯标题|无|
|source|string|资讯来源|无|
|summary|string|资讯摘要|无|
|thumbnail|string|缩略图url地址|无|
|url|string|网页跳转地址|无|
|content|string|处理过后的内容，填充为同步过来后经过处理的文本内容。|无|
|srcContent|string|源内容，填充为同步过来的原始文本内容。|无|
|categories|array|渠道或类型，如为二级分类则用"-"分隔一级分类和二级分类，数据示例如[ "头条-列表", "涨价专题" ]|无|
|labels|array|标签数组|无|
|isDisable |number|是否禁用 0不禁用 1禁用|0|
|correlatedStocks|array|相关股票数组|无|  从CommNews_EDIT 中xggg
|correlatedStocks.code|string|股票代码|无|
|correlatedStocks.name|string|股票名称|无|
|correlatedStocks.market|string|股票市场|无|
|author|string|作者|无|
|publishTime |datetime|发布时间| 无|
|clickNumber |number|点击数|0|
|likeNumber |number|好评数|0|
|shareNumber |number|分享数|0|
|collectNumber |number|收藏数|0|
|relationId |string|同步系统关联ID| 无|

###webservice接口字段->MC字段###
	webservice接口字段				MC字段
						->			sync      1
NewsTitle				->			title
OtherDefine2	        ->       	source
NewsBrief	            ->       	summary
OtherDefine1	        ->      	thumbnail
OtherDefine4            ->       	url
OtherDefine4 			->			pcUrl
NewsContent		        ->     		content
NewsContent	            ->     		srcContent
xggg					->			correlatedStockStr
NewsStyle	            ->       	categories
NewsStyle/xghy(主题投资)->      	labels
isDisable	            ->       	isDisable
OtherDefine2            ->      	author
NewsDate                ->      	publishTime
						->			clickNumber		0
	                    ->       	likeNumber		0
	                    ->       	shareNumber		0
	                    ->       	collectNumber    0
rsMainkeyID             ->       	relationId
						-> 			contentDealStatus    0
	                    ->         	CDNStatus			0
	                    ->         	imgCDNStatus		0



2、 钱坤晨会查询
####描述####
钱坤晨会查询同步
###同步逻辑描述###

###webservice接口###
Query_sirsReportRemark
###表名###
A_DxtInformation
####字段说明####
|名称|类型|说明|缺省|
|--------|
|title|string|资讯标题|无|
|source|string|资讯来源|无|
|summary|string|资讯摘要|无|
|thumbnail|string|缩略图url地址|无|
|url|string|网页跳转地址|无|
|content|string|处理过后的内容，填充为同步过来后经过处理的文本内容。|无|
|srcContent|string|源内容，填充为同步过来的原始文本内容。|无|
|categories|array|渠道或类型，如为二级分类则用"-"分隔一级分类和二级分类，数据示例如[ "头条-列表", "涨价专题" ]|无|
|labels|array|标签数组|无|
|isDisable |number|是否禁用 0不禁用 1禁用|0|
|correlatedStocks|array|相关股票数组|无|  从CommNews_EDIT 中xggg
|correlatedStocks.code|string|股票代码|无|
|correlatedStocks.name|string|股票名称|无|
|correlatedStocks.market|string|股票市场|无|
|author|string|作者|无|
|publishTime |datetime|发布时间| 无|
|clickNumber |number|点击数|0|
|likeNumber |number|好评数|0|
|shareNumber |number|分享数|0|
|collectNumber |number|收藏数|0|
|relationId |string|同步系统关联ID| 无|

###webservice接口字段->MC字段###
	webservice接口字段				MC字段
						->			sync      3
AttachTitle				->			title
						->       	source   ""
						->       	summary		""
OtherDefine8	        ->      	thumbnail
OtherDefine4            ->       	url
OtherDefine4 			->			pcUrl
AttachContent		    ->     		content
AttachContent	        ->     		srcContent
RemarkClass	            ->       	categories
RemarkClass				->      	labels
isDisable	            ->       	isDisable
RemarkMan           	->      	author
RemarkTime              ->      	publishTime
						->			clickNumber		0
	                    ->       	likeNumber		0
	                    ->       	shareNumber		0
	                    ->       	collectNumber    0
rsMainkeyID             ->       	relationId
						-> 			contentDealStatus    0
	                    ->         	CDNStatus			0
	                    ->         	imgCDNStatus		0
AttachFile				->			AttachFile
AttachPath              ->         	AttachPath


3、 财富快线新闻主表查询
####描述####
财富快线新闻主表查询同步
###同步逻辑描述###

###webservice接口###
Query_jx_News
###表名###
A_DxtInformation
####字段说明####
|名称|类型|说明|缺省|
|--------|
|title|string|资讯标题|无|
|source|string|资讯来源|无|
|summary|string|资讯摘要|无|
|thumbnail|string|缩略图url地址|无|
|url|string|网页跳转地址|无|
|content|string|处理过后的内容，填充为同步过来后经过处理的文本内容。|无|
|srcContent|string|源内容，填充为同步过来的原始文本内容。|无|
|categories|array|渠道或类型，如为二级分类则用"-"分隔一级分类和二级分类，数据示例如[ "头条-列表", "涨价专题" ]|无|
|labels|array|标签数组|无|
|isDisable |number|是否禁用 0不禁用 1禁用|0|
|correlatedStocks|array|相关股票数组|无|  从CommNews_EDIT 中xggg
|correlatedStocks.code|string|股票代码|无|
|correlatedStocks.name|string|股票名称|无|
|correlatedStocks.market|string|股票市场|无|
|author|string|作者|无|
|publishTime |datetime|发布时间| 无|
|clickNumber |number|点击数|0|
|likeNumber |number|好评数|0|
|shareNumber |number|分享数|0|
|collectNumber |number|收藏数|0|
|relationId |string|同步系统关联ID| 无|

###webservice接口字段->MC字段###
	webservice接口字段				MC字段
						->			sync      2
NewsTitle				->			title
NewsSource				->       	source
						->       	summary		""
NewsImage	        	->      	thumbnail
						->       	url     ""
NewsContent		    	->     		content
NewsContent	        	->     		srcContent
CalssID	            	->       	categories
CalssID					->      	labels
isDisable	            ->       	isDisable
NewsAuthor           	->      	author
NewsTime              	->      	publishTime
						->			clickNumber		0
	                    ->       	likeNumber		0
	                    ->       	shareNumber		0
	                    ->       	collectNumber    0
rsMainkeyID             ->       	relationId
						-> 			contentDealStatus    0
	                    ->         	CDNStatus			0
	                    ->         	imgCDNStatus		0


4、 技术学堂表
####描述####
技术学堂表同步
###同步逻辑描述###

###webservice接口###
Query_CommNews_Extract
###表名###
A_DxtInformation
####字段说明####
|名称|类型|说明|缺省|
|--------|
|title|string|资讯标题|无|
|source|string|资讯来源|无|
|summary|string|资讯摘要|无|
|thumbnail|string|缩略图url地址|无|
|url|string|网页跳转地址|无|
|content|string|处理过后的内容，填充为同步过来后经过处理的文本内容。|无|
|srcContent|string|源内容，填充为同步过来的原始文本内容。|无|
|categories|array|渠道或类型，如为二级分类则用"-"分隔一级分类和二级分类，数据示例如[ "头条-列表", "涨价专题" ]|无|
|labels|array|标签数组|无|
|isDisable |number|是否禁用 0不禁用 1禁用|0|
|correlatedStocks|array|相关股票数组|无|  从CommNews_EDIT 中xggg
|correlatedStocks.code|string|股票代码|无|
|correlatedStocks.name|string|股票名称|无|
|correlatedStocks.market|string|股票市场|无|
|author|string|作者|无|
|publishTime |datetime|发布时间| 无|
|clickNumber |number|点击数|0|
|likeNumber |number|好评数|0|
|shareNumber |number|分享数|0|
|collectNumber |number|收藏数|0|
|relationId |string|同步系统关联ID| 无|

###webservice接口字段->MC字段###
	webservice接口字段				MC字段
						->			sync      4
NewsTitle				->			title
NewsSource				->       	source  
						->       	summary		""
						->      	thumbnail     ""
OtherDefine4			->       	url    
OtherDefine4			-> 			pcUrl
NewsContent		    	->     		content
NewsContent	        	->     		srcContent
NewsStyle				->			NewsStyle
ClassName	            ->       	categories
ClassName				->      	labels
rsStatus	            ->       	isDisable    	0 if rsStatus> 0  else  1
NewsAuthor           	->      	author
NewsDate[:-5]           ->      	publishTime
OtherDefine1			->			clickNumber		0
OtherDefine3	        ->       	likeNumber		0
	                    ->       	shareNumber		0
OtherDefine2	        ->       	collectNumber    0
rsMainkeyID             ->       	relationId
						-> 			contentDealStatus    0
	                    ->         	CDNStatus			0
	                    ->         	imgCDNStatus		0



