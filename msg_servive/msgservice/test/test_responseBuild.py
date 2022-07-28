import unittest
from msgservice.utils.responseBuild import responseBuilder
from msgservice.utils.res_msg_enum import ResMSG
class MyTestCase(unittest.TestCase):
    def test_something(self):
        response =responseBuilder.build_response(code=201,msg= ResMSG.LOGOUT_SUCCESS.value, username='kop', phone = '15382359899', avate = 'http://www.baidu.com/gg')
        print(response)
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
