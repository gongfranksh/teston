# -*- coding: utf-8 -*-
from Entity.jsEntity import JsEntity


class PayMent(JsEntity):
    def __init__(self, branchcode):
        JsEntity.__init__(self, "PayMent", branchcode)

    def get_branch_payment_all(self):
        sql_cond = """
                SELECT * FROM payment WHERE isActive=1  ORDER BY sortbyid
          """
        sql = sql_cond
        rst = self.get_remote_result_by_sql(sql)
        return rst
