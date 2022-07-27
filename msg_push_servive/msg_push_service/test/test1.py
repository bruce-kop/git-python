#encoding = utf8
from msg_push_service.utils.MessageQueue import MQLocal
from msg_push_service.utils.Logger import logger
if __name__ == '__main__':
    q = MQLocal(1024)
    l = [1,2,3,4]
    q.put('a')
    while True:
        for i in l:
            try:
                a = q.()
            except Exception as e:
                logger.info(e)
            logger.info(a)
            logger.info(i)

        logger.info(55)


