# -*- coding: utf-8 -*-

import json
import pymssql
import sys


from apps.Entity.Utils import MsSqlResultDataEncoder

# reload(sys)
# sys.setdefaultencoding("utf-8")
#




class JsEntity(object):

    def __CONNECT_INFO(self):
        self.js_host = "192.168.72.5"
        self.js_user = "syzy"
        self.js_pwd = "7fad69fa0c"
        self.js_db = "headquarters"

    def __init__(self, table,branchcode):
        self.remote_table = table
        self.local_table = table
        self.branch_code =branchcode
        self.__CONNECT_INFO()

    def __init_no_branchcode__(self, table):
        self.remote_table = table
        self.local_table = table
        self.__CONNECT_INFO()

    def init_table_diff(self, remotetable,branchcode):
        self.remote_table = remotetable
        self.branch_code =branchcode
        self.__CONNECT_INFO()

    def init_by_branch(self, table,branchcode):
        self.remote_table = table
        self.local_table = table
        self.branch_code =branchcode
        self.__CONNECT_INFO()

    def __IsNoneRow(self,row):
            if row[0] is None:
                return 0
            else:
                return row[0]

    def IsNone(self,row):
            if row is None:
                return 0
            else:
                return row

    def __GetConnect_mssql(self):
        if not self.js_db:
            raise (NameError, "没有设置数据库信息")
        self.conn_js = pymssql.connect(host=self.js_host, user=self.js_user, password=self.js_pwd, database=self.js_db, charset="utf8")

        #add para as_dict=true return dict recordset

        cur = self.conn_js.cursor(as_dict=True)
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def __MsSql_ExecQuery(self, sql):
        cur = self.__GetConnect_mssql()
        cur.execute(sql)
        resList = cur.fetchall()
        return resList


    def get_remote_table_result_all(self):
        sql = """
        SELECT * FROM {0};
        """
        sql=sql.format(self.remote_table)
        res = self.__MsSql_ExecQuery(sql)
        # print res[0]
        json_res= json.dumps(res,cls=MsSqlResultDataEncoder)
        return json_res

    def get_remote_table_result_by_timestamp(self,timestamp):
        sql = """
        SELECT *,CONVERT (int,timestamp) as stamps FROM {0} where CONVERT (int,timestamp) > {1} order by timestamp ;
        """
        sql=sql.format(self.remote_table,timestamp)
        res = self.__MsSql_ExecQuery(sql)
        return res

    def get_remote_table_result_by_branch_timestamp(self,timestamp):
        sql = """
        SELECT *,CONVERT (int,timestamp) as stamps FROM {0} 
        where CONVERT (int,timestamp) > {1} and braid='{2}' 
        order by timestamp ;
        """
        sql=sql.format(self.remote_table,timestamp,self.branch_code)
        print (sql)
        res = self.__MsSql_ExecQuery(sql)
        return res

    def get_remote_result_by_sql(self,sql):
        res = self.__MsSql_ExecQuery(sql)
        json_res= json.dumps(res,cls=MsSqlResultDataEncoder)
        return json_res

    def get_remote_list_by_sql(self,sql):
        res = self.__MsSql_ExecQuery(sql)
        return res

    def execSql(self,sql):
        try:
            if not self.js_db:
                raise (NameError, "没有设置数据库信息")
            conn = pymssql.connect(host=self.js_host, user=self.js_user, password=self.js_pwd,
                                           database=self.js_db, charset="utf8")
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print(e.message)

