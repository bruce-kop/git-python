#dencoding = utf8
import requests
import re
import json
import base64, io
import time
import pytesseract
from PIL import Image


def set_head(hd, key ,value):
    hd[key] = value
    return hd

def get_base_head():
    hd = {
        'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Content-type':'application/json'
        }
    return hd
def set_params(p,key,value):
    p[key] = value
    return p


def verfifycode():
    hd = get_base_head()
    p={}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/verifycode'
    res = requests.post(url, headers=hd, json=p)

    print(res.text)
    json_data = json.loads(res.text)

    return json_data['data']['verifycode']
    #json_data = json.loads(res.text)
    #print(json_data)

def register(code):
    hd = get_base_head()
    p={'username':'bruce','phone':'15382359899','pwd':'Hik123456', 'verifycode':code}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/register'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)
    #json_data = json.loads(res.text)
    #print(json_data)

def login():
    hd = get_base_head()
    p={'username':'kebi','phone':'18969196682','pwd':'Hik1234567'}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/login'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)
    json_data = json.loads(res.text)
    return json_data['data']['token']

def logout(token):
    hd = get_base_head()
    p={'token':token}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/logout'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def unsubscribe(token):
    hd = get_base_head()
    p={'token':token}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/unsubscribe'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def user_precise_query(token):
    hd = get_base_head()
    p={'token':token, 'username':'kop'}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/user/precise_query'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)
def user_pwd_modify(token):
    hd = get_base_head()
    p={'token':token, 'old_pwd':'Hik123456', 'new_pwd':'Hik1234567'}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/pwd/modify'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def user_phone_modify(token):
    hd = get_base_head()
    p={'token':token, 'old_phone':'18969196682', 'new_phone':'18969196683'}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/phone/modify'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

if __name__ == '__main__':
    code = verfifycode()
    register(code)
    #token = login()

    #time.sleep(3)
    #user_precise_query(token)
    #user_pwd_modify(token)
    #user_phone_modify(token)
    #logout(token)

    #unsubscribe(token)