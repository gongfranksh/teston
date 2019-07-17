# -*- coding: utf-8 -*-
import json
import time
import uuid

from Entity.jsEntity import JsEntity


class PosOrder(JsEntity):
    def __init__(self):
        JsEntity.__init_no_branchcode__(self, "SaleDaily")

    def Submit_PosOrder(self, transcation):
        try:
            if transcation != None:
                trans = json.loads(transcation)
                branch = json.loads(trans['branch'])
                operator = json.loads(trans['operator'])
                saledaily = json.loads(trans['saledaily'])
                payment = json.loads(trans['payment'])
                member = json.loads(trans['member'])
                posmachine = json.loads(trans['posmachine'])
                deviceid = trans['device_uuid']
                transid = trans['trans_uuid']

                self.braid = branch['braid']
                self.posno = posmachine['posno']

                self.tmp_saleid = self.get_current_saleid()

                for order in saledaily:
                    self.insert_into_saledaily(order)

                for payment in payment:
                    self.inser_into_salepayment(payment)

                resultjson = [{'pos_order_submit_state': 'ok',
                               'pos_order_submit_innerid': transid,
                               'pos_order_submit_deviceid': deviceid,
                               'pos_order_return_saleid': self.tmp_saleid,
                               }]

                str_resultjson = json.dumps(resultjson)

        except Exception as e:
            print(e.message)
            resultjson = {'pos_order_submit_state': 'error'}
            str_resultjson = json.dumps(resultjson)

        return str_resultjson

    #产生交易流水编号
    def get_current_saleid(self):

        #获取当日门店同一个收银机最后一笔正常交易号码
        sql = """
                SELECT saleid
                FROM mobile_sale_daily
                WHERE id IN (
                    SELECT MAX(id)
                    FROM mobile_sale_daily
                    WHERE BraId = '{0}'
                        AND PosNo = '{1}'
                        AND substring(saleid,1,1)!='R'
                        AND datediff(day, saledate, getdate()) = 0
                )        
            """
        sql = sql.format(self.braid, self.posno)

        #最后流水4位，取1000 截取后四位
        seq_number = 10000

        rst = self.get_remote_list_by_sql(sql)

        #如果有记录，流水加一，否则从一开始计算
        if len(rst) == 1:
            seq_number += int(rst[0]["saleid"][-4:])

        tmp_saleid = self.posno + time.strftime('%y%m%d', time.localtime(time.time())) + str(seq_number + 1)[-4:]
        return tmp_saleid





    def inser_into_salepayment(self, paymentbean):
        uploadtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        tmp_saleid = ''
        tmp_cardtype = ''
        tmp_cardno = ''

        # if paymentbean.has_key('SaleId'):
        #     tmp_saleid=paymentbean['SaleId']

        if paymentbean.has_key('cardtype'):
            tmp_cardtype = paymentbean['cardtype']

        if paymentbean.has_key('cardno'):
            tmp_cardno = paymentbean['cardno']

        insert_statment = """
            INSERT INTO dbo.mobile_sale_paymode (
                BraId, SaleDate, SaleId, SalerId, PaymodeId, 
                PayMoney, cardtype, cardno, uploadtime, orderinnerid,
                deviceid)
            values (
              '{0}','{1}','{2}','{3}','{4}',
              {5},'{6}','{7}','{8}','{9}','{10}'
            )
        """

        insert_statment = insert_statment.format(
            paymentbean['Braid'], paymentbean['SaleDate'], self.tmp_saleid, paymentbean['SalerId'],
            paymentbean['PayModeId'],
            paymentbean['PayMoney'], tmp_cardtype, tmp_cardno, uploadtime,
            paymentbean['OrderInnerId'], paymentbean['DeviceId']
        )
        self.execSql(insert_statment)
        # print insert_statment

    def insert_into_saledaily(self, orderbean):
        uploadtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        tmp_IsDM = ''
        tmp_IsPmt = ''
        tmp_IsTimePrompt = ''

        tmp_SaleDisAmt = 0.00
        tmp_TransDisAmt = 0.00
        tmp_AvgCostPrice = 0.00
        tmp_LastCostPrice = 0.00
        tmp_SaleId = ''

        tmp_MemCardNo = ''
        tmp_InvoiceId = ''
        tmp_Points1 = 0.00
        tmp_Points2 = 0.00
        tmp_ReturnRat = 0.00

        tmp_SaleType = ''

        if orderbean.has_key('SaleType'):
            tmp_SaleType = orderbean['SaleType']

        if orderbean.has_key('IsDM'):
            tmp_IsDM = orderbean['IsDM']

        if orderbean.has_key('IsPmt'):
            tmp_IsPmt = orderbean['IsPmt']

        if orderbean.has_key('IsTimePrompt'):
            tmp_IsPmt = orderbean['IsTimePrompt']

        if orderbean.has_key('SaleDisAmt'):
            tmp_SaleDisAmt = orderbean['SaleDisAmt']

        if orderbean.has_key('TransDisAmt'):
            tmp_TransDisAmt = orderbean['TransDisAmt']

        if orderbean.has_key('AvgCostPrice'):
            tmp_AvgCostPrice = orderbean['AvgCostPrice']

        if orderbean.has_key('LastCostPrice'):
            tmp_LastCostPrice = orderbean['LastCostPrice']

        # if orderbean.has_key('SaleId'):
        #     tmp_SaleId = orderbean['SaleId']

        if orderbean.has_key('MemCardNo'):
            tmp_MemCardNo = orderbean['MemCardNo']

        if orderbean.has_key('InvoiceId'):
            tmp_InvoiceId = orderbean['InvoiceId']

        if orderbean.has_key('Points1'):
            tmp_Points1 = orderbean['Points1']

        if orderbean.has_key('Points2'):
            tmp_Points2 = orderbean['Points2']

        if orderbean.has_key('ReturnRat'):
            tmp_ReturnRat = orderbean['ReturnRat']

        insert_statment = """
         INSERT INTO dbo.mobile_sale_daily 
         (BraId, SaleDate, ProId, Barcode, ClassId, IsDM, IsPmt, IsTimePrompt, SaleTax, PosNo, 
         SalerId, SaleMan, SaleType, SaleQty, SaleAmt, SaleDisAmt, TransDisAmt, NormalPrice, CurPrice, AvgCostPrice, 
         LastCostPrice, SaleId, MemCardNo, InvoiceId, Points1, Points, ReturnRat, 
         cash1, cash2, cash3, cash4, cash5, cash6, cash7, cash8, 
         uploadtime, orderinnerid, deviceid)
        values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}',{8},'{9}',
                '{10}','{11}','{12}',{13},{14},{15},{16},{17},{18},{19},
                {20},'{21}','{22}','{23}',{24},{25},{26},
                {27},{28},{29},{30},{31},{32},{33},{34},
                '{35}','{36}','{37}'
        )
        """
        insert_statment = insert_statment.format(
            orderbean['Braid'], orderbean['SaleDate'], orderbean['ProId'], orderbean['BarCode'], orderbean['ClassId'],
            tmp_IsDM, tmp_IsPmt, tmp_IsTimePrompt, orderbean['SaleTax'], orderbean['PosNo'],
            orderbean['SalerId'], orderbean['SaleMan'], tmp_SaleType, orderbean['SaleQty'], orderbean['SaleAmt'],
            tmp_SaleDisAmt, tmp_TransDisAmt, orderbean['NormalPrice'], orderbean['CurPrice'], tmp_AvgCostPrice,
            tmp_LastCostPrice, self.tmp_saleid, tmp_MemCardNo, tmp_InvoiceId, tmp_Points1,
            tmp_Points2, tmp_ReturnRat,
            orderbean['Cash1'], orderbean['Cash2'], orderbean['Cash3'], orderbean['Cash4'], orderbean['Cash5'],
            orderbean['Cash6'], orderbean['Cash7'], orderbean['Cash8'],
            uploadtime, orderbean['OrderInnerId'], orderbean['DeviceId']
        )

        self.execSql(insert_statment)
        return 'ok'
