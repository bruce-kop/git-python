#dencoding = utf8
import requests
import re
import json
import base64, io
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

def register(username = None, phone = None, code = None):
    hd = get_base_head()
    p={'username':username,'phone':phone,'pwd':'Hik123456', 'verifycode':code}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/register'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)
    #json_data = json.loads(res.text)
    #print(json_data)

def login(username = None,phone= None,pwd = 'Hik1234567'):
    hd = get_base_head()
    p={'phone':phone,'pwd':pwd}
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

import random
import string

# 运营商的号码前缀
prefix = [
    '130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
    '145', '147', '149', '150', '151', '152', '153', '155', '156', '157',
    '158', '159', '165', '171', '172', '173', '174', '175', '176', '177',
    '178', '180', '181', '182', '183', '184', '185', '186', '187', '188',
    '189', '191'
    ]


def phone_builder():
    # 随机取一个手机号前缀
    rom = random.randint(0, len(prefix) - 1)
    # 随机生成后8位数字，string.digits是数字0~9
    suffix = ''.join(random.sample(string.digits, 8))
    # 拼接返回11位手机号
    return prefix[rom] + suffix


def username_builder():
    return  ''.join(random.sample(string.ascii_letters + string.digits, 8))

def register_users():
    for i in range(1000):
        code = verfifycode()
        username = username_builder()
        phone = phone_builder()
        print(username,phone)
        register(username=username,phone=phone,code = code)
        time.sleep(1)


def add_friend(token, friendid):
    hd = get_base_head()
    p = {'token': token, 'friend_id': friendid}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5001/api/friend/add'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def del_friend(token, friendid):
    hd = get_base_head()
    p = {'token': token, 'friend_id': friendid}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5001/api/friend/del'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def list_friend(token, currentPage):
    hd = get_base_head()
    p = {'token': token, "pageSize": 5, 	"currentPage": currentPage}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5001/api/friend/list'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)


def set_permission_friend(token, friendid, friend_au):
    hd = get_base_head()
    p = {'token': token, "friend_id": friendid, 	"friend_au": friend_au}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5001/api/friend/set_permission'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def set_note_friend(token, friendid,note):
    hd = get_base_head()
    p = {'token': token, "friend_id": friendid, 	"note": note}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5001/api/friend/set_note'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def set_label_friend(token, friendid,friend_label):
    hd = get_base_head()
    p = {'token': token, "friend_id": friendid, 	"friend_label": friend_label}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5001/api/friend/set_label'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def list_friend(token, pageSize = 10,currentPage = 0):
    hd = get_base_head()
    p = {'token': token, "pageSize": pageSize, 	"currentPage": currentPage}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5001/api/friend/list'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def add_group(token, name,members):
    hd = get_base_head()
    p = {'token': token, "name":name, 'members': members}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5002/api/group/add'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def del_group(token, groupid):
    hd = get_base_head()
    p = {'token': token, "groupid":groupid}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5002/api/group/del'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def del_members(token, groupid,members):
    hd = get_base_head()
    p = {'token': token, "groupid":groupid, "members":members}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5002/api/group/del_member'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def add_members(token, groupid,members):
    hd = get_base_head()
    p = {'token': token, "groupid":groupid, "members":members}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5002/api/group/add_member'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def set_group_name(token, groupid,name):
    hd = get_base_head()
    p = {'token': token, "groupid":groupid, "name":name}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5002/api/group/set_name'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def set_group_notice(token, groupid,notice):
    hd = get_base_head()
    p = {'token': token, "groupid":groupid, "notice":notice}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5002/api/group/set_notice'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def set_group_note(token, groupid,note):
    hd = get_base_head()
    p = {'token': token, "groupid":groupid, "note":note}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5002/api/group/set_note'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def group_list(token):
    hd = get_base_head()
    p = {'token': token}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5002/api/group/get_groups'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def save_to_addr(token, groupid):
    hd = get_base_head()
    p = {'token': token,'groupid':groupid}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5002/api/group/save_to_addr'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def QR_code(token, groupid):
    hd = get_base_head()
    p = {'token': token,'groupid':groupid}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5002/api/group/QR_code'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def set_member_role(token,groupid,role_id,members):
    hd = get_base_head()
    p = {'token': token,'groupid':groupid, "role_id":role_id, "members":members}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5002/api/group/set_member_role'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def member_list(token,groupid):
    hd = get_base_head()
    p = {'token': token,'groupid':groupid}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5002/api/group/member_list'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def member_info(token,groupid,memberid):
    hd = get_base_head()
    p = {'token': token,'groupid':groupid, 'memberid':memberid}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5002/api/group/member_info'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def group_list_in_addr(token):
    hd = get_base_head()
    p = {'token': token}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5002/api/group/groups_in_addr_book'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def find(token,type= "group", msg_from =None):
    hd = get_base_head()
    if type == 'user':
        p = {'token': token, 'char_session':{'type':type, 'friend': msg_from}, "pageIndex": 1, "pageSize": 5}
    elif type == 'group':
        p = {'token': token, 'char_session': {'type': type, 'group': msg_from}, "pageIndex": 1, "pageSize": 5}
    else:
        return
    p = json.dumps(p)
    url = 'http://127.0.0.1:5003/api/msg/find'
    res = requests.post(url, headers=hd, json=p)
    response = json.loads(res.text)
    datas = response.get('data').get('messages')
    for d in datas:
        print(d.get('created_at'))

    print(response)

