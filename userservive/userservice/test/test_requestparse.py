import unittest
from userservice.utils.requestParse import *
import json

class MyTestCase(unittest.TestCase):

    def test_parser_succ_001(self):
        data = b'"{\\"username\\": \\"kebi\\", \\"phone\\": \\"18969196682\\", \\"pwd\\": \\"Hik1234567\\"}"'
        data = parser.parse_to_dict(data)
        print(type(data))

        self.assertIsInstance(data, dict)  # add assertion here


if __name__ == '__main__':
    unittest.main()
