# -*- coding: utf-8 -*-
from rwslib import RWSConnection

import appconfig

__author__ = 'glow'


def get_rave_subjects():
    client = RWSConnection(username=appconfig.RAVE_USER,
                           password=appconfig.RAVE_PASSWORD)
    return []

