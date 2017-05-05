create external table if not exists ods_mysql.ods_beeper_trans_match__match_job_process_params_task (
    `id` bigint comment "招司机 JOB 参数 ID" ,
    `process_id` bigint comment "找司机进程ID" ,
    `params_created_at` timestamp comment "该参数创建时间" ,
    `params_updated_at` timestamp comment "该参数最后更新时间" ,
    `receiving_bid_end_time` timestamp comment "司机报价截止时间" ,
    `evaluating_bid_end_time` timestamp comment "选择报价截止时间" ,
    `task_id` bigint comment "任务ID" ,
    `task_created_at` timestamp comment "任务创建时间" ,
    `task_updated_at` timestamp comment "最后更新时间" ,
    `task_deleted_at` timestamp comment "删除时间" ,
    `requirement_created_at` timestamp comment "创建时间" ,
    `requirement_updated_at` timestamp comment "最后更新时间" ,
    `version` int comment "任务版本号" ,
    `customer_id` bigint comment "客户ID" ,
    `warehouse_id` bigint comment "仓库ID" ,
    `line_name` string comment "线路名称" ,
    `type` int comment "任务类型" ,
    `status` int comment "任务状态" ,
    `open_task_time` timestamp comment "开启任务的时间（开标时间）" ,
    `driver_id` bigint comment "司机ID" ,
    `driver_price` bigint comment "司机价格, 单位:人民币分" ,
    `schedule` string comment "符合RFC2445标准的重复事件字符串表达式" ,
    `work_begin_time` string comment "上班时间（到仓时间）" ,
    `time_cost` bigint comment "预计工作耗时(秒)" ,
    `onboard_date` date comment "上岗日期" ,
    `end_date` date comment "任务结束日期" ,
    `expected_end_date` date comment "预计任务结束日期" ,
    `is_distribution_point_fixed` int comment "配送点是否固定" ,
    `distribution_point_min` int comment "预计配送点最小个数" ,
    `distribution_point_max` int comment "预计配送点最大个数" ,
    `distribution_area` string comment "配送区域描述(配送点固定时为备注)" ,
    `distance_min` double comment "配送里程最小值" ,
    `distance_max` double comment "配送里程最大值" ,
    `is_back` int comment "是否要求返仓" ,
    `is_ignore_restrict` int comment "限行是否要求配送" ,
    `is_need_receipt` int comment "是否需要回单" ,
    `receipt_type` int comment "回单方式" ,
    `receipt_info` string comment "回单信息(json)" ,
    `expected_price_min` bigint comment "客户预期单趟价格最小值（单位：分）" ,
    `expected_price_max` bigint comment "客户预期单趟价格最大值（单位：分）" ,
    `expected_price_describe` string comment "影响司机报价的情况说明" ,
    `reason` string comment "招标原因（单选+其他）" ,
    `driver_welfare` string comment "司机福利、补贴及奖励" ,
    `comment` string comment "更新线路任务为废弃, 等终点状态的说明" ,
    `cargo_type` string comment "货物类型" ,
    `cargo_volume_min` double comment "货物体积最小值，单位：立方米" ,
    `cargo_volume_max` double comment "货物体积最大值，单位：立方米" ,
    `cargo_weight_min` double comment "货物重量最小值，单位：吨" ,
    `cargo_weight_max` double comment "货物重量最大值，单位：吨" ,
    `cargo_number_min` int comment "货物件数最小值，单位：个|件|箱|捆" ,
    `cargo_number_max` int comment "货物件数最大值，单位：个|件|箱|捆" ,
    `city_id` string comment "城市ID(json array)" ,
    `car_type_id` string comment "车型ID(json array)" ,
    `deliver_experience` string comment "配送经验（多选+详情）" ,
    `handling_type` string comment "搬运程度" ,
    `is_req_xiaogong` int comment "是否需要司机自带小工" ,
    `is_with_load` int comment "是否有人帮忙装货" ,
    `is_with_unload` int comment "是否有人帮忙卸货" ,
    `is_with_board` int comment "是否带尾板" ,
    `other_handling_req` string comment "其他搬运说明" ,
    `is_need_clear_seats` int comment "是否需要拆后座" ,
    `is_need_tuiche` int comment "是否需要推车" ,
    `is_limit_phone` int comment "是否安卓系统手机、3G以上网络" ,
    `is_need_double_fire_extinguisher` int comment "是否需要配备双灭火器" ,
    `is_need_lock` int comment "是否需要配备明锁/暗锁" ,
    `is_need_practice_before_onboard` int comment "是否需要上岗前实习" ,
    `driver_req` string comment "其他上岗要求" ,
    `other_desc` string comment "补充说明" ,
    `extra` string comment "一些需要再任务大厅中展示，又不影响撮合任务的非结构化信息 json字符串" ) partitioned by(p_day string)
 stored as orc