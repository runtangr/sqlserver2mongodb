###CJS ͬ�������߼������ĵ�###

1��Position 
####����####
�ʽ�ֲ�����ͬ�� 
###ͬ���߼�����###

###webservice�ӿ�###
Query_uimsStockTransList
###����###
AnalogStock
####�ֶ�˵��####
|----|----|
|����|����|˵��|ȱʡ|
|userObjectId |�ַ���|BOSSϵͳ�û�objectid| ��|
|userName |�ַ���|BOSSϵͳ�û�����| ��|
|analogUserId |����|ģ�⳴��ϵͳ�û�id| ��|
|matchObjectId |�ַ���|BOSSϵͳ������ojectid| ��|
|matchName |�ַ���|BOSSϵͳ��������| ��|
|analogMatchId |����|ģ�⳴��ϵͳ����id| ��|
|groupBmId |����|ģ�⳴��ϵͳ�ʽ�id| ��|
|stockCode |�ַ���|��Ʊ���룬����600036| ��|
|stockName |�ַ���|��Ʊ����| ��|
|stockTypeName |�ַ���|��Ʊ�������ƣ�����A��| ��|
|marketCode |�ַ���|�г����룬����SH| ��|
|marketName |�ַ���|�г����ƣ������Ϻ�| ��|
|totalVolume |����|�ֲֹ���| ��|
|useVolume |����|���ù���| ��|
|price |����|�ɱ��۸�| ��|
|cost |����|����ɱ�| ��|
|profitorLoss |����|ӯ��| ��|
|buyMoney |����|����ɱ���Ŀǰ��costΪ׼�����ֶ��ݲ�ʹ��| ��|
|headImageUrl |�ַ���|�û�ͷ��| ��|

###webservice�ӿ��ֶ�->MC�ֶ�###
	webservice�ӿ��ֶ�		MC�ֶ�
					->     userObjectId   		����AnalogMyMatch���ȡuserObjectId��
	ZhName	        ->     userName      
					->     analogUserId  	 	����AnalogMyMatch���ȡanalogUserId��
					->     matchObjectId 		����AnalogMyMatch���ȡmatchObjectId��
					->     matchName     		����AnalogMyMatch���ȡmatchName��
					->     analogMatchId 		����AnalogMyMatch���ȡanalogMatchId��
	VGroupid        ->     groupBmId        
	StockCode       ->     stockCode     
	stockname       ->     stockName     
	stockTypeName   ->     stockTypeName
	marketCode      ->     marketCode   
	marketName      ->     marketName    
	CurrentVolume   ->     totalVolume  
	UseVolume       ->     useVolume    
					->     price        �����㣩
	cost            ->     cost         
	ProfitorLoss    ->     profitorLoss 
    BuyMoney        ->     buyMoney     
    headImageUrl    ->     headImageUrl 

###����###
AnalogMyMatch
####�ֶ�˵��####
|----|----|
|����|����|˵��|ȱʡ|
|userObjectId |�ַ���|BOSSϵͳ�û�objectid| ��|
|userName |�ַ���|BOSSϵͳ�û�����| ��|
|analogUserId |����|ģ�⳴��ϵͳ�û�id| ��|
|matchObjectId |�ַ���|BOSSϵͳ������ojectid| ��|
|matchName |�ַ���|BOSSϵͳ��������| ��|
|analogMatchId |����|ģ�⳴��ϵͳ����id| ��|
|beginTime |Date|��ʼ����| ��|
|endTime |Date|��������| ��|
|groupBmId |����|ģ�⳴��ϵͳ�ʽ�id| ��|
|pm |����|����| ��|
|pmDay |����|������| ��|
|pmWeek |����|������| ��|
|syl |�ַ���|������| ��|
|sylDay |�ַ���|��������| ��|
|sylWeek |�ַ���|��������| ��|
|shouYiLv |����|������| ��|
|shouYiLvDay |����|��������| ��|
|shouYiLvWeek |����|��������| ��|
|originalCapital |����|ԭʼ�ʽ�| ��|
|residualCapital |����|ʣ���ʽ�| ��|
|frozenCapital |����|�����ʽ�| ��|
|tradeTotal |����|������| ��|
|tradeCountYL |����|ӯ��������| ��|
|myPopularity |����|������������ע��| ��|
|totalProfitorLoss |����|��ӯ��| ��|
|isDefault |�ַ���|ģ�⳴�ɱ�־ 1ģ�⳴�� ���� ���ɴ���| ��|
|headImageUrl |�ַ���|�û�ͷ��| ��|

