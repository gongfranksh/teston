# -*- coding: utf-8 -*-
from apps.Entity.jsEntity import JsEntity


class Member(JsEntity):

    def __init__(self):
        JsEntity.__init_no_branchcode__(self, "mem_personal")
        self.base_query_sql = """
          SELECT cardid AS  bncid,telephone AS mobile,' ' AS nickname FROM mem_personal 
                """

    def seek_memeber_by_mobile(self, mobile):
        rst_array=[]
        sql_cond = """
                where  telephone='{0}'
                """
        sql = self.base_query_sql + sql_cond
        sql = sql.format(mobile)
        rst = self.get_remote_result_by_sql(sql)
        # rst_array.append(rst)
        return rst

    def seek_memeber_by_bncid(self, bncid):
        rst_array = []
        sql_cond = """
                where cardid='{0}'
                """
        sql = self.base_query_sql + sql_cond
        sql = sql.format(bncid)
        rst = self.get_remote_result_by_sql(sql)
        rst_array.append(rst)
        return rst

