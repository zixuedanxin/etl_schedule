create external table if not exists ods.ods_trans_event (
    `id`  bigint comment "事件id，即出车计划ID" ,
    `trans_task_id`  bigint comment "线路任务ID" ,
    `trans_driver_bid_id`  bigint comment "司机竞价ID" ,
    `customer_id`  bigint comment "客户ID" ,
    `warehouse_id`  bigint comment "仓库ID" ,
    `driver_id`  bigint comment "司机ID" ,
    `sales_id`  bigint comment "客服经理ID" ,
    `sop_mgr_id`  bigint comment "现控经理id" ,
    `bid_mgr_id`  bigint comment "岗位管理经理ID" ,
    `dd_id`  bigint comment "拓展经理ID" ,
    `car_id`  bigint comment "司机的车型ID" ,
    `car_num`  string comment "司机的车牌号码" ,
    `car_team_id`  bigint comment "司机所属车队id" ,
    `status`  int comment "状态" ,
    `type`  int comment "运力类型，默认为普通运力" ,
    `inspect_status`  int comment "检察状态" ,
    `inspect_at`  timestamp comment "检察状态最后更新时间" ,
    `comment`  string comment "状态变化的描述：例如旷工原因、请假原因" ,
    `work_time`  timestamp comment "出车日期 到仓时间" ,
    `created_at`  timestamp comment "任务创建时间" ,
    `updated_at`  timestamp comment "最后更新时间" ,
    `check_in_ip`  string comment "司机签到的IP地址" ,
    `check_in_longitude`  double comment "签到位置经度" ,
    `check_in_latitude`  double comment "签到位置纬度" ,
    `check_in_time`  timestamp comment "签到时间" ,
    `is_complete`  int comment "是否完成配送" ,
    `complete_time`  timestamp comment "司机完成配送时间" ,
    `is_del`  int comment "出车计划是否被删除" ,
    `dprice_per_day`  bigint comment "司机基础价格（就是司机在手机上报价的原始价格,单天次,单位:分" ,
    `dprice_subsidy_total`  bigint comment "司机补贴总金额,该运力事件对应的所有补贴类型中的司机补贴金额的合计" ,
    `customer_tcsp`  double comment "客户运力补贴率 transport capacity subsidy percentage  例如20%，tcsp=0.2" ,
    `cprice_per_day`  bigint comment "客户基础价格（在司机价格的基础上，加入客户补贴，得出的价格 单位:分" ,
    `cprice_per_day_tax`  bigint comment "客户基础运力的税额" ,
    `cprice_subsidy_total`  bigint comment "客户补贴总金额 （该运力事件对应的所有补贴类型中的客户补贴金额的合计）" ,
    `cprice_total`  bigint comment "客户总价格" ,
    `cprice_total_with_tax`  bigint comment "客户总价格（含税）" ,
    `cargo_insurance_price`  bigint comment "货物保险金额 单位:分 (cprice_per_day * cargo_insurance_rate)" ,
    `cargo_insurance_price_tax`  bigint comment "货物保险金税额 单位:分 (cprice_per_day * cargo_insurance_rate)*invoice_tax_rate" ,
    `cargo_insurance_rate`  double comment "货物保险金额费率 例如: 0.0150 (1.5%)" ,
    `day_off_refund_price`  bigint comment "客户未设置不配送异常的退款金额" ,
    `day_off_refund_rate`  double comment "客户未设置不配送异常的退款比率" ,
    `first_onboard_price`  bigint comment "首岗奖金额 单位:分 (dprice_per_day * first_onboard_rate)" ,
    `first_onboard_rate`  double comment "首岗奖费率 例如: 0.20 (20%)" ,
    `have_sop`  int comment "是否具有SOP服务" ,
    `fcc_id`  bigint comment "现控员ID" ,
    `sop_price`  bigint comment "SOP服务总价格" ,
    `sop_rate`  double comment "SOP服务费率" ,
    `sop_price_tax`  bigint comment "SOP服务税额" ,
    `sop_royalty_rate`  double comment "现控员提成率（签到时对应的提成率）" ,
    `sop_royalty_price`  bigint comment "现控员提成金额（单位：分）提成=增值服务价格*提成率" ,
    `invoice_tax_rate`  double comment "存储当时需开发票的税率" ,
    `invoice_contents`  string comment "存储当时需开发票的内容" ,
    `task_type`  int comment "线路任务类型" ,
    `task_warehouse_id`  bigint comment "仓库ID" ,
    `task_line_name`  string comment "线路名称" ,
    `task_onboard_date`  string comment "上岗日期" ,
    `task_schedule`  string comment "配送时间" ,
    `task_work_begin_time`  string comment "到仓时间" ,
    `task_work_end_time`  string comment "预计完成时间" ,
    `task_is_back`  int comment "是否返仓 0不要求；1要求" ,
    `is_addition`  int comment "该出车记录是否是加跑" ,
    `addition_count`  bigint comment "加跑次数，表示该出车记录被加跑了几次" ,
    `addition_comment`  string comment "加跑说明，该出车记录被设置加跑的时候的说明文字" ,
    `addition_seq`  bigint comment "当该出车记录为加跑记录的时候，表示该加跑是第几次加跑，序号" ,
    `source_event_id`  bigint comment "当该出车记录为加跑记录的时候，记录其父项出车计划ID 即是对那一条出车计划进行加跑" ,
    `first_pay_money`  int comment "是否首次签到，用来做首日打款用的，一个司机只能有一个" ,
    `first_check_in`  int comment "是否首次签到，用来做产生待评价用的，一个司机在一个客户的一个仓库下只能有一个" ,
    `exception_id`  bigint comment "异常ID，当发生迟到、投诉未配送、签到位置有偏差时会产生异常" ,
    `is_supplement`  int comment "是否为补签到" ,
    `is_late`  int comment "是否迟到" ,
    `is_wrong_location`  int comment "是否签到位置与仓位置偏差大于1.5公里" ,
    `departure_ip`  string comment "司机离仓打点的IP地址" ,
    `departure_longitude`  double comment "离仓打点经度" ,
    `departure_latitude`  double comment "离仓打点纬度" ,
    `departure_time`  timestamp comment "离仓打点时间" ,
    `is_departure`  int comment "是否离仓" ,
    `new_trade_level_one`  bigint comment "客户新行业一级分类id" ,
    `adc_id`  bigint comment "客户所属管理区ID" ,
    `have_temp_ctrl`  int comment "是否有温控服务" )
 stored as orc