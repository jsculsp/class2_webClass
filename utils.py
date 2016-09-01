import time


def log(*args, **kwargs):
    """
    用这个 log 替代 print
    """
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)