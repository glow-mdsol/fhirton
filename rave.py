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

"""
{'search': {'mode': 'match'},
'fullUrl': 'http://fhir.careevolution.com/apitest/fhir/MedicationStatement/f3fb1ace-3c21-e611-8128-0a69c1b3225b',
'resource': {'identifier': [{'type': {'coding': [{'code': 'PLAC', 'system': 'http://hl7.org/fhir/identifier-type'}]},
'system': 'http://fhir.carevolution.com/identifiers/CareEvolution/MRN/NextGenPRA',
'value': 'd1772668-80c1-4694-8923-347a75773968', 'use': 'usual'}],
'id': 'f3fb1ace-3c21-e611-8128-0a69c1b3225b', 'medicationReference': {'reference': 'Medication/194'},
'resourceType': 'MedicationStatement',
'dosage': [{'asNeededBoolean': False,
'text': 'Exelon 9.5 mg/24 hour Transderm 24 hr XXXXX apply 1 XXXXX (9.5MG)  by transdermal route  every day . Do not apply to same area more than once every 14 days.',
'timing': {'code': {'coding': [{'userSelected': True, 'code': 'N/A',
'system': 'http://fhir.carevolution.com/codes/NextGen/OrderFrequency', 'display': 'N/A'}], 'text': 'N/A'},
'event': ['2014-02-13T00:00:00-05:00']}}], 'meta': {'lastUpdated': '2016-05-23T23:19:35.163+00:00'},
'patient': {'reference': 'Patient/968d3477-3c21-e611-8128-0a69c1b3225b'}, 'status': 'completed',
'effectivePeriod': {'start': '2014-02-13T00:00:00-05:00', 'end': '2014-08-10T00:00:00-04:00'}}}
"""

def push_conmed(subject_uuid, conmed):
    """
    Insert a Concomitant Medication Record
    :param subject_uuid: UUID for subject
    :param conmed:
    """
    pass

"""
{'birthDate': '1974-12-25', 'deceasedBoolean': False,
'address': [{'line': ['534 ErewhonnqUIbOfdO St'], 'postalCode': '6271', 'state': 'Vic',
'city': 'PleasantVille', 'use': 'home'}],
'telecom': [{'value': '(03) 5555 6473', 'system': 'phone', 'use': 'work'}],
'meta': {'lastUpdated': '2016-06-16T11:25:47.47+00:00'},
'name': [{'family': ['ChalmersnYxaAplu'], 'use': 'official',
'given': ['PeternYxaAplu', 'JamesnYxaAplu']}, {'use': 'usual', 'given': ['Jim']}],
'id': '7a81ba0d-b533-e611-8128-0a69c1b3225b',
'identifier': [{'use': 'usual', 'system': 'urn:oid:1.2.36.146.595.217.0.1', 'value': 'srBFzLT0gmeWT5B2'}],
'resourceType': 'Patient', 'gender': 'male'}
"""

def push_demographics(subject_uuid, patient_json):
    """
    Insert Patient Demography Data
    :param subject_uuid: UUID for subject
    :param patient_json: returned Patient JSON
    :return:
    """

