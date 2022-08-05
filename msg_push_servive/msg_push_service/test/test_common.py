import unittest
from msg_push_service.utils.common import *
import json

class MyTestCase(unittest.TestCase):
    def test_find_msg_suc(self):
        msgs = '''{"msg_id":"1","content":"sdfsdfa"},{"msg_id":"2","content":"sdfsd555fa"},{"msg_id":"3","content":"sdfsdfa"}'''
        msg_id = "sdfsd555fa"
        msg = find_msg(msgs, msg_id)
        msg = json.loads(msg)

        self.assertEquals(int(msg["msg_id"]), 2)  # add assertion here

    def test_find_msg_err(self):
        msgs = '''{"msg_id":"1","content":"sdfsdfa"},{"msg_id":"2","content":"sdfsd555fa"},{"msg_id":"3","content":"sdfsdfa"}'''
        msg_id = "sdfsd59955fa"
        msg = find_msg(msgs, msg_id)

        self.assertIsNone(msg)  # add assertion here

    def test_pop_user_suc(self):
        unreads = 'sdhfsfsaf,jlsidjfsidfj,sewerwe,werwerwe,'
        unreads = pop_user(unreads,'sewerwe')
        self.assertEqual(unreads, 'sdhfsfsaf,jlsidjfsidfj,werwerwe,')

    def test_pop_user_err(self):
        unreads = 'sdhfsfsaf,jlsidjfsidfj,sewerwe,werwerwe,'
        unreads = pop_user(unreads,'sewer55we')
        self.assertIsNone(unreads)


if __name__ == '__main__':
    unittest.main()
