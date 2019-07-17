# -*- coding: utf-8 -*-
from apps.Entity.jsEntity import JsEntity


class PosMachine(JsEntity):
    def __init__(self, branchcode):
        JsEntity.__init__(self, "pos_machine", branchcode)
        self.branch_code = branchcode
        self.base_query_sql = """
              SELECT braid,posno,isnull(remarks,'')  posdesc ,isnull(Mobile_flag,'0') mobileflag
              FROM pos_machine
              WHERE isnull(Mobile_flag,'0')='1'
        """

    def get_branch_pos_machine_all(self):
        sql_cond = " AND BraId='{0}' ORDER BY posno"
        sql = self.base_query_sql + sql_cond
        sql = sql.format(self.branch_code)
        rst = self.get_remote_result_by_sql(sql)
        return rst

