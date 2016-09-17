# -*- coding: utf-8 -*-
import requests

__author__ = 'glow'

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
    pass


def get_fhir_subjects(endpoint="http://fhir.careevolution.com/apitest/fhir/Patient"):
    client = requests.Session()
    client.headers = {'Accept': 'application/json+fhir'}
    t = client.get('http://fhir.careevolution.com/apitest/fhir/Patient')
    return []

