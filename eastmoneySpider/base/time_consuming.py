#!python
#encoding = utf8
import time
from functools import wraps, update_wrapper
from base.Logger import logger

class time_consuming:
    """装饰器：打印函数的耗时
    :param print_args:是否打印发发那个发名和参数，默认为False
    """
    def __init__(self, func):
        update_wrapper(self, func)  # 作用和wraps一样
        self.func = func

    def __call__(self, *args, **kwargs):
        st = time.perf_counter()
        ret = self.func(*args, **kwargs)
        logger.debug("time cost:{} seconds".format(time.perf_counter()-st))
        return ret