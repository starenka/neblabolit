#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings.base import *

try:
    from settings.local import *
except ImportError:
    pass

DB = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=DB_USER,
                                                           pw=DB_PASSWORD,
                                                           url=DB_HOST,
                                                           db=DB_NAME)
