# -*- coding: utf-8 -*-
import os

__author__ = 'glow'

RAVE_USER = os.environ.get('RAVE_USERNAME', 'glow123')
RAVE_PASSWORD = os.environ.get('RAVE_PASSWORD', '')
RAVE_URL = os.getenv('RAVE_URL', 'innovate')
RAVE_PROJECT = os.environ.get('RAVE_PROJECT', 'EHRTOEDC(DEV)')
STUDY = os.environ.get('STUDY', 'EHRTOEDC')
ENV = os.environ.get('ENV', 'DEV')
