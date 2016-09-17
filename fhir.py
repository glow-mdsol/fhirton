# -*- coding: utf-8 -*-
import os

import requests

__author__ = 'glow'

ENDPOINT = "http://fhir.careevolution.com/apitest/fhir/Patient"


def get_patient_medications(patient_id):
    """
    Get the Medications Resource from the FHIR endpoint
    :param patient_id:
    :return:
    """
    pass


def get_patient_demographics(patient_id):
    """
    Get the Patient resource from the FHIR endpoint
    :param patient_id:
    :return:
    """
    client = requests.Session()
    t = client.get('http://fhir.careevolution.com/apitest/fhir/Patient')
    patient_resource = os.path.join(ENDPOINT, patient_id)
    pass


def get_fhir_subjects(endpoint="http://fhir.careevolution.com/apitest/fhir/Patient"):
    client = requests.Session()
    client.headers = {'Accept': 'application/json+fhir'}
    t = client.get('http://fhir.careevolution.com/apitest/fhir/Patient')
    if not t.status_code == 200 :
        print("Error found retrieving subjects")
        subjects = []
    else :
        subjects = t.json().get("entry")
    return subjects

