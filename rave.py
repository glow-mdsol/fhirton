# -*- coding: utf-8 -*-
import datetime
from rwslib import RWSConnection
from rwslib.rws_requests import StudySubjectsRequest, PostDataRequest
import uuid

import appconfig
from ehr_to_rave_odm import make_odm, audit_id

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
'event': ['2014-02-13T00:00:00-05:00']}}],
'meta': {'lastUpdated': '2016-05-23T23:19:35.163+00:00'},
'patient': {'reference': 'Patient/968d3477-3c21-e611-8128-0a69c1b3225b'}, 'status': 'completed',
'effectivePeriod': {'start': '2014-02-13T00:00:00-05:00', 'end': '2014-08-10T00:00:00-04:00'}}}
"""

"""
     <ItemGroupDef OID="CM" Name="CM" Repeating="No">
        <ItemRef ItemOID="CM.CMSTAT" OrderNumber="196" Mandatory="Yes" />
        <ItemRef ItemOID="CM.HIDDEN_NOW" OrderNumber="197" Mandatory="No" />
        <ItemRef ItemOID="CM.CMREASND" OrderNumber="198" Mandatory="No" />
      </ItemGroupDef>
      <ItemGroupDef OID="CM_LOG_LINE" Name="CM_LOG_LINE" Repeating="Yes">
        <ItemRef ItemOID="CM.CMTRT" OrderNumber="199" Mandatory="No" />
        <ItemRef ItemOID="CM.CMDOSTOT" OrderNumber="200" Mandatory="No" />
        <ItemRef ItemOID="CM.CMDOSU" OrderNumber="201" Mandatory="No" />
        <ItemRef ItemOID="CM.CMDOSFRM" OrderNumber="202" Mandatory="No" />
        <ItemRef ItemOID="CM.CMDOSFRQ" OrderNumber="203" Mandatory="No" />
        <ItemRef ItemOID="CM.CMROUTE" OrderNumber="204" Mandatory="No" />
        <ItemRef ItemOID="CM.CMDOSRGM" OrderNumber="205" Mandatory="No" />
        <ItemRef ItemOID="CM.CMSTDTC" OrderNumber="206" Mandatory="No" />
        <ItemRef ItemOID="CM.CMONG" OrderNumber="207" Mandatory="No" />
        <ItemRef ItemOID="CM.CMENDTC" OrderNumber="208" Mandatory="No" />
        <ItemRef ItemOID="CM.CMDUR" OrderNumber="209" Mandatory="No" />
        <ItemRef ItemOID="CM.CMINDC" OrderNumber="210" Mandatory="No" />
      </ItemGroupDef>

