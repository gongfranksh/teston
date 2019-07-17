# -*- coding: utf-8 -*-
from apps.Entity.jsEntity import JsEntity


class Branch(JsEntity):

    def __init__(self,branchcode):
        JsEntity.__init__(self, "BRANCH",branchcode)



    def get_branch_all(self):
        sql= " SELECT * FROM branch WHERE BraType='0' AND Status='0' ORDER BY BraName,braid "
        rst = self.get_remote_result_by_sql(sql)
        return rst

