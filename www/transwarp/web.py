#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/9 下午9:23
# @Author  : mingming.wan
# @File    : web.py
# @Software: PyCharm


import types, os, re, cgi, sys, time, datetime, functools, mimetypes, threading, logging, traceback, urllib

from db import Dict


import utils

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


ctx = threading.local()

_RE_RESPONSE_STATUS = re.compile(r'^\d\d\d(\ [\w\ ]+)?$')
_HEADER_X_POWERED_BY = ('X-Powered-By', 'transwarp/1.0')


_TIMEDELTA_ZERO = datetime.timedelta(0)

_RE_TZ = re.compile(r'^([\+\-])([0-9]{1,2})\:([0-9]{1,2})$')

_RESPONSE_STATUSE = {
    100: 'Continue',
    101: 'Switching Protocols',
    102: 'Processing',

    200: 'Ok',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',
    207: 'Multi Status',
    226: 'IM Used',

    300: 'Muliple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    307: 'Temporary Redirect',

    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Confict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Request Entity Too Large',
    414: 'Request URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Requested Range Not Satisfiable',
    417: 'Expection Failed',
    418: "I'm a teapot",
    422: 'Unprocessable Entity',
    423: 'Locked',
    424: 'Failed Dependency',
    426: 'Upgrade Required',

    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported',
    507: 'insufficient Storage',
    510: 'Not Extended'
}

_RESPONSE_HEADERS = (
    'Accept-Ranges',
    'Age',
    'Allow',
    'Cache-Control',
    'Connection',
    'Content-Encoding',
    'Content-Language',
    'Content-Length',
    'Content-Location',
    'Content-MD5',
    'Content-Disposition',
    'Content-Range',
    'Content-Type',
    'Date',
    'ETag',
    'Expires',
    'Last-Modified',
    'Link',
    'Location',
    'P3P',
    'Pragma',
    'Proxy-Authenticate',
    'Refresh',
    'Server',
    'Set-Cookie',
    'Strict-Transport-Security',
    'Trailer',
    'Transfer-Encoding',
    'Vary',
    'Via',
    'Warning',
    'WWW-Authenticate',
    'X-Frame-Options',
    'X-Content-Type-Options',
    'X-Forwarded-Proto',
    'X-Powered-By',
    'X-UA-Compatible'
)


class UTC(datetime.tzinfo):

    def __init__(self, utc):
        utc = str(utc.strip().upper())
        mt = _RE_TZ.match(utc)
        if mt:
            minus = mt.group(1) == '-'
            h = int(mt.group(2))
            m = int(mt.group(3))
            if minus:
                h, m = (-h), (-m)
            self._utcoffset = datetime.timedelta(hours=h, minutes=m)
            self._tzname = 'UTC%s' % utc
        else:
            raise ValueError('bad utc time zone')

    def utcoffset(self, dt):
        return self._utcoffset

    def dst(self, dt):
        return _TIMEDELTA_ZERO

    def tzname(self, dt):
        return self._tzname

    def __str__(self):
        return 'UTC timezone info object (%s)' % self._tzname

    __repr__ = __str__


UTC_0 = UTC('+00:00')


class _HttpError(Exception):

    def __init__(self, code):
        super(_HttpError, self).__init__()
        self.status = '%d %s' % (code, _RESPONSE_STATUSE[code])
        self._headers = None

    def header(self, name, value):
        if not self._headers:
            self._headers = [_HEADER_X_POWERED_BY]
        self._headers.append((name, value))

    @property
    def headers(self):
        if hasattr(self, '_headers'):
            return self._headers
        return []

    def __str__(self):
        return self.status
    __repr__ = __str__


class _RedirectError(_HttpError):

    def __init__(self, code, location):
        super(_RedirectError, self).__init__(code)
        self.location = location

    def __str__(self):
        return '%s, %s' % (self.status, self.location)

    __repr__ = __str__


class HttpError(object):

    @staticmethod
    def badrequest():
        return _HttpError(400)


    @staticmethod
    def unauthorized():
        return _HttpError(401)

    @staticmethod
    def forbidden():
        return _HttpError(403)

    @staticmethod
    def notfound():
        return _HttpError(404)

    @staticmethod
    def conflict():
        return _HttpError(409)

    @staticmethod
    def internalerror():
        return _HttpError(500)

    @staticmethod
    def redirect(location):
        return _RedirectError(301, location)

    @staticmethod
    def found(location):
        return _RedirectError(302, location)

    @staticmethod
    def seeother(location):
        return _RedirectError(303, location)


_RESPONSE_HEADER_DICT = dict(zip(map(lambda x: x.upper(), _RESPONSE_HEADERS), _RESPONSE_HEADERS))





if __name__ == '__main__':



    print(UTC_0)



