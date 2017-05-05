create external table if not exists ods_mysql.ods_beeper_trans_task__trans_task_vas_temperature_control (
    `id` bigint comment "线路任务温控配置 ID" ,
    `trans_task_id` bigint comment "线路任务ID" ,
    `is_enable` int comment "当前配置是否生效" ,
    `have_temp_ctrl` int comment "是否开启温控服务: 0关闭，1开启" ,
    `enable_notify` int comment "是否开启短信通知司机温控报警: 0关闭，1开启" ,
    `begin_at` timestamp comment "温控服务开启时间" ,
    `price` bigint comment "每趟出车的温控价格（单位：分）" ,
    `price_mode` int comment "收费模式 100: 费率 , 200: 固定费用" ,
    `price_rate` double comment "每趟出车的温控收费标准, 按基础运力价格的比率收费，如：0.05" ,
    `alert_seconds` bigint comment "报警持续时间（单位：秒）" ,
    `warning_range_type` int comment "预警温度区间：保鲜、冷藏、冷冻" ,
    `normal_min` int comment "正常温度最小值" ,
    `normal_max` int comment "正常温度最大值" ,
    `warning_left_min` int comment "预警温度低范围最小值" ,
    `warning_left_max` int comment "预警温度低范围最大值" ,
    `warning_right_min` int comment "预警温度高范围最小值" ,
    `warning_right_max` int comment "预警温度高范围最大值" ,
    `alert_min` int comment "报警温度最小值" ,
    `alert_max` int comment "报警温度最大值" ,
    `battery_alert_rate` double comment "报警电量百分比" ,
    `notify_mobiles` string comment "报警通知的手机号码,例如：18610811525,13267838982" ,
    `operator_id` bigint comment "操作人ID" ,
    `source` int comment "操作来源" ,
    `created_at` timestamp comment "创建时间" ,
    `updated_at` timestamp comment "更新时间" ) partitioned by(p_day string)
 stored as orc