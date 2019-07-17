import json
from flask import jsonify, request
from sqlalchemy import desc

from apps.auths import Auth
from apps.model1 import User
from apps.common import trueReturn, complexObj2json, falseReturn
from flask.json import JSONDecoder,JSONEncoder
from apps.cache_utils import getUserById

from flask_login import login_required, current_user,login_user,logout_user,utils

from apps.jwt_utils import jwtEncoding,jwtDecoding

from apps import login_manager

class  Dog():
    lisn='sdfds'
    ous='23432'

    def __init__(self,lisn=None,ous=None):
        self.lisn =lisn
        self.ous = ous



class Cat():
    slit=[]
    ous='3ewer'
    username = '2w34'
    size=12
    slit.append('sdfsd')
    slit.append('sdf2d')
    slit.append('sdf2d')
    dog = Dog(lisn='wer',ous='234')
    xiaoban=12

    def say(self):
        return "ok!!!"

    def __init__(self,username,slit,size):
        self.username = username
        self.slit =slit
        self.size = size

    def  __str__(self):
        return  self.__dict__

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
            return jsonify(trueReturn(returnUser, "用户注册成功"))
        else:
            return jsonify(falseReturn('', '用户注册失败'))

    @app.route('/xiaoming')
    def getUser():
        slices =[]
        slices.append('sdfsd')
        slices.append('sdf2d')
        slices.append('sdf2d')
        lons = Cat(username='e3rwer',slit=slices, size=12)


        print(lons.__dict__)
        print(vars(lons))
        print(Cat.__dict__)
        jstr=complexObj2json(lons)
        jstr = str(jstr)
        print(jstr)
        print("===========================")
        users = User.query.all()
        print("===============")
        jstr ='{"xiao":"23423","er":12}'
        js01= JSONDecoder().decode(jstr)
        print(js01["xiao"])
        llo = complexObj2json(lons)
        print(llo["username"])
        dis =llo["dog"]
        print(dis["ous"])
        return jsonify(trueReturn(jstr, "用户注册成功"))

    @app.route('/des',methods=['POST'])
    def getdl2():
        str = request.get_json()
        print(str)
        print(str['username'])
        str2=request.get_data()
        print(str2)
        return jsonify(trueReturn("{'ok':True}", "for sucess"))


    @login_manager.request_loader
    def load_user_from_request(request):
        api_key = request.headers.get('Authorization')
        print(api_key)
        if api_key:
            obj = jwtDecoding(api_key)
            user = obj['some']
            if user:
                user = getUserById(user['id'])
                return user
            else:
                print("is exception !!!!"+str(obj['error_msg']))
                return None

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
            "id":admin.id,
            "username":admin.username,
            "email":admin.email
        }

        if admin == None:
            return jsonify(trueReturn("{'ok':Flase}", "not the user"))
        else:
            #request.headers['Authorization']='liuliuyyeshibushidslfdslfsdkfkdsf23234243kds'
            #login_user(admin)
            token = jwtEncoding(userInfo)
            print(token)
            return Auth.authenticate(Auth, name, password)
            # return jsonify(trueReturn("{'ok':True,'token':"+token.decode()+"}", "you are sucess"))

    @app.route('/info/<id>', methods=['GET', 'POST'])
    @login_required
    def getxiaomingInfo(id):
        lds =  admin = User.query.filter_by(id=id).first()
        print(str(lds))
        return jsonify(trueReturn("{'ok':True}", "you are sucess"))

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return jsonify(trueReturn("{'ok':True}", "you are sucess"))

    @app.route('/cun')
    @login_required
    def getUser2():
        user=utils._get_user()
        print(user.__dict__)
        return jsonify(trueReturn("{'ok':True}", "cun success!!!!!"))

