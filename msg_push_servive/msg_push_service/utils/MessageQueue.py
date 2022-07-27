#python
#encoding = utf8
'''file:MessageQueue.py
include:
base class: MessageQueueBse;
derived classes: Local Message Queue  contain queue
derived classes: remote Message Queue  contain kafka
'''
from queue import Queue
from msg_push_service.utils.Logger import logger

class MessageQueueBase():
    '''base class: MessageQueueBse;'''
    def config_queue(self, maxsize=0):
        pass

    def put(self,data):
        pass

    def get(self):
        pass

class MQLocal(MessageQueueBase):
    '''derived classes: Local Message Queue  contain queue'''

    def __init__(self, maxsize = 0):
        self.msg_queue = Queue(maxsize)

    def put(self, item, block=True, timeout=None):
        '''Put an item into the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until a free slot is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Full exception if no free slot was available within that time.
        Otherwise ('block' is false), put an item on the queue if a free slot
        is immediately available, else raise the Full exception ('timeout'
        is ignored in that case).
        '''
        try:
            self.msg_queue.put(item, block=True, timeout=10)
        except Exception as err:
            logger.debug("put to queue faild.{}".format(err.with_traceback()))
            raise err

    def get(self,block=True, timeout=None):
        '''Remove and return an item from the queue.

                If optional args 'block' is true and 'timeout' is None (the default),
                block if necessary until an item is available. If 'timeout' is
                a non-negative number, it blocks at most 'timeout' seconds and raises
                the Empty exception if no item was available within that time.
                Otherwise ('block' is false), return an item if one is immediately
                available, else raise the Empty exception ('timeout' is ignored
                in that case).
        '''
        try:
            return self.msg_queue.get( block=False)
        except Exception as err:
            logger.debug("there are no request data, queue is empty.{}".format(err))
            return None

class MQRemote():
    '''base class: MessageQueueBse;'''
    def config_queue(self, maxsize=0):
        pass

    def put(self,data):
        pass

    def get(self):
        pass