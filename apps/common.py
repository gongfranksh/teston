# -*- coding:utf-8 -*-
from datetime import datetime
import json

def trueReturn(data, msg):
    return {
        "status": True,
        "data": data,
        "msg": msg
    }


def falseReturn(data, msg):
    return {
        "status": False,
        "data": data,
        "msg": msg
    }


# 对象转为json字符串
def obj2dict(obj):
    dd = {}
    # 展开它的属性
    for m in dir(obj):
        if m[0] != "_":
            value = getattr(obj, m)
            if not callable(value):
                dd[m] = complexObj2json(value)
    return dd


def list2json(ll):
    res_list = []
    for item in ll:
        value = complexObj2json(item)
        res_list.append(value)
    return res_list


def dict2json(dd):
    res = {}
    for item in dd:
        res[item] = complexObj2json(dd[item])
    return res

# complex obj to json
# 复杂对象转换json对象 (dict、list)
def complexObj2json(obj):
    # list, set, tuple
    if isinstance(obj, (list, set, tuple)):
        return list2json(obj)
    # dict
    elif isinstance(obj, dict):
        return dict2json(obj)
    # string
    elif isinstance(obj, str):
        return obj
    # 基本类型
    # int, long, basestring, bool, float
    elif obj == None or isinstance(obj, (int,complex, bool, float)):
        return obj
    elif isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    # 用户自定义的类
    else:
        return obj2dict(obj)


"""
class Tiger():
     xiao=[]
     username=""
     xialbing=""


# 把json转为字符串
#json = '{"a":1,"b":2,"c":3,"d":4,"e":5}';


python_object = "{ 'name':'Peggy','email':'peggy@gmail.com','homepage':'http://www.peggy.com'}"
json_string = '{"favorited": false, "contributors": null,"xiaobing":"xiaoldjnnd"}'
#print(python_object['name'])
# text = json.loads(json)
# print(text['a'])
# Converting Python to JSON

json_object = json.loads(json_string)
print(json_object['xiaobing'])
# Converting JSON to Python
python_object = json.dumps(json_string)
print(python_object)

from flask import json as ojson

print(ojson.dumps(json_object))

lastobj = ojson.loads(json_string)
print(json_object['xiaobing'])

"""