###webservice�ӿ��ֶ�->MC�ֶ�###
	webservice�ӿ��ֶ�		MC�ֶ�
						->     userObjectId   		����_User���ȡuserId��
	ZhName	    		->     userName      
						->     analogUserId  	 	����AnalogMyMatch���ȡanalogUserId��
						->     matchObjectId 		����AnalogMyMatch���ȡmatchObjectId��
						->     matchName     		����AnalogMyMatch���ȡmatchName��
						->     analogMatchId 		����AnalogMyMatch���ȡanalogMatchId��
						->	   beginTime        	����AnalogMyMatch���ȡanalogMatchId��
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
	headImageUrl        ->     headImageUrl     	����_User���ȡheadImageUrl��

	
2��Order 
####����####
�ɽ�����ͬ��
###ͬ���߼�����###

###webservice�ӿ�###
Query_uimsStockTransDataSetList
###����###
AnalogOrder
####�ֶ�˵��####
|----|----|
|����|����|˵��|ȱʡ|
|userObjectId |�ַ���|BOSSϵͳ�û�objectid| ��|
|userName |�ַ���|BOSSϵͳ�û�����| ��|
|analogUserId |����|ģ�⳴��ϵͳ�û�id| ��|
|matchObjectId |�ַ���|BOSSϵͳ������ojectid| ��|
|matchName |�ַ���|BOSSϵͳ��������| ��|
|analogMatchId |����|ģ�⳴��ϵͳ����id| ��|
|groupBmId |����|ģ�⳴��ϵͳ�ʽ�id| ��|
|mainKeyId |����|ģ�⳴��ϵͳί��id| ��|
|stockCode |�ַ���|��Ʊ���룬����600036| ��|
|stockName |�ַ���|��Ʊ���ƣ�������������| ��|
|marketCode |�ַ���|�г����룬����SH| ��|
|price |����|�ɽ��۸�| ��|
|volume |����|�ɽ�����| ��|
|cjje |����|�ɽ��۸�| ��|
|transType |�ַ���|��������| ��|
|dealTime |Date|�ɽ�ʱ��| ��|
|profitorLoss |����|����ֵ| ��|
|syl |�ַ���|������| ��|
|headImageUrl |�ַ���|�û�ͷ��| ��|

###webservice�ӿ��ֶ�->MC�ֶ�###
	webservice�ӿ��ֶ�		MC�ֶ�
					->     userObjectId   		����AnalogMyMatch���ȡuserObjectId��
	ZhName	        ->     userName      
					->     analogUserId  	 	����AnalogMyMatch���ȡanalogUserId��
					->     matchObjectId 		����AnalogMyMatch���ȡmatchObjectId��
					->     matchName     		����AnalogMyMatch���ȡmatchName��
					->     analogMatchId 		����AnalogMyMatch���ȡanalogMatchId��
	VGroupid        ->     groupBmId     
	TransRecordId   ->     mainKeyId     
	StockCode       ->     stockCode     
	stockname       ->     stockName     
	marketcode      ->     marketCode    
	Price           ->     price         
	Volume          ->     volume        
					->     cjje   �����㣩       
	transType       ->     transType	 (ת��1����   0����)    
	cjdatetime      ->     dealTime      
	ProfitorLoss    ->     profitorLoss  
	syl             ->     syl           
					->     headImageUrl  ����AnalogMyMatch���ȡheadImageUrl��
	

