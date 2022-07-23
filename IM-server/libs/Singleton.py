#python
#encoding = utf8
'''file:Singleton.py
   author: bruce zhang
   Date: 2022-7-19
'''
def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kwagrs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwagrs)
        return _instance[cls]

    return _singleton