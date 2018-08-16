#!/usr/local/bin/python
# -*- coding: utf-8 -*-


import time
import uuid
import functools
import threading
import logging


# global engine object:
engine = None

def next_id(t=None):
    if t is None:
        t=time.time()
    return '%015d%s000' % (int(t*1000),uuid.uuid4().hex)


def _profiling(start,sql=''):
    t=time.time()-start
    if t>0.1:
        logging.warning('[PROFILING] [DB] %s: %s' % (t,sql));
    else:
        logging.info('[PROFILING] [DB] %s:%s' % (t,sql))
