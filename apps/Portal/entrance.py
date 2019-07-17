import json
from flask import jsonify, request
from sqlalchemy import desc

from apps.Auth.auths import Auth
from apps.Auth.Users import User
from apps.Entity.Branch import Branch
from apps.Entity.ProductBarCode import ProductBarCode
from apps.Utils.common import trueReturn, falseReturn
from apps.Utils.cache_utils import getUserById

from flask_login import login_required, logout_user, utils

from apps.Utils.jwt_utils import jwtEncoding

from apps import login_manager
from apps.Utils.message import API_SUCCESS_MSG, API_FAILURE_MSG, REGISTER_SUCCESS_MSG, REGISTER_FAILURE_MSG


def init_api(app):
    @app.route('/')
    def index():
        return 'Index Page'

    @app.route('/register', methods=['POST'])
    def register():
        """
        用户注册
        :return: json
        """
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        # 最后一条记录及其ID
        lastUserRecord = User.query.order_by(desc('id')).first()

        if (lastUserRecord is None):
            newRecordId = 1
        else:
            newRecordId = lastUserRecord.id + 1

        user = User(id=newRecordId, email=email, username=username, password=User.set_password(User, password))
        User.add(User, user)

        userInfo = User.get(User, user.id)
        if userInfo:
            returnUser = {
                'id': userInfo.id,
                'username': userInfo.username,
                'email': userInfo.email,
                'login_time': userInfo.login_time
            }
            return jsonify(trueReturn(returnUser, REGISTER_SUCCESS_MSG))
        else:
            return jsonify(falseReturn('', REGISTER_FAILURE_MSG))

    @app.route('/des', methods=['POST'])
    def getdl2():
        str = request.get_json()
        print(str)
        print(str['username'])
        str2 = request.get_data()
        print(str2)
        return jsonify(trueReturn("{'ok':True}", API_SUCCESS_MSG))

    @login_manager.request_loader
    def load_user_from_request(request):
        result = Auth.identify(Auth, request)
        if (result['status'] and result['data']):
            user = User.get(User, result['data'])
            if user:
                return user
            else:
                print("is exception !!!!")
                return falseReturn('', '用户验证失败')

    @login_manager.user_loader
    def load_user(userid):
        user = getUserById(userid)
        return user

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        name = request.form.get('username')
        password = request.form.get('password')

        admin = User.query.filter_by(username=name).first()

        if admin == None:
            return jsonify(trueReturn("{'ok':Flase}", API_FAILURE_MSG))
        else:
            return Auth.authenticate(Auth, name, password)

    @app.route('/info/<id>', methods=['GET', 'POST'])
    @login_required
    def getuserinfo(id):
        lds = User.query.filter_by(id=id).first()
        return jsonify(trueReturn(json.dumps(lds.columns_to_dict()), API_SUCCESS_MSG))

    @app.route("/logout",methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        return jsonify(trueReturn("{'ok':True}", API_SUCCESS_MSG))


    @app.route("/branch",methods=['GET', 'POST'])
    @login_required
    def get_branch_result():
            branchcode='01001'
            branch = Branch(branchcode)
            rst = branch.get_branch_all()
            return jsonify(trueReturn(rst, API_SUCCESS_MSG))

    @app.route("/product/<branchcode>/<barcode>", methods=['GET', 'POST'])
    @login_required
    def get_product_by_barcode(branchcode, barcode):
        productbarcode = ProductBarCode(branchcode)
        rst = productbarcode.seek_branch_product_barcode(barcode)
        # barcode查询步到，使用prodid查询
        if len(rst) == 2:
            rst = productbarcode.seek_branch_product_proid(barcode)
        return jsonify(trueReturn(rst, API_SUCCESS_MSG))



    #测试取得用户数据
    @app.route('/cun', methods=['GET', 'POST'] )
    @login_required
    def getUser2():
        user = utils._get_user()
        return jsonify(trueReturn(user.columns_to_dict(), API_SUCCESS_MSG))
