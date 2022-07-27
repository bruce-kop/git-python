#encoding = uts8
import re

class VerifyUtil:
    @staticmethod
    def verify_phone(phone):
        # A regular expression for the mobile phone number format
        reg = '^1(3[0-9]|4[5,7]|5[0,1,2,3,5,6,7,8,9]|6[2,5,6,7]|7[0,1,7,8]|8[0-9]|9[1,8,9])\d{8}$'
        return re.match(reg, phone)

    @staticmethod
    def verify_pwd(pwd):
        '''A regular expression for the pwd format
        The password must contain at least three types of characters and contain at least eight characters, maximum of 32 characters
            big lettles,such as A,B,C...Z
            little lettles, such as a,b,c...z
            digits,such as 0,1,2...9
            special characters, such as {}[],<>@$%&^()_+=
        '''
        reg = '^(?:' \
              '(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])|' \
              '(?=.*[A-Z])(?=.*[a-z])(?=.*[^A-Za-z0-9])|' \
              '(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])|' \
              '(?=.*[a-z])(?=.*[0-9])(?=.*[^A-Za-z0-9])).{8,32}$'
        return re.match(reg, pwd)