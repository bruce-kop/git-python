#python
#encoding = utf8
from io import BytesIO
import base64
from PIL import Image
import re
from userservice.utils.Logger import logger

def image_to_base64(image: Image.Image, fmt='png') -> str:
    try:
        output_buffer = BytesIO()
        image.save(output_buffer, format=fmt)
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data).decode('utf-8')
    except Exception as e:
        logger.debug(e)
        return None
    return 'data:image/{};base64,'.format(fmt) + base64_str

def base64_to_image(base64_str: str) -> Image.Image:
    try:
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
    except Exception as e:
        logger.debug(e)
        return None
    return img