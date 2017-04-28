create external table if not exists ods.ods_accident (
    `id`  bigint comment "事故ID" ,
    `happened_at`  bigint comment "发生时间" ,
    `customer_id`  bigint comment "客户ID" ,
    `customer_name`  string comment "客户名称" ,
    `customer_payment_price`  bigint comment "客户赔付款，单位：分" ,
    `driver_id`  bigint comment "司机ID" ,
    `driver_name`  string comment "司机姓名" ,
    `driver_punish_price`  bigint comment "司机罚款，单位：分" ,
    `service_rule_type`  int comment "违规岗控条款类型" ,
    `sop_rule_group`  string comment "违规SOP条款流程" ,
    `payment_type`  int comment "客户赔付类型" ,
    `payment_scene`  string comment "客户赔付场景" ,
    `status`  int comment "处理状态" ,
    `type`  int comment "事故类型" ,
    `yn_feedback_user`  string comment "公司反馈人" ,
    `yn_feedback_user_contact`  string comment "公司反馈人联系方式" ,
    `customer_feedback_user`  string comment "客户反馈人" ,
    `customer_feedback_user_contact`  string comment "客户反馈人联系方式" ,
    `feedback_at`  bigint comment "反馈时间" ,
    `operator_id`  bigint comment "处理人ID" ,
    `operator_nick`  string comment "处理人名称" ,
    `operated_at`  bigint comment "处理时间" ,
    `updated_at`  bigint comment "更新时间" ,
    `created_at`  bigint comment "创建时间" ,
    `is_driver_blacklist`  int comment "是否将司机加入黑名单" ,
    `project_type`  int comment "项目类型，1自助，2封装" ,
    `creator_nick`  string comment "创建人" ,
    `priority`  int comment "紧急程度" ,
    `source`  bigint comment "反馈来源" ,
    `source_desc`  string comment "反馈来源描述" ,
    `feedback_way`  bigint comment "反馈方式" ,
    `feedback_way_desc`  string comment "反馈方式描述" ,
    `feedback_user`  string comment "反馈人" ,
    `feedback_user_contact`  string comment "反馈人电话" ,
    `responsible_type`  int comment "责任人类型，100司机，200运作主管" ,
    `level`  int comment "事故等级，1一级，2二级" ,
    `label`  bigint comment "事故标签" ,
    `process_result`  int comment "处理结果，100确定事故，200不是事故" ,
    `customer_real_payment_price`  bigint comment "实际客户赔付款,单位：分" ,
    `driver_real_punish_price`  bigint comment "实际罚司机金额,单位：分" ,
    `finished_at`  bigint comment "处理完成时间" )
 stored as orc