# -*- coding: utf-8 -*-

__author__ = 'glow'

import requests
import json

server = "http://fhir.careevolution.com/apitest/fhir"

client = requests.Session()

response = client.get(server + "/Patient?_id=23&_format=application/json+fhir")
print(response)
print(response.json())
