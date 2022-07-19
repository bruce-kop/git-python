import unittest
from libs import ImageConvert

class MyTestCase(unittest.TestCase):
    def test_image_to_base64_err(self):
        ret = ImageConvert.image_to_base64("FDSF",'UTF8')
        self.assertIsNone(ret)


if __name__ == '__main__':
    unittest.main()
