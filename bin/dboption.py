#!/usr/bin/python
# -*- coding:utf-8 -*-

from logutil import Logger
from dateutil import DateUtil
from dbutil import DBUtil
import MySQLdb
import traceback

JOB_RUNNING = "Running"
JOB_DONE = "Done"
JOB_FAILED = "Failed"
JOB_PENDING = "Pending"


class DBOption(object):
    def __init__(self):
        self.dbUtil = DBUtil()
        self.logger = Logger("db").getlog()

    # 获取时间触发job
    def get_time_trigger_job(self, hour, minute):
        sql = "select t1.job_name as job_name,start_day,start_hour, \
                start_minute,trigger_type \
                from t_etl_job t1 \
                left join t_etl_job_trigger t2 \
                on  t1.job_name = t2.job_name \
                where t1.enable = 0 and t1.job_status = %s \
                and t2.job_name is not null and t2.start_hour = %s and t2.start_minute = %s"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, (JOB_DONE, hour, minute))
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return None

    # 更新时间出发Job 的状态为 Pending
    def update_trigger_job_pending(self, current, job_name):
        sql = "update t_etl_job set job_status = %s , pending_time = %s \
                where job_name = %s and job_status = %s and enable = 0"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, (JOB_PENDING, DateUtil.format_year_second(current), job_name, JOB_DONE))
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    # 获取当前运行的Job
    def get_running_jobs(self):
        sql = "select job_name from t_etl_job where job_status = %s"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, (JOB_RUNNING,))
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return None

            # 查询 Job 信息

    def get_job_info(self, job_name):
        try:
            connection = self.dbUtil.get_connection()
            sql = "select job_name,job_status,job_trigger,job_script,main_man,retry_count," \
                  "pending_time from t_etl_job where job_name = %s"
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, (job_name,))
            row = cursor.fetchone()
            connection.close()
            return row
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return None

    # 查询 job 的 依赖job
    def get_dependency_job(self, job_name):
        sql = "select dependency_job from t_etl_job_dependency where job_name = %s and enable = 0"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, (job_name,))
            rows = cursor.fetchall()
            cursor.close()
            connection.commit()
            connection.close()
            return rows
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return None

    # 获取job 依赖运行状态
    def get_dependency_job_status(self, job_name):
        sql = "select job_name,job_status,last_run_date from t_etl_job t1 \
                right join ( \
               select dependency_job from t_etl_job_dependency where job_name = %s and enable = 0) t2 \
                on t1.job_name = t2.dependency_job"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, (job_name,))
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return None

    def get_pending_jobs(self):
        sql = "select job_name,job_script from t_etl_job where job_status = %s"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, (JOB_PENDING,))
            rows = cursor.fetchall()
            cursor.close()
            connection.commit()
            connection.close()
            return rows
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return None

    # 获取需要运行的任务数 状态为 Pending
    def get_pending_jobs_by_require_time(self, require_time, job_limit):  # 方便增加优先级排序
        sql = "select job_name,job_script from t_etl_job where job_status = %s order by pending_time asc limit %s , %s"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            offset = require_time * job_limit
            cursor.execute(sql, (JOB_PENDING, offset, job_limit))
            rows = cursor.fetchall()
            cursor.close()
            connection.commit()
            connection.close()
            return rows
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return None

    # 获取 t_etl_job_queue 中等待运行的Job , 或者是今天已经运行完成的job
    def get_queue_job(self, job_name):
        time = DateUtil.get_now()
        day = DateUtil.format_year_day(time)
        sql = "select job_name,job_status,run_number from t_etl_job_queue where job_name = %s and (job_status = %s " \
              "or (job_status=%s and run_date = %s))"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, (job_name, JOB_PENDING, JOB_DONE, day))
            row = cursor.fetchone()
            cursor.close()
            connection.close()
            return row
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return None

    # 保存 t_etl_job_queue 等待运行
    def save_job_queue(self, job_name, pending_time):
        sql = "insert into t_etl_job_queue(job_name,create_time,run_number," \
              "job_status,pending_time) values (%s,%s,%s,%s,%s)"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, (job_name, DateUtil.get_now(), 1, JOB_PENDING, pending_time))
            cursor.close()
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    def get_queue_job_pending(self):
        sql = "select job_name,run_number from t_etl_job_queue where job_status = %s order by create_time asc limit 1"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, (JOB_PENDING,))
            row = cursor.fetchone()
            cursor.close()
            connection.close()
            return row
        except Exception, e:
            self.logger.error(traceback.format_exc())

    def update_job_running(self, job_name):
        time_string = DateUtil.format_year_second(DateUtil.get_timestamp())
        run_sql = "update t_etl_job set job_status = %s , last_start_time=%s where job_name=%s and (job_status = %s or job_status = %s)"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(run_sql, (JOB_RUNNING, time_string, job_name, JOB_PENDING, JOB_RUNNING))
            cursor.close()
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    def update_job_done(self, job_name):
        time = DateUtil.get_now()
        time_string = DateUtil.format_year_second(time)
        time_day = DateUtil.format_year_day(time)
        done_sql = "update t_etl_job set job_status = %s , last_end_time=%s , last_run_date=%s  \
                    where job_name=%s and job_status = %s"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(done_sql, (JOB_DONE, time_string, time_day, job_name, JOB_RUNNING))
            cursor.close()
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    # 修改 job 的运行状态为 Failed
    def update_job_failed(self, job_name):
        time = DateUtil.get_now()
        time_string = DateUtil.format_year_second(time)
        day = DateUtil.format_year_day(time)
        failed_sql = "update t_etl_job set job_status = %s , last_end_time=%s , last_run_date = %s where job_name=%s"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(failed_sql, (JOB_FAILED, time_string, day, job_name))
            cursor.close()
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    # 获取需要触发的job
    def get_stream_job(self, job_name):
        sql = "select job_name,stream_job,enable from t_etl_job_stream where job_name = %s and enable = 0"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, (job_name,))
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except Exception, e:
            self.logger.error(traceback.format_exc())

    # 更新job状态为 Pending
    def update_job_pending(self, job_name):
        time = DateUtil.get_now()
        sql = "update t_etl_job set job_status = %s , pending_time = %s \
               where job_name = %s and job_status = %s and enable = 0"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, (JOB_PENDING, DateUtil.format_year_second(time), job_name, JOB_DONE))
            connection.commit()
            cursor.close()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    def update_job_pending_from_running(self, job_name):
        time = DateUtil.get_now()
        sql = "update t_etl_job set job_status = %s , pending_time = %s \
               where job_name = %s and job_status = %s and enable = 0"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, (JOB_PENDING, DateUtil.format_year_second(time), job_name, JOB_RUNNING))
            connection.commit()
            cursor.close()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    def update_job_queue_done(self, job_name):
        time = DateUtil.get_now()
        day = DateUtil.format_year_day(time)
        sql = "update t_etl_job_queue set job_status = %s , run_time = %s , run_date = %s \
               where job_name = %s and job_status = %s"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, (JOB_DONE, time, day, job_name, JOB_PENDING))
            connection.commit()
            cursor.close()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    ''' 更新是按照天的,如果一天运行多次就有问题了, 运行多次应该更新最新的'''

    def update_job_queue_failed(self, job_name):
        time = DateUtil.get_now()
        day = DateUtil.format_year_day(time)
        sql = "update t_etl_job_queue set job_status = %s , run_time = %s , run_date = %s \
               where job_name = %s and create_time > %s"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, (JOB_FAILED, time, day, job_name, day))
            connection.commit()
            cursor.close()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    def get_main_man(self):
        sql = "select user_phone from t_etl_job_monitor where enable = 0"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return None

    def get_main_man_user(self, user_name):
        sql = "select user_phone from t_etl_job_monitor where enable = 0 and user_name = %s"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, (user_name,))
            row = cursor.fetchone()
            cursor.close()
            connection.close()
            return row
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return None

    def get_main_man_by_role(self, role_name):
        sql = "select user_phone from t_etl_job_monitor where enable=0 and role = %s"
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, (role_name,))
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return None

    def save_time_trigger_job(self, job_name, trigger_type, day, hour, minute, interval, man, script, dep_jobs):
        try:
            etl_job_sql = "insert into t_etl_job(job_name,job_status,job_script,job_trigger,main_man)  \
                       values(%s,%s,%s,%s,%s)"
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(etl_job_sql, (job_name, JOB_DONE, script, trigger_type, man))
            time_job = "insert into t_etl_job_trigger(job_name,start_day,start_hour,start_minute,trigger_type) \
                       values(%s,%s,%s,%s,%s)"
            cursor.execute(time_job, (job_name, day, hour, minute, interval))
            dep_job_sql = "insert into t_etl_job_dependency(job_name,dependency_job) values(%s,%s)"
            for dep_job in dep_jobs:
                # 判断是否存在,存在则删除
                self.remove_dependency(job_name, dep_job)
                cursor.execute(dep_job_sql, (job_name, dep_job.upper()))
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    def save_depdency_trigger_job(self, job_name, trigger_type, dep_jobs, stream, man, script):
        try:
            etl_job_sql = "insert into t_etl_job(job_name,job_status,job_script,job_trigger,main_man)  \
                       values(%s,%s,%s,%s,%s)"
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(etl_job_sql, (job_name, JOB_DONE, script, trigger_type, man))
            dep_job_sql = "insert into t_etl_job_dependency(job_name,dependency_job) values(%s,%s)"
            for dep_job in dep_jobs:
                # 判断是否存在,存在则删除
                self.remove_dependency(job_name, dep_job)
                cursor.execute(dep_job_sql, (job_name, dep_job.upper()))
            # 删除触发
            self.remove_stream(stream, job_name)
            stream_job_sql = "insert into t_etl_job_stream(job_name,stream_job) values(%s,%s)"
            cursor.execute(stream_job_sql, (stream, job_name))
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    def remove_stream(self, stream_job, job_name):
        try:
            remove_sql = "delete from t_etl_job_stream where job_name = %s and stream_job = %s"
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(remove_sql, (stream_job, job_name))
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    def remove_dependency(self, job_name, dep_job):
        try:
            remove_sql = "delete from t_etl_job_dependency where job_name = %s and dependency_job = %s"
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(remove_sql, (job_name, dep_job))
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    # no use
    def remove_etl_job(self, job_name):
        try:
            remove_sql = "delete from t_etl_job where job_name = %s"
            print remove_sql % "'" + job_name + "'"  # 需要输出到控制台
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(remove_sql, (job_name,))
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    def remove_etl_dependency_job(self, job_name):
        try:
            remove_sql = "delete from t_etl_job_dependency where job_name = %s"
            print remove_sql % "'" + job_name + "'"  # 需要输出到控制台
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(remove_sql, (job_name,))
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    def remove_etl_stream_job(self, job_name):
        try:
            remove_sql = "delete from t_etl_job_stream where stream_job = %s"
            print remove_sql % "'" + job_name + "'"  # 需要输出到控制台
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(remove_sql, (job_name,))
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    def remove_etl_job_trigger(self, job_name):
        try:
            remove_sql = "delete from t_etl_job_trigger where job_name = %s"
            print remove_sql % "'" + job_name + "'"  # 需要输出到控制台
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(remove_sql, (job_name,))
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    def get_before_job(self, job_name):
        try:
            stream_job_sql = "select job_name,enable from t_etl_job_stream where stream_job = %s"
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(stream_job_sql, (job_name,))
            row = cursor.fetchone()
            return row
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return None

    def get_etl_job_trigger(self, job_name):
        try:
            trigger_job_sql = "select job_name,start_day,start_hour,start_minute, \
                              trigger_type from t_etl_job_trigger where job_name = %s"
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(trigger_job_sql, (job_name,))
            row = cursor.fetchone()
            return row
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return None

    def update_job_run_number(self, job_name, retry_count):
        try:
            current_date = DateUtil.get_now_fmt(None)
            update_sql = "update t_etl_job_queue set run_number = %s , job_status = %s " \
                         "where job_name = %s and run_date = %s and job_status = %s"
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(update_sql, (retry_count, JOB_PENDING, job_name, current_date, JOB_DONE))
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    def remove_queue_job(self, job_name):
        try:
            current_date = DateUtil.get_now_fmt(None)
            print current_date
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            remove_sql = "delete from t_etl_job_queue where job_name = %s and run_date = %s"
            cursor.execute(remove_sql, (job_name, current_date))
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    def update_job_queue_complete_time(self, job_name):
        try:
            time = DateUtil.get_now()
            current_date = DateUtil.get_now_fmt(None)
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            remove_sql = "update t_etl_job_queue set complete_time = %s where job_name = %s and run_date = %s"
            cursor.execute(remove_sql, (time, job_name, current_date))
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    def execute_sql(self, sql, param):
        try:
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, param)
            connection.commit()
            connection.close()
            return cursor.rowcount
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return 0

    # 获取job 被哪些 job 依赖
    def get_depended_job(self, job_name):
        try:
            stream_job_sql = "select job_name from t_etl_job_dependency where dependency_job = %s"
            connection = self.dbUtil.get_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(stream_job_sql, (job_name,))
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except Exception, e:
            self.logger.error(traceback.format_exc())
            raise Exception("查询被依赖 job 异常")
