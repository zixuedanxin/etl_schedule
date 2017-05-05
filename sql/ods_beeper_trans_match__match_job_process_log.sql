create external table if not exists ods_mysql.ods_beeper_trans_match__match_job_process_log (
    `id` bigint comment "找司机进程日志ID" ,
    `job_id` bigint comment "找司机JOB ID" ,
    `process_id` bigint comment "找司机进程ID" ,
    `source_id` bigint comment "需求方id" ,
    `source_type` int comment "需求方类型 100 线路任务" ,
    `match_type` int comment "找司机方式 100 竞价方式 200 派单方式" ,
    `job_status` int comment "招司机JOB状态" ,
    `process_status` int comment "招司机进程状态" ,
    `attempts` bigint comment "该进程是第几次重试" ,
    `max_attempts` bigint comment "最大重试次数" ,
    `driver_id` bigint comment "找到的司机ID" ,
    `driver_price` bigint comment "司机金额 单位:分" ,
    `customer_price` bigint comment "客户金额 单位:分" ,
    `operator_id` bigint comment "操作人ID" ,
    `operator_name` string comment "操作人名称" ,
    `operation_time` timestamp comment "操作时间" ,
    `operation_from` bigint comment "操作来源,即模块from" ,
    `action` string comment "操作" ,
    `remark` string comment "备注说明" ) partitioned by(p_day string)
 stored as orc