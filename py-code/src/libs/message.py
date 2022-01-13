from queue import Queue

class MsgQueue(Queue):
    """
    A MsgQueue is a queue used during test process, to send different levels 
    of messages. You can define specified process method for these messages.
    A MsgQueue is registered on a TestSuite object.
    """
    def __init__(self, *args, **kwargs):
        super(MsgQueue, self).__init__(*args, **kwargs)

    def _putMsg(self, msg, msgLevel:str, msgType:str, block=True, timeout=None, **kwargs):
        """
        kwargs: additional keyword arguments will be directly updated to msgPack put to the MsgQueue.
        """
        msgPack = {
            'msgType': msgType,
            'msgLevel': msgLevel,
            'msg': msg
        }
        msgPack.update(kwargs)  # additional kwargs could be attached to msgPack
        self.put(msgPack, block=block, timeout=timeout)

    # - msgLevel base methods -
    def debug(self, msg, msgType='debug', block=True, timeout=None, **kwargs):
        self._putMsg(msg, msgLevel='debug', msgType=msgType, block=block, timeout=timeout, **kwargs)

    def info(self, msg, msgType='info', block=True, timeout=None, **kwargs):
        self._putMsg(msg, msgLevel='info', msgType=msgType, block=block, timeout=timeout, **kwargs)

    def warn(self, msg, msgType='warn', block=True, timeout=None, **kwargs):
        self._putMsg(msg, msgLevel='warn', msgType=msgType, block=block, timeout=timeout, **kwargs)

    def error(self, msg, msgType='error', block=True, timeout=None, **kwargs):
        self._putMsg(msg, msgLevel='error', msgType=msgType, block=block, timeout=timeout, **kwargs)

    def fatal(self, msg, msgType='fatal', block=True, timeout=None, **kwargs):
        self._putMsg(msg, msgLevel='fatal', msgType=msgType, block=block, timeout=timeout, **kwargs)

    # - extended msg methods -
    def progress(self, msg, block=True, timeout=None, **kwargs):
        """
        msgLevel = info. Updating progress, such as percentage, time delay or others.
        """
        self.info(msg, msgType='progress', block=block, timeout=timeout, **kwargs)

    def plot(self, title, data, block=True, timeout=None, **kwargs):
        self.info(title, msgType='plot', block=True, timeout=None, data=data, **kwargs)