3��Range 
####����####
��������ͬ�� 
###ͬ���߼�����###

###webservice�ӿ�###
Query_uimsSYPM
###����###
AnalogRange
####�ֶ�˵��####
|----|----|
|����|����|˵��|ȱʡ|
|userObjectId |�ַ���|BOSSϵͳ�û�objectid| ��|
|userName |�ַ���|BOSSϵͳ�û�����| ��|
|headImageUrl |�ַ���|ͷ��| ��|
|groupBmId |����|ģ�⳴��ϵͳ�ʽ�id| ��|
|pm |����|����| ��|
|syl |�ַ���|������| ��|
|type |����|�������� 1������ 2������ 3������ | ��|
|totalCapital |����|���ʲ� | ��|
|cgl |����|�ֹ��� | ��|
|groupBm |�ַ���|�������� | ��|
|djs |����|�����| ��|
|shouYiLv |����|������ | ��|
|originalCapital |����|ԭʼ�ʽ�| ��|
|cw |����|��λ | ��|

###webservice�ӿ��ֶ�->MC�ֶ�###
	webservice�ӿ��ֶ�			MC�ֶ�
						->	  	userObjectId 	 (��AnalogMyMatch���ȡuserObjectId)
	groupbm	            ->		userName        
						->		headImageUrl      (��AnalogMyMatch���ȡheadImageUrl)
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
	
4��Speech	
####����####
�񽱸���ͬ�� 
###ͬ���߼�����###
ÿ�����һ���16��30���� �������µĻ񽱸������� 

###webservice�ӿ�###
Query_uimsHJGY
###����###
uimsHJGY
####�ֶ�˵��####

###webservice�ӿ��ֶ�->MC�ֶ�###
	webservice�ӿ��ֶ�			MC�ֶ�
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
	
5��HistRank
####����####
��ʷ����ͬ�� 
###ͬ���߼�����###
ÿ�����һ���16��30�������µ���ʷ��������

###webservice�ӿ�###
Query_uimsLSPM
###����###
uimsLSPM
####�ֶ�˵��####

###webservice�ӿ��ֶ�->MC�ֶ�###
	webservice�ӿ��ֶ�			MC�ֶ�
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
	
	
6��Comment
####����####
ר�ҵ���ͬ�� 
###ͬ���߼�����###
ÿ��16��30����ר�ҵ�������

###webservice�ӿ�###
Query_uimsZJDP
###����###
uimsZJDP
####�ֶ�˵��####

###webservice�ӿ��ֶ�->MC�ֶ�###
	webservice�ӿ��ֶ�			MC�ֶ�
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
	
7��Season
####����####
����ͬ�� 
###ͬ���߼�����###
ÿ�����һ���16��30����������������

###webservice�ӿ�###
Query_uimsSEASONSET
###����###
uimsSeasonSet
####�ֶ�˵��####

###webservice�ӿ��ֶ�->MC�ֶ�###
	webservice�ӿ��ֶ�			MC�ֶ�
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
	
	
8��NiuguList
ţ�ɰ�ͬ�� 
###ͬ���߼�����###
ÿ��16��30��������ţ�ɰ�����

###webservice�ӿ�###
Query_uimsNGB
###����###
uimsNGB
####�ֶ�˵��####

###webservice�ӿ��ֶ�->MC�ֶ�###
	webservice�ӿ��ֶ�			MC�ֶ�
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
	
9��RecordVideo
CCTVͬ��
###ͬ���߼�����###


###webservice�ӿ�###
P_Z_video
###����###
A_DxtRecordVideo
####�ֶ�˵��####

###webservice�ӿ��ֶ�->MC�ֶ�###
	webservice�ӿ��ֶ�			MC�ֶ�
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