def find_message_by(token,type = "group",msg_from = None, msg_type = "text" ):
    hd = get_base_head()
    if type == 'user':
        p = {'token': token, 'char_session': {'type': type, 'friend': msg_from}, "msg_type": msg_type, "pageIndex": 1,
             "pageSize": 5}
    elif type == 'group':
        p = {'token': token, 'char_session': {'type': type, 'group': msg_from}, "msg_type": msg_type, "pageIndex": 1,
             "pageSize": 5}
    else:
        return
    p = json.dumps(p)
    url = 'http://127.0.0.1:5003/api/msg/find_by'
    print(p)
    res = requests.post(url, headers=hd, json=p)
    response = json.loads(res.text)
    datas = response.get('data').get('messages')
    for d in datas:
        print(d.get('created_at'))

    print(response)

def find_message_by_kw(token,type = "group",msg_from = None, kw = None ):
    hd = get_base_head()
    p = {'token': token, 'char_session':{'type':type, 'msg_from': msg_from}, "key_word":kw,"pageIndex": 1, "pageSize": 5}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5003/api/msg/find_by_kw'
    print(p)
    res = requests.post(url, headers=hd, json=p)
    response = json.loads(res.text)
    datas = response.get('data').get('messages')
    for d in datas:
        print(d.get('created_at'))

    print(response)

def find_message_by_member(token,groupid, memberid):
    hd = get_base_head()
    p = {'token': token, 'groupid': groupid, "memberid": memberid,"pageIndex": 1, "pageSize": 5}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5003/api/msg/find_by_member'

    res = requests.post(url, headers=hd, json=p)
    response = json.loads(res.text)

    print(response)

def find_by_date(token,type = "group",msg_from = None , start_date = None, end_date = None):
    hd = get_base_head()
    p = {'token': token, 'char_session':{'type':type, 'msg_from': msg_from}, "start_date":start_date, "end_date":end_date, "pageIndex": 1, "pageSize": 5}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5003/api/msg/find_by_date'
    res = requests.post(url, headers=hd, json=p)
    response = json.loads(res.text)
    datas = response.get('data').get('messages')
    for d in datas:
        print(d.get('created_at'))

    print(response)

def find_chats(token):
    hd = get_base_head()
    p = {'token': token, "pageIndex": 1, "pageSize": 5}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5003/api/msg/find_chats'
    res = requests.post(url, headers=hd, json=p)
    response = json.loads(res.text)

    print(response)

