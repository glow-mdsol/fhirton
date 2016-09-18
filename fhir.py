# -*- coding: utf-8 -*-
import os
import urllib

import requests

__author__ = 'glow'

BASE_URL ="http://fhir.careevolution.com/apitest/fhir"


class FHIRConnection(object):

    def __init__(self, base_url):
        self.base_url = base_url
        self._client = requests.Session()
        self._client.headers = {'Accept': 'application/json+fhir'}

    @property
    def patients(self):
        patients = []
        response = self._client.get(os.path.join(self.base_url, 'Patient'))

        while True:
            patients.extend(response.json().get('entry'))
            links = dict([(x.get('relation'), x.get('url')) for x in response.json().get('link')])
            if 'next' in links:
                response = self._client.get(links.get('next'))
            else:
                break
        return patients

    def get_patient(self, patient_id):
        patient = self._client.get(os.path.join(self.base_url, 'Patient', patient_id))
        if patient.status_code == 404:
            print("No such patient")
            return None
        return patient

    def get_patient_medications(self, patient_id):
        medications = []
        params = urllib.parse.urlencode(dict(patient="Patient/{}".format(patient_id)))
        target = os.path.join(self.base_url, 'MedicationStatement?{}'.format(params))
        response = self._client.get(target)
        while True:
            medications.extend(response.json().get('entry'))
            links = dict([(x.get('relation'), x.get('url')) for x in response.json().get('link')])
            if 'next' in links:
                response = self._client.get(links.get('next'))
            else:
                break
        return medications

