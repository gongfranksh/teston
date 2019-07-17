# -*- coding: utf-8 -*-
from apps.Entity.jsEntity import JsEntity


class ProductBarCode(JsEntity):

    def __init__(self, branchcode):
        JsEntity.__init__(self, "Product_barcode", branchcode)
        self.branch_code = branchcode
        self.base_query_sql = """
            SELECT braid, ProId, Barcode, ProName, ProSName, sectionid, bigclass, ClassId, Spec, 
            isnull(BrandId,'') AS BrandId, isnull(Statid,'') StatId, Grade, Area, SupId, MeasureId, 
            PacketQty, PacketQty1,  
            isnull(TaxType,'') TaxType, isnull(InTax,0) InTax, isnull(SaleTax,0) SaleTax, 
            isnull(InPrice,0) InPrice, isnull(TaxPrice,0) TaxPrice,  isnull(NormalPrice,0)  NormalPrice,isnull(MemberPrice,0)  MemberPrice,
            isnull(GroupPrice,0)   GroupPrice,  isnull(avgcostprice,0)   avgcostprice, 
            isnull(MainFlag,0)   MainFlag, isnull(ProFlag,0)   ProFlag, WeightFlag, Barmode, OrderMode, 
            isnull(MinOrderQty,0) MinOrderQty, isnull(OrderMultiplier,0) OrderMultiplier, FreshMode, isnull(ReturnRat,1) ReturnRat, 
            isnull(cardpoint,0)  cardpoint, status, PromtFlag, PotFlag, CanChangePrice, 
            CreateDate, UpdateDate, isnull(vipdiscount,1) VipDisCount, isnull(posdiscount,1) posdiscount, isorder, isnull(minprice,0) minprice, isnull(maxprice,0) maxprice,
            isnull(seatid,'') seatid, maxtimestamp,isnull(guideprice,0) guideprice
            FROM dbo.v_branch_product 
                """

    def get_branch_product_barcode_all(self):
        sql_cond = """
                where braid='{0}'
        """
        sql = self.base_query_sql + sql_cond
        sql=sql.format(self.branch_code)
        rst = self.get_remote_result_by_sql(sql)
        return rst

    def seek_branch_product_barcode(self, barcode):
        sql_cond = """
                where braid='{0}' and barcode='{1}'
                """
        sql = self.base_query_sql + sql_cond
        sql=sql.format(self.branch_code, barcode)

        rst = self.get_remote_result_by_sql(sql)
        return rst

    def seek_branch_product_proid(self, proid):
        sql_cond = """
                where braid='{0}' and proid='{1}'
                """
        sql = self.base_query_sql + sql_cond
        sql =sql.format(self.branch_code, proid)
        rst = self.get_remote_result_by_sql(sql)
        return rst

    def seek_branch_product_proid_us_like(self, proid):
        sql_cond = """
                where braid='{0}' and proid like '%{1}%'
                """
        sql = self.base_query_sql + sql_cond
        sql =sql.format(self.branch_code, proid)
        rst = self.get_remote_result_by_sql(sql)
        return rst

    def seek_branch_product_name(self, proname):
        sql_cond = """
                where braid='{0}' and proname like '%{1}%'
                """
        sql = self.base_query_sql + sql_cond
        sql =sql.format(self.branch_code, proname)
        rst = self.get_remote_result_by_sql(sql)
        return rst
