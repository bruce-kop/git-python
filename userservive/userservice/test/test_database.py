import unittest
from userservice.models import database

class MyTestCase(unittest.TestCase):

    def test_user_authenticate_succ_001(self):

        user = database.User()
        user.set_password('Hik123456')
        res = user.authenticate('Hik123456')
        self.assertEqual(res, True)
    def test_user_authenticate_err_001(self):

        user = database.User()
        user.set_password('Hik123456')
        res = user.authenticate('Hik1234567')
        self.assertEqual(res, False)

    def test_user_authenticate_err_002(self):
        user = database.User()
        user.set_password('Hik123456')
        res = user.authenticate('')
        self.assertEqual(res, False)

if __name__ == '__main__':
    unittest.main()
