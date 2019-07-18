from flask import Blueprint, jsonify
from flask_login import login_required

from apps.Js.Entity.Branch import Branch
from apps.Js.Entity.Member import Member
from apps.Js.Entity.ProductBarCode import ProductBarCode
from apps.Utils.common import trueReturn
from apps.Utils.message import API_SUCCESS_MSG

jsapi = Blueprint('jspai', __name__,
                        template_folder='templates')

# @jsapi.route('/js')
# @login_required
# def show():
#     try:
#         print('go to ss')
#         return jsonify(trueReturn("ok", REGISTER_SUCCESS_MSG))
#     except TemplateNotFound:
#         abort(404)


@jsapi.route("/js/branch", methods=['GET', 'POST'])
@login_required
def get_branch_result():
    branchcode = '01001'
    branch = Branch(branchcode)
    rst = branch.get_branch_all()
    return jsonify(trueReturn(rst, API_SUCCESS_MSG))


@jsapi.route("/js/product/<branchcode>/<barcode>", methods=['GET', 'POST'])
@login_required
def get_product_by_barcode(branchcode, barcode):
    productbarcode = ProductBarCode(branchcode)
    rst = productbarcode.seek_branch_product_barcode(barcode)
    # barcode查询步到，使用prodid查询
    if len(rst) == 2:
        rst = productbarcode.seek_branch_product_proid(barcode)
    return jsonify(trueReturn(rst, API_SUCCESS_MSG))

@jsapi.route("/js/member/<mobile>", methods=['GET', 'POST'])
@login_required
def Get_memeber_by_mobile(mobile):
     member = Member()
     rst = member.seek_memeber_by_mobile(mobile)
     return jsonify(trueReturn(rst, API_SUCCESS_MSG))
