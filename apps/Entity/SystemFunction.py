# -*- coding: utf-8 -*-
import json

from Entity.Utils import MsSqlResultDataEncoder
from Entity.jsEntity import JsEntity


class SystemFunction(JsEntity):

    def __init__(self,branchcode):
        JsEntity.__init__(self, "system_function",branchcode)

    def query_branch_section_menu(self):
        sql = """
       SELECT cast (id as int) AS centid, cast(id_child as int) AS sectionid ,menutext AS sectionname  
       FROM system_function_mobile  
       WHERE id_child_child=0 and isnull(Flag,'0')='1'
        ORDER BY id,id_child
        """
        rst = self.get_remote_list_by_sql(sql)
        return rst


    def query_branch_function_menu(self,centid,sectionid):
        sql = """
            SELECT CAST (id*1000+id_child*100+id_child_child AS INT) AS functionid
            ,menutext AS functionname  
            ,isnull(iconname,'') as iconname
            ,isnull(methodname,'') as methodname  
            FROM system_function_mobile 
            WHERE id_child_child NOT IN (0,-1) 
            and id={0} AND id_child={1}
            and  isnull(Flag,'0')='1' 
            """
        sql=sql.format(centid,sectionid)
        rst = self.get_remote_list_by_sql(sql)
        return rst


    def get_section_function_json(self):
        rst_section=self.query_branch_section_menu()
        json_result=[]
        for section_row in rst_section:
            rst_function=self.query_branch_function_menu(section_row['centid'],section_row['sectionid'])
            section_row['functions']=rst_function
            json_result.append(section_row)

        json_result_str=json.dumps(json_result,cls=MsSqlResultDataEncoder)

        return json_result_str




