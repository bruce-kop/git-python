#dencoding = utf8

import requests
import json

class httpclient():

    def __init__(self,server_host):
        self.server_host = server_host

    @staticmethod
    def set_head(hd, key, value):
        hd[key] = value
        return hd

    @staticmethod
    def get_base_head():
        hd = {
            'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
            (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
            'Content-type':'application/json'
            }
        return hd

    @staticmethod
    def set_params(p,key,value):
        p[key] = value
        return p

    def verfifycode(self):
        hd = httpclient.get_base_head()
        p={}
        p = json.dumps(p)
        url = self.server_host+'/api/verifycode'
        res = requests.post(url, headers=hd, json=p)
        json_data = json.loads(res.text)

        return json_data['data'].get('verifycode')

    def common_request(self, api=None, params=None):
        hd = httpclient.get_base_head()
        p = json.dumps(params)
        url = self.server_host + api
        res = requests.post(url, headers=hd, json=p)
        return res.text

    def register(self, code=None, username=None, phone=None, pwd=None):
        hd = httpclient.get_base_head()
        p = {
            'username': username,
            'phone': phone,
            'pwd': pwd,
            'verifycode': code
        }
        p = json.dumps(p)
        url = self.server_host+'/api/register'
        res = requests.post(url, headers=hd, json=p)
        return res.text

    def login(self, code=None, username=None, phone=None, pwd=None):
        hd = httpclient.get_base_head()
        if code:
            p = {'username': username, 'phone': phone, 'pwd': pwd}
        else:
            p = {'username': username, 'phone': phone, 'pwd': pwd, 'verifycode': code}
        p = json.dumps(p)
        url = self.server_host+'/api/login'
        res = requests.post(url, headers=hd, json=p)

        json_data = json.loads(res.text)
        print(json_data)
        return json_data['data'].get('token')

    def logout(self, token):
        hd = httpclient.get_base_head()
        p = {'token':token}
        p = json.dumps(p)
        url = self.server_host+'/api/logout'
        res = requests.post(url, headers=hd, json=p)

        return res.text

    def unsubscribe(self, token):
        hd = httpclient.get_base_head()
        p =  {'token': token}
        p = json.dumps(p)
        url = self.server_host+'/api/unsubscribe'
        res = requests.post(url, headers=hd, json=p)

        return res.text

    def user_precise_query(self, token, username=None, phone=None):
        hd = httpclient.get_base_head()
        if username:
            p={'token': token, 'username':username}
        else:
            if phone:
                p = {'token': token, 'phone': phone}
            else:
                return None
        p = json.dumps(p)
        url = self.server_host+'/api/user/precise_query'
        res = requests.post(url, headers=hd, json=p)

        return res.text

    def user_pwd_modify(self, token, old_pwd=None, new_pwd=None):
        hd = httpclient.get_base_head()
        p={'token': token, 'old_pwd': old_pwd, 'new_pwd': new_pwd}
        p = json.dumps(p)
        url = self.server_host+'/api/pwd/modify'
        res = requests.post(url, headers=hd, json=p)

        return res.text

    def user_phone_modify(self, token, old_phone=None, new_phone=None):
        hd = httpclient.get_base_head()
        p={'token': token, 'old_phone':old_phone, 'new_phone': new_phone}
        p = json.dumps(p)
        url = self.server_host+'/api/phone/modify'
        res = requests.post(url, headers=hd, json=p)

        return res.text


if __name__ == '__main__':
    pass

    #client = httpclient()
    #code = client.verfifycode()
    #register(code)
    #token = login()

    #time.sleep(3)
    #user_precise_query(token)
    #user_pwd_modify(token)
    #user_phone_modify(token)
    #logout(token)

    #unsubscribe(token)