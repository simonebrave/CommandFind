#!/bin/python3.6
import datetime
from functools import wraps


class TimeIt:
    def __init__(self, fn):
        self._fn = fn
        wraps(fn)(self)

    def __call__(self, *args, **kwargs):
        start = datetime.datetime.now()
        ret = self._fn(*args, **kwargs)
        delta = (datetime.datetime.now() - start).total_seconds()
        print('time cost:', delta)
        return ret

# 这个装饰器没有毛病