# -*- coding: utf-8 -*-
import csv
import os
from collections import namedtuple

__author__ = 'glow'

# Configuration Variables for a Rave integration
RAVE_USER = os.environ.get('RAVE_USERNAME', '')
RAVE_PASSWORD = os.environ.get('RAVE_PASSWORD', '')
RAVE_URL = os.getenv('RAVE_URL', 'innovate')
RAVE_PROJECT = os.environ.get('RAVE_PROJECT', 'EHRTOEDC(DEV)')
STUDY = os.environ.get('STUDY', 'EHRTOEDC')
ENV = os.environ.get('ENV', 'DEV')

# Arbitrary Endpoint for Content
ENDPOINT = "http://fhir3.healthintersections.com.au/open/"

Server = namedtuple('Server', ['url', 'secured','notes'])

# NOTE: These may not all work, need to update as and when necessary
_servers = """http://fhir3.healthintersections.com.au/open/,no,
http://wildfhir.aegis.net/fhir1-8-0,no,
https://api3.hspconsortium.org/fhirconnect14/open,no,
https://fhirsandbox1.tsysinteropsvcs.net:8100/sites/123,no,
https://api3.hspconsortium.org/fhirconnect14/open,no,
https://fhir-open.stagingcernerpowerchart.com/stu3/a758f80e-aa74-4118-80aa-98cc75846c76/,no,STU 3 1.8.0
https://fhir-open.sandboxcerner.com/dstu2/d075cf8b-3261-481d-97e5-ba6c48d3b41f/,no,DSTU 2
https://open-ic.epic.com/Argonaut/api/FHIR/Argonaut/,yes,
https://open-ic.epic.com/FHIR/api/FHIR/DSTU2/,no,
http://fhirtest.uhn.ca,no,
https://tw171.open.allscripts.com/FHIR,yes,
https://tw171.open.allscripts.com/FHIRAnon,no,
http://twdev.open.allscripts.com/FHIR,yes,
http://twdev.open.allscripts.com/FHIRAnon,no,
https://vonk.furore.com/,no,
https://ipsdemo.accentureanalytics.com/fhir/v1.0.0,no,
http://fhir.ext.apelon.com:7080/dtsserverws/fhir,no,
http://sqlonfhir-stu3.azurewebsites.net/fhir,no,
http://fhir-2.transcendinsights.com/hl/alpine/fhir,no,
http://10.199.129.11:7080/CentricityPracticeFHIRServer/fhir/,no,
http://demo.oridashi.com.au:8290,no,DSTU2 - open; read-only; see metadata for scope; Best Practice Clinical System
http://demo.oridashi.com.au:8291,no,DSTU2 - open; read-only; see metadata for scope; Medical Director Clinical System
http://demo.oridashi.com.au:8297,no,STU3 (1.8.0) - open; read-only; see metadata for scope; Best Practice Clinical System
http://demo.oridashi.com.au:8298,no,STU3 (1.8.0) - open; read-only; see metadata for scope; Medical Director Clinical System
"""

SERVERS = []

for server in map(Server._make, csv.reader([x for x in _servers.split("\n") if x])):
    SERVERS.append(server)

Domain = namedtuple('Domain', ["name", "description", "prefix", "mapped"])

_domains = """COMMON,Common,COMMON,no
CO,Comments,CO,no
DM,Demographics,DM,yes
DA-Denormalized,Drug Accountability (Denormalized),DA,no
EG-Central Processing,"Scenario 3: Central Processing with Clinical Significance Assessment - Central processing, but the CRF includes site assessment of clinical significance and/or overall interpretation.",EG,no
EG-Central Reading,Scenario 1: Central Reading ECG  - Central Reading ECG results are captured directly by an electronic device and transmitted separately or read centrally - not recorded on the CRF.,EG,no
EG-Local Reading,Scenario 2: Local Reading ECG - Local Reading ECGs are performed and analyzed and results are recorded directly on the CRF,EG,no
SE,Subject Elements,SE,no
LB-Central Processing,"Scenario 1: Central Processing - Central Processing Where specimens are taken at site, but sent out and results are provided separately or where results are captured directly by an electronic device and transmitted separately - not recorded on the CRF.",LB,no
LB-Central Processing with CS,Scenarion 3: Central Processing with Clinical Significance Assessment - Central processing but CRF includes site assessment of clinical significance.,LB,no
LB-Local Processing,Scenario 2: Local Processing  - Local processing is when results of specimen analysis are recorded directly on the CRF.,LB,no
PE-Best Practice,Best Practice Approach (Option A),PE,no
PE-Traditional,Traditional Approach (Options B/C),PE,no
SV,Subject Visits,SV,no
AE,Adverse Event,AE,no
CE,Clinical Events,CE,no
DS,Disposition,DS,no
DV,Protocol Deviations,DV,no
HO,Healthcare Encounters,HO,no
MH,Medical History,MH,yes
CM,Prior and Concomitant Medications,CM,yes
PR,Procedures,PR,no
EX,Exposure,EX,no
EC,Exposure as Collected,EC,no
SU,Substance Use,SU,no
TA,Trial Arms,TA,no
TE,Trial Elements,TE,no
TV,Trial Visits,TV,no
TD,Trial Disease Assessments,TD,no
TI,Trial Inclusion/Exclusion Criteria,TI,no
TS,Trial Summary Information,TS,no
TX,Trial Sets,TX,no
SUPPQUAL,Supplemental Qualifiers [DOMAIN NAME],SUPPQUAL,no
RELREC,Related Records,RELREC,no
POOLDEF,Pool Definition Dataset,POOLDEF,no
RELSUB,Related Subjects,RELSUB,no
APDM,Associated Persons Demographics,APDM,no
FA,Findings About,FA,no
SR,Skin Response,SR,no
DA,Drug Accountability,DA,no
DD,Death Details,DD,no
EG,ECG Test Results,EG,no
IE,Inclusion and Exclusion Criteria,IE,no
IS,The Immunogenicity Specimen Assessments,IS,no
LB,Laboratory Test Results,LB,yes
MB,Microbiology Specimen,MB,no
MS,Microbiology Susceptibility,MS,no
MI,Microscopic Findings,MI,no
MO,Morphology,MO,no
PC,Pharmacokinetics Concentrations,PC,no
PP,Pharmacokinetics Parameters,PP,no
PE,Physical Exam,PE,no
QS,Questionnaires,QS,no
RP,Reproductive System Findings,RP,no
SC,Subject Characteristics,SC,no
SS,Subject Status,SS,no
TU,The Tumor Identification,TU,no
TR,The Tumor Response,TR,no
RS,The Disease Response,RS,no
VS,Vital Signs,VS,yes
"""

DOMAINS = []

for domain in map(Domain._make, csv.reader([x for x in _domains.split("\n") if x])):
    DOMAINS.append(domain)
