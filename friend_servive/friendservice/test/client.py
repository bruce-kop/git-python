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

if __name__ == '__main__':

    #register_users()
    token = login(phone='15382359899',pwd='Hik123456')


    friends = ['005ebcc8-8105-4f33-abe9-ffb5a938229b',
     '00a94fd7-550e-478f-b5b5-dc6801537ab3',
     '00b4cd05-8774-4512-b643-eddd519cac43',
     '00c211fa-f43f-401b-848e-db03c9af2485',
     '00ffc2db-7c77-49e2-a71d-155362fd2db5',
     '0142ecea-222e-4116-bce9-893fe09e83a8',
     '017ff76b-15ee-4dcf-9b1b-1a2124e25f8f',
     '01869816-82f2-4df3-b2e4-2426860d08d0',
     '01a56fb0-f093-445e-98ec-59c301d9d0f1',
     '01b3067d-9ea9-4d01-9d92-250ce9f33caa',
     '02118e43-147e-4158-b692-7554a1a8a2a0',
     '021e6417-4a51-4a5a-b7ce-04219936f0f4',
     '02cd0847-47e6-46c2-a7b8-5c5af5a1941d',
     '035584d4-64a7-445a-a1d3-c7bb26b2506f',
     '0357dcf9-f642-4422-a7b2-4d5565a6a5e8',
     '03e41e13-9184-4f15-a7ce-480e74d16cb5',
     '040b2fed-b4c7-453f-aedd-5cc1658330ba',
     '041d167e-0088-4026-9b03-582bf1097af0',
     '0456c5ca-62de-4f39-84fb-6e9d8026a0d8',
     '047f891d-0d88-4124-9c7c-222de32f458a',
     '048d8972-7517-448a-a845-fb583d366edf',
     '04be3b4d-9546-4310-9026-86ba5df434ac',
     '05b9114b-c236-4167-ac08-5af1229db098',
     '05c491a3-d656-4178-b500-c2b0080f51eb',
     '05fece2e-acf7-4fb5-9312-9d507a92b40a',
     '06ac290f-84b0-405c-b1f0-90490c49809f',
     '06f280c6-8d0d-492d-bc9a-a06beaccc92f',
     '07bab11c-304e-48f5-a7a7-99f29ee87d87',
     '08661ecb-0f07-401c-8d78-663aeae69690',
     '0876cac1-613e-452c-89ad-622662cf0ddf',
     '087ffcb9-2517-40bb-b769-ff2225237615',
     '08939951-92cc-4559-9737-e2cbea45f56f',
     '08f5f307-992f-4343-8461-577a526decaa',
     '09069936-5978-4c7c-b902-2bb2f9985c1c',
     '09151569-0cbe-4b53-a5b8-f2abd99af054',
     '093c6fa8-06ec-4a9b-a29f-f0e2882f75f2',
     '09409169-9107-43d7-a44a-2d1e5728e882',
     '098ec607-bd34-4d5f-9ecc-f35ee78560a7',
     '09d0b3b7-813a-4bd4-a1a8-756a25116053',
     '09d78293-fcf5-4994-ba26-3b13dfbe59e3',
     '0a4e8265-65da-409b-b72d-ab77d4ae9d07',
     '0a7117a1-7705-4208-8095-88b1bea03b00',
     '0a988867-c718-4ca7-a73a-7726991d20b2',
     '0b04767e-b496-4c23-8723-25fa641cd9b0',
     '0b255109-8cc1-4cf5-bec9-49b40b003307',
     '0b714bf1-d6af-4a8e-9c29-130db382b26c',
     '0b881f7a-76f3-4dcf-8f4b-923eaadc03d9',
     '0c3c979a-91f9-472e-b447-e410e40830a6',
     '0cb4c34b-a2dd-4a6c-abe3-9eba4669b1a7',
     '0d1ed5ea-6f91-4d8e-9caa-03abd9f4b8f4',
     '0dec320b-e7eb-4518-821a-8d112e54d536',
     '0dff8ffb-6665-43ba-bd52-a7b47310753f',
     '0e05eaab-d613-44a2-9097-cd146769a8bc',
     '0e492703-d3bc-4504-ac79-edeb51a1b1fd',
     '0f043b70-d454-4fe7-aec0-f2714f4a11e8',
     '0f82dc53-eefd-4a28-bbc7-6d1aa75ab7be',
     '1043df0a-0788-41b8-888b-9f7e9a7b09b5',
     '10c6e0d7-6542-4c24-bd9b-c74a3749a345',
     '10e90f85-a7cf-448b-b7cb-5470c2031b3c',
     '10f1cead-5a5c-4b29-98e8-e81048c195ed',
     '1186768c-5ea9-4130-8071-eb5cef4d243c',
     '11ad0d13-1188-46b0-84df-ee43edc219ae',
     '11f14f65-4f71-4765-bbd7-e097d119d053',
     '12019b8a-4748-4064-8499-4881bd124b3e',
     '12850ad9-7959-4501-a62b-9ee3debac58f',
     '12d0789c-a932-494c-8fbf-bb2d700f3b8c',
     '1327a87b-3929-4cca-9dff-a2b2d2d045b3',
     '1354bad9-cf2b-43da-a8e2-2623500e9a32',
     '13ded83a-f2be-4def-9ad9-f8669c79ca1f',
     '143024ee-6310-4edd-b341-cfe5378ea841']
    '''
    for friend in friends:
        #add_friend(token, friend)
        set_permission_friend(token, friend,'1,2,3,4,5')
        set_note_friend(token, friend,"RTC业务部")
        set_label_friend(token, friend, "kebi")
    # del_friend(token, '005ebcc8-8105-4f33-abe9-ffb5a938229b')
    list_friend(token, pageSize=10, currentPage=1)
    '''
    list_friend(token, pageSize=10, currentPage=1)
