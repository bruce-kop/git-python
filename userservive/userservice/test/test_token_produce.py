#encoding=utf8
import unittest
from userservice.utils.tokenProducer import Jwt,TOKEN_PRODUCE_KEY
from userservice.utils.res_msg_enum import ResMSG

class MyTestCase(unittest.TestCase):
    def test_token_producer_succ_001(self):
        # 测试
        s = Jwt.encode({"name": "lyt"}, TOKEN_PRODUCE_KEY, 300)  # 制作令牌
        print(s)
        d = Jwt.decode(s, TOKEN_PRODUCE_KEY)  # 校验令牌 返回payload明文 字典类型
        print(d)
        self.assertEquals(d['name'], "lyt")


if __name__ == '__main__':
    unittest.main()