"""


def push_conmeds(subject_id, conmeds):
    """
    Insert a Concomitant Medication Record
    :param subject_id: UUID for subject
    :param conmeds: list of conmeds
    """
    locationoid, subject_uuid = subject_id.split('_')

    client = RWSConnection(domain=appconfig.RAVE_URL,
                           username=appconfig.RAVE_USER,
                           password=appconfig.RAVE_PASSWORD)
    for medrx in conmeds[:5]:
        #print(medrx)
        mapping = []
        resource = medrx.get('resource')
        # Log context
        ctxt = resource.get('id')
        print(ctxt)
        mapping.append(dict(folder_oid="SUBJECT",
                            form_oid="CM",
                            field_oid="CM.CMINDC",
                            value=ctxt,
                            cdash_domain="CM",
                            log_context_field="CM.CMINDC",
                            log_context_value=ctxt, is_new=True))
        period = resource.get('effectivePeriod')
        if period:
            if period.get('start'):
                mapping.append(dict(folder_oid="SUBJECT",
                                    form_oid="CM", field_oid="CM.CMSTDTC",
                                    value=munge_to_rave_date(period.get('start').split('T')[0]), cdash_domain="CM",
                                    log_context_field="CM.CMINDC", log_context_value=ctxt))
            if period.get('end'):
                mapping.append(dict(folder_oid="SUBJECT",
                                    form_oid="CM", field_oid="CM.CMENDTC",
                                    value=munge_to_rave_date(period.get('end').split('T')[0]), cdash_domain="CM",
                                    log_context_field="CM.CMINDC", log_context_value=ctxt))
        # truncate the text, should look into how we get a proper name
        if resource.get('dosage'):
            dosage = resource.get('dosage')[0]
            cmtrt = dosage.get('text')[:198]
            mapping.append(dict(folder_oid="SUBJECT",
                                form_oid="CM", field_oid="CM.CMTRT",
                                value=cmtrt, cdash_domain="CM",
                                log_context_field="CM.CMINDC",
                                log_context_value=ctxt))
            if dosage.get('route'):
                mapping.append(dict(folder_oid="SUBJECT",
                                    form_oid="CM", field_oid="CM.CMROUTE",
                                    value=dosage.get('route').get('text'),
                                    cdash_domain="CM",
                                    log_context_field="CM.CMINDC", log_context_value=ctxt))
        odm = make_odm(appconfig.STUDY, appconfig.ENV, locationoid, subject_uuid, mapping,
                       retrieved_datetime=datetime.datetime.now(), transfer_user='glow',
                       transfer_identifier=audit_id(), freeze=False)
        print(odm)
        request = PostDataRequest(str(odm))
        response = client.send_request(request)


"""
{'identifier': [{'system': 'http://fhir.carevolution.com/identifiers/CareEvolution/MRN/Lourdes-Camden-Invision-Patient',
'value': 'AZVe0IYogrjXt19aIXR1LQ==', 'use': 'usual'}, {'system': 'http://fhir.carevolution.com/identifiers/CareEvolution/MRN',
'value': 'AZVe0I'}, {'system': 'http://hl7.org/fhir/sid/us-ssn', 'value': '211928575'}],
'communication': [{'preferred': True,
'language': {'coding': [{'userSelected': True, 'code': 'ENG',
'system': 'http://fhir.carevolution.com/codes/Lourdes-Camden-Invision-NS/PreferredLanguage', 'display': 'ENG'}], 'text': 'ENG'}}],
'id': 'd38eed79-3b21-e611-8128-0a69c1b3225b',
'resourceType': 'Patient',
'link': [
{'other': {'reference': 'Patient/968d3477-3c21-e611-8128-0a69c1b3225b'}, 'type': 'seealso'},
{'other': {'reference': 'Patient/e20a11ee-3b21-e611-8128-0a69c1b3225b'}, 'type': 'seealso'},
{'other': {'reference': 'Patient/4237d016-3e21-e611-8128-0a69c1b3225b'}, 'type': 'seealso'},
{'other': {'reference': 'Patient/b68c958e-3d21-e611-8128-0a69c1b3225b'}, 'type': 'seealso'}],
'meta': {'lastUpdated': '2016-05-23T23:10:07.547+00:00'},
'extension': [
{'url': 'http://hl7.org/fhir/StructureDefinition/us-core-ethnicity',
    'valueCodeableConcept': {'coding': [
        {'userSelected': True,
            'code': '0',
            'system': 'http://fhir.carevolution.com/codes/Lourdes-Camden-Invision-NS/Ethnicity'}]}},
{'url': 'http://hl7.org/fhir/StructureDefinition/us-core-race',
    'valueCodeableConcept': {'coding': [{'userSelected': True, 'code': 'W',
    'system': 'http://fhir.carevolution.com/codes/Lourdes-Camden-Invision-NS/Race', 'display': 'W'},
    {'userSelected': False, 'code': 'C', 'system': 'http://fhir.carevolution.com/codes/CareEvolution/Race',
    'display': 'Caucasian'}], 'text': 'W'}}
    ],
'deceasedBoolean': False,
'name': [{'given': ['SHAWN', 'L'], 'family': ['GUIDOTTI'], 'use': 'official'}],
'birthDate': '1942-01-01',
'gender': 'female'}
"""

"""
      <ItemGroupDef OID="DM" Name="DM" Repeating="No">
        <ItemRef ItemOID="DM.BRTHDTC" OrderNumber="189" Mandatory="Yes" />
        <ItemRef ItemOID="DM.AGE" OrderNumber="190" Mandatory="No" />
        <ItemRef ItemOID="DM.SEX" OrderNumber="191" Mandatory="Yes" />
        <ItemRef ItemOID="DM.CHILDBEAR" OrderNumber="192" Mandatory="No" />
        <ItemRef ItemOID="DM.RACE" OrderNumber="193" Mandatory="Yes" />
        <ItemRef ItemOID="DM.COUNTRY" OrderNumber="194" Mandatory="No" />
        <ItemRef ItemOID="DM.DSSTDT" OrderNumber="195" Mandatory="Yes" />
      </ItemGroupDef>
"""

def munge_to_rave_date(datestr):
    dt = datetime.datetime.strptime(datestr, '%Y-%m-%d')
    return dt.strftime('%d %b %Y')

def push_demographics(subject_id, patient_json):
    """
    Insert Patient Demography Data
    :param subject_uuid: UUID for subject
    :param patient_json: returned Patient JSON
    :return:
    """
    locationoid, subject_uuid = subject_id.split('_')
    mapping = []
    date_of_birth = patient_json.get('birthDate')
    if date_of_birth:
        mapping.append(dict(folder_oid="SCREEN", form_oid="DM", field_oid="DM.BRTHDTC",
                            value=munge_to_rave_date(date_of_birth), cdash_domain="DM",
           cdash_element="BRTHDTC"))
    gender = patient_json.get('gender')
    if gender:
        if gender.lower() in ['male', 'female']:
            mapping.append(dict(folder_oid="SCREEN", form_oid="DM", field_oid="DM.SEX",
                                value=gender.upper(), cdash_domain="DM", cdash_element="SEX"))
    if mapping:
        odm = make_odm(appconfig.STUDY, appconfig.ENV, locationoid, subject_uuid, mapping,
                       retrieved_datetime=datetime.datetime.now(), transfer_user='glow',
                       transfer_identifier=audit_id(), freeze=False)
        request = PostDataRequest(str(odm))
        client = RWSConnection(domain=appconfig.RAVE_URL,
                               username=appconfig.RAVE_USER,
                               password=appconfig.RAVE_PASSWORD)
        response = client.send_request(request)
        return response
