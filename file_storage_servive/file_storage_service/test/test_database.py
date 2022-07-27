import unittest
from file_storage_service.models import database

class MyTestCase(unittest.TestCase):
    def test_something(self):

        user = database.User()
        user.set_password('Hik123456')
        print(user.pwd)
        user.set_password('Hik123456')
        res = user.authenticate('Hik123456')
        print(user.pwd)
        self.assertEqual(res, True)


if __name__ == '__main__':
    unittest.main()
