import json
from flask import jsonify, request
from sqlalchemy import desc

from apps.Auth.auths import Auth
from apps.Auth.model1 import User
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

    # @app.route('/xiaoming')
    # def getUser():
    #     slices = []
    #     slices.append('sdfsd')
    #     slices.append('sdf2d')
    #     slices.append('sdf2d')
    #     lons = Cat(username='e3rwer', slit=slices, size=12)
    #
    #     print(lons.__dict__)
    #     print(vars(lons))
    #     print(Cat.__dict__)
    #     jstr = complexObj2json(lons)
    #     jstr = str(jstr)
    #     print(jstr)
    #     print("===========================")
    #     users = User.query.all()
    #     print("===============")
    #     jstr = '{"xiao":"23423","er":12}'
    #     js01 = JSONDecoder().decode(jstr)
    #     print(js01["xiao"])
    #     llo = complexObj2json(lons)
    #     print(llo["username"])
    #     dis = llo["dog"]
    #     print(dis["ous"])
    #     return jsonify(trueReturn(jstr, "用户注册成功"))

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
        # else:
        #     return result

        # api_key = request.headers.get('Authorization')
        # print(api_key)
        # if api_key:
        #     obj = jwtDecoding(api_key)
        #     user = obj['some']
        #     if user:
        #         user = getUserById(user['id'])
        #         return user
        #     else:
        #         print("is exception !!!!"+str(obj['error_msg']))
        #         return None

    @login_manager.user_loader
    def load_user(userid):
        user = getUserById(userid)
        return user

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        name = request.form.get('username')
        password = request.form.get('password')

        admin = User.query.filter_by(username=name).first()

        userInfo = {
            "id": admin.id,
            "username": admin.username,
            "email": admin.email
        }

        if admin == None:
            return jsonify(trueReturn("{'ok':Flase}", API_FAILURE_MSG))
        else:
            # request.headers['Authorization']='liuliuyyeshibushidslfdslfsdkfkdsf23234243kds'
            # login_user(admin)
            token = jwtEncoding(userInfo)
            print(token)
            return Auth.authenticate(Auth, name, password)
            # return jsonify(trueReturn("{'ok':True,'token':"+token.decode()+"}", "you are sucess"))

    @app.route('/info/<id>', methods=['GET', 'POST'])
    @login_required
    def getuserinfo(id):
        lds = User.query.filter_by(id=id).first()
        return jsonify(trueReturn(json.dumps(lds.columns_to_dict()), API_SUCCESS_MSG))

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return jsonify(trueReturn("{'ok':True}", API_SUCCESS_MSG))

    @app.route('/cun')
    @login_required
    def getUser2():
        user = utils._get_user()
        print(user.__dict__)
        return jsonify(trueReturn("{'ok':True}", API_SUCCESS_MSG))
