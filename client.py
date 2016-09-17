# -*- coding: utf-8 -*-

__author__ = 'glow'

from fhirclient import client
settings = {
    'app_id': 'my_web_app',
    'api_base': 'http://fhir.careevolution.com/apitest/fhir'
}
smart = client.FHIRClient(settings=settings)

import fhirclient.models.patient as p
import fhirclient.models.observation as o

patient = p.Patient.read('hca-pat-1', smart.server)
print(patient.birthDate.isostring)
# '1963-06-12'
print(smart.human_name(patient.name[0]))
# 'Christy Ebert'

search = o.Observation.where(struct={'subject': 'hca-pat-7'})
vitals = search.perform_resources(smart.server)
for vital in vitals:
    print(vital.code.text,"->" ,vital.status)
