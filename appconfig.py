# -*- coding: utf-8 -*-
import os

__author__ = 'glow'

RAVE_USER = os.environ.get('RAVE_USERNAME', 'shume')
RAVE_PASSWORD = os.environ.get('RAVE_PASSWORD', 'Merry1179')
RAVE_URL = os.getenv('RAVE_URL', 'innovate')
RAVE_PROJECT = os.environ.get('RAVE_PROJECT', 'EHRTOEDC(DEV)')
STUDY = os.environ.get('STUDY', 'EHRTOEDC')
ENV = os.environ.get('ENV', 'DEV')
