# -*- coding: utf-8 -*-
import os
import urllib


import requests
from fhirclient import client
import fhirclient.models.patient as p
import fhirclient.models.medicationstatement as cm
import fhirclient.models.observation as ob


__author__ = 'glow'


class FHIRConnection(object):

    def __init__(self, base_url="https://fhir-open-api-dstu2.smarthealthit.org"):
        smart = client.FHIRClient(settings=dict(api_base=base_url, app_id='my_client'))

    @property
    def patients(self):
        search = p.Patient.where(struct=dict())
        pt_list = []
        for patient in search.perform_resources(smart.server):
            pt_list.append(patient.as_json())
        return pt_list

    def get_patient(self, patient_id):
        patient = p.Patient.read(patient_id, smart.server)
        return patient.as_json()

    def get_patient_medications(self, patient_id):
        # ??? need the right patient id
        search_meds = cm.MedicationStatement.where(struct=dict(patient=patient_id))
        meds = []
        for meds in search_meds.perform_resources(smart.server):
           meds.append(meds.as_json())
        return meds

    def get_medication(self, medication_id):
        medication = cm.MedicationStatement.read(medication_id, smart.server)
        return medication.as_json();

    def get_obs(self, patient_id, loinc_code):
        search_obs = ob.Observation.where(struct=dict(patient=patient_id, code=loinc_code))
        obs = ""
        if len(search_obs.perform_resources(smart.server)) > 0:
            sysbp = search_obs.perform_resources(smart.server).pop().as_json()
        return obs

    def get_vitals_sysbp(self, patient_id):
        return self.get_obs(patient_id, "8480-6")

    def get_vitals_diabp(self, patient_id):
        return self.get_obs(patient_id, "55284-4")

    def get_vitals_bmi(self, patient_id):
        return self.get_obs(patient_id, "39156-5")

    def get_vitals_hr(self, patient_id):
        return self.get_obs(patient_id, "8867-4")

    def get_vitals_temp(self, patient_id):
        return self.get_obs(patient_id, "8310-5")

    def get_vitals_weight(self, patient_id):
        return self.get_obs(patient_id, "3141-9")

    def get_vitals_height(self, patient_id):
        return self.get_obs(patient_id, "8302-2")

    def get_labs_wbc(self, patient_id):
        return self.get_obs(patient_id, "6690-2")

    def get_labs_rbc(self, patient_id):
        return self.get_obs(patient_id, "789-8")

    def get_labs_creat(self, patient_id):
        return self.get_obs(patient_id, "14682-9")

    def labs_alb(self, patient_id):
        return self.get_obs(patient_id, "1751-7")

