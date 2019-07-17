# -*- coding: utf-8 -*-
from apps.Entity.jsEntity import JsEntity


class BranchEmployee(JsEntity):
    def __init__(self, branchcode):
        JsEntity.__init__(self, "Branch_Employee", branchcode)
        self.branch_code = branchcode
        self.base_query_sql = """
               SELECT braid,empid,empname,isnull(domainaccounts,'') domain,
                    isnull(discount,1) discount,
                    isnull(password,'00000000') password 
                    FROM branch_employee  
                    WHERE Status=0 
        """

    def get_branch_employee_all(self):
        sql_cond = " AND BraId='{0}' ORDER BY EmpName"
        sql = self.base_query_sql + sql_cond
        sql = sql.format(self.branch_code)
        rst = self.get_remote_result_by_sql(sql)
        return rst

    def get_branch_employee_by_domains(self,domainaccount):
        sql_cond = " AND  braid='{0}' and domain='{1}'  ORDER BY EmpName "
        sql = self.base_query_sql + sql_cond
        sql = sql.format(self.branch_code,domainaccount)
        rst = self.get_remote_result_by_sql(sql)
        return rst