def find_unreaders(token,msf_ids):
    hd = get_base_head()
    p = {'token': token, "msg_ids": msf_ids}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5003/api/msg/unreaders'
    res = requests.post(url, headers=hd, json=p)
    response = json.loads(res.text)

    print(response)

import datetime
from datetime import time

if __name__ == '__main__':

    #register_users()
    token = login(phone='18969196681', pwd='Hik123456')
    #find(token, type= "user", msg_from = "ba0b7df0-a7ca-4a31-93d6-e0bcefc41ddc")
    #find(token, type= "group", msg_from ="42177ae4-81bf-4bc8-8fc5-74a025cd154f")

    #find_message_by(token, type= "user", msg_from = "f692b513-8e1c-410a-927b-58687b85dcc8", msg_type="text")
    #find_message_by(token, type="group", msg_from="42177ae4-81bf-4bc8-8fc5-74a025cd154f", msg_type="text")
    #find_message_by(token, type="user", msg_from="f692b513-8e1c-410a-927b-58687b85dcc8",msg_type="file")
    #find_message_by(token, type="group", msg_from="42177ae4-81bf-4bc8-8fc5-74a025cd154f",msg_type="file")
    #find_message_by(token, type="user", msg_from="f692b513-8e1c-410a-927b-58687b85dcc8",msg_type="link")
    #find_message_by(token, type="group", msg_from="42177ae4-81bf-4bc8-8fc5-74a025cd154f",msg_type="link")

    #find_message_by(token, type="user", msg_from="f692b513-8e1c-410a-927b-58687b85dcc8",msg_type="pic")
    #find_message_by(token, type="group", msg_from="42177ae4-81bf-4bc8-8fc5-74a025cd154f",msg_type="pic")

    #find_message_by(token, type="user", msg_from="ba0b7df0-a7ca-4a31-93d6-e0bcefc41ddc",msg_type="video")
    #find_message_by(token, type="group", msg_from="42177ae4-81bf-4bc8-8fc5-74a025cd154f", msg_type="video")

    start_date = datetime.datetime.combine(datetime.date(2022,7,29), time(17,8,00))
    end_date = datetime.datetime.combine(datetime.date(2022,7,29), time(17,20,0))
    d = datetime.date(2022, 7, 29)
    t = time(17, 20, 0)
    s = start_date.strftime("%Y-%m-%d %H:%M:%S")
    e = end_date.strftime("%Y-%m-%d %H:%M:%S")
    #find_by_date(token, type="group", msg_from="42177ae4-81bf-4bc8-8fc5-74a025cd154f", start_date= s,end_date= e)
    #find_by_date(token, type="user", msg_from="f692b513-8e1c-410a-927b-58687b85dcc8", start_date= s,end_date= e)
    #find_message_by_member(token, "42177ae4-81bf-4bc8-8fc5-74a025cd154f", "ba0b7df0-a7ca-4a31-93d6-e0bcefc41ddc")
    #find_message_by_kw(token, type="group",msg_from="42177ae4-81bf-4bc8-8fc5-74a025cd154f", kw="你好")
    #find_message_by_kw(token, type="user", msg_from="f692b513-8e1c-410a-927b-58687b85dcc8", kw = "visit")
    #find_chats(token)
    s = '058fd28a-f870-444a-8e16-cf01c678961e'
    print(len(s.encode('utf-8')))
    msg_ids = ["fc759ebe-84b0-4f61-87ee-773a4c6a1a35", "6b5b495d-3401-491b-94b4-6d7caef6a59c", "e7c3ead3-9708-4383-87dd-2dfe01f79fbc"]

    #find_unreaders(token, msg_ids)

    d1 = {"a": 1, "b": 2}
    d2 = {"a": 1, "b": 2}

    if d1 == d2:
        print('success')

