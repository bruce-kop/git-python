import unittest
from libs.responseBuild import responseBuilder

class responseBuilderTestCase(unittest.TestCase):
    def test_something(self):
        ret = responseBuilder.build_common_suc()
        self.assertIsInstance(ret,str)

        ret = responseBuilder.build_verifycode_faild()
        self.assertIsInstance(ret, str)

        ret = responseBuilder.build_register_faild()
        self.assertIsInstance(ret, str)

        ret = responseBuilder.build_verifycode_suc("dfsadf","fsdf")
        self.assertIsInstance(ret, str)

        ret = responseBuilder.build_login_faild()
        self.assertIsInstance(ret, str)


if __name__ == '__main__':
    unittest.main()
