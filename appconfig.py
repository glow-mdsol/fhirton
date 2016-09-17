# -*- coding: utf-8 -*-
import os

__author__ = 'glow'

USERNAME = os.environ['RAVE_USERNAME']
PASSWORD = os.environ['RAVE_PASSWORD']
RAVE_URL = os.getenv('RAVE_URL', 'innovate')
RAVE_PROJECT = os.environ['RAVE_PROJECT']