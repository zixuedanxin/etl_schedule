create external table if not exists ods.ods_pack_report (
    `id` bigint comment "封装项目日报ID" ,
    `charge_id` bigint comment "客户封装项目计费信息ID" ,
    `customer_id` bigint comment "客户ID" ,
    `report_date` date comment "日报日期" ,
    `reporter_id` bigint comment "填报人ID" ,
    `adc_id` bigint comment "管理区ID" ,
    `sales_id` bigint comment "客户顾问ID" ,
    `bu_lead_id` bigint comment "bu lead id" ,
    `status` int comment "状态：100 为提交 200 已提交" ,
    `committed_at` timestamp comment "提交时间" ,
    `created_at` timestamp comment "填写时间" ,
    `updated_at` timestamp comment "最后更新时间" ,
    `fcc_commit_at` timestamp comment "主管提交时间" ,
    `customer_flag` bigint comment "封装标记" ,
    `have_surety` int comment "是否有保底 0 表示没保底 1 表示有保底" ,
    `have_arrange_auth` int comment "是否有排线权 0 表示没排线权 1 表示有排线权" ,
    `charge_unit` int comment "计费单位：件、票、重量、货值、体积、捆绑按趟" ,
    `surety_unit` int comment "保底单位 数量 和 金额" ,
    `gross_profit` bigint comment "毛利" ,
    `gross_profit_rate` double comment "毛利率" ,
    `customer_tax_rate` double comment "税率" ,
    `customer_sop_rate` double comment "SOP费率" ,
    `income_total` bigint comment "所有收入合计,包括拒收退货收入、专程退货收入、赔付收入、司机事故收入、杂项收入、日超重收入、其他收入" ,
    `income_total_tax` bigint comment "收入税金 = income_total * customer_tax_rate" ,
    `income_business_total` bigint comment "营运收入，为日报营收明细中各个二级计费的收入合计" ,
    `income_other_total` bigint comment "其他各项收入 包括 拒收退货收入、专程退货收入、赔付收入(客户-事故中心)，司机事故收入等" ,
    `cost_total` bigint comment "成本合计" ,
    `cost_surcharge_total` bigint comment "杂费合计" ,
    `cost_business_total` bigint comment "其他业务成本合计，包括：基础运力费成本、提成（标准提点费，线下）、司机福利（线上）等" ,
    `description` string comment "日报说明" )
 stored as orc