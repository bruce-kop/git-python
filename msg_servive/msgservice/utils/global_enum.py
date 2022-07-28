#python
#encoding = utf8

''' file:global_enum.py
    class: GlobalEnum. defines all enum for the service
'''

from enum import Enum, unique
@unique
class GlobalEnum(Enum):
    LOGIN_ERR_COUNT_LIMIT = 3

APIS = {
'/api/verifycode',
'/api/register',
'/api/login'
}
