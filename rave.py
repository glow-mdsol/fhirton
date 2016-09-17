# -*- coding: utf-8 -*-
from rwslib import RWSConnection
from rwslib.rws_requests import StudySubjectsRequest

import appconfig

__author__ = 'glow'


def get_rave_subjects():
    client = RWSConnection(domain=appconfig.RAVE_URL,
                           username=appconfig.RAVE_USER,
                           password=appconfig.RAVE_PASSWORD)
    subjects = client.send_request(StudySubjectsRequest(appconfig.STUDY,
                                                        appconfig.ENV,
                                                        subject_key_type='SubjectUUID'))
    return subjects
