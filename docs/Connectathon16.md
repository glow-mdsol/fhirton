# Scenario 1 
## Examining EHR patient data for protocol feasibility and clinical trial recruitment for a specific clinical trial
* Scenario Lead: Lisa Morgan, TransCelerate
## Objective: 
Applications that will allow users to query clinical data (ideally both structured and narrative) from source systems, including EMR’s, to find suitable patients for clinical trials.
## Background: 
Currently, manual chart review of a patient’s medical record is typically required to identify patients who may be eligible to participate in clinical trials. However, this process is burdensome, expensive and time intensive, and the complexity of the eligibility criteria requires an appropriately skilled individual to review the information, so that clinical information is appropriately matched and interpreted. As well, that same information used to define the eligibility of the patient, must then be redundantly entered into downstream systems manually for data capture.
## Action: 
Clinical trial designer creates an application and user interface which allows the sites to search for specific characteristics based upon the protocol inclusion and exclusion criteria, and output a list of candidate patients and their information to downstream applications.
## Precondition: 
EHR data exists for a significant group of patients. The data must include Demographic information, clinical narrative and clinical data such as problems, medications and lab reports. At least 1 patient meeting all eligibility criteria exists in the EHR database (may be preassigned) a study and subject identifier. The following Eligibility Criteria are listed in the Protocol ABC5236:
1. Female Age: 18-70
1. Patients that are newly diagnosed with stage I, II or III unilateral Triple Negative Breast Cancer who have not undergone neoadjuvant chemotherapy or undergone definitive breast surgery.
1. ECOG performance status score of 0-1 (Karnofsky score can be substituted)
1. Have a Left Ventricular Ejection Fraction (LVEF) of ≥ 50% by echocardiogram or MUGA scan, and does not have a current or historical diagnosis of CHF, MI, TIA, PVD, or uncontrolled hypertension with a blood pressure of greater than 160/90
1.  Subject does not have metastatic disease (consider substituting a positive occurrence rather than an absence of a condition which is more difficult to query).
## Success Criteria: 
Returns counts, practitioner identifiers, patient identifiers. 
The application will present the research data user with: 
1. a count of patients that meet the criteria and 
1. a list of ranked patients that can be manually validated as eligible for clinical trials `ABC5236`. 
The information retrieved will allow a patient to be enrolled and randomized and allow sending of the relevant information on that patient downstream in a machine-readable format for consumption by appropriate application(s).
### Bonus point: 
Assign a ResearchStudy Identifier and ResearchSubject Identifier in EHR for enrolled subjects

# Scenario 2 
## Extract relevant EHR data for ResearchSubject and import into Study Database
* Scenario 2 Lead: Michelle Crouthamel , TransCelerate
## Objective: 
Advance the use of FHIR resources as eSource data used to pre-populate clinical research case report forms for both regulated and non-regulated clinical research.
## Background: 
Clinical Research studies currently require the redundant entry of clinical data that already typically resides in Meaningful Use conformant EHR systems. EHR data represents original records in electronic format that can be used as eSource to eliminate the need for redundant data entry in clinical research EDC databases.
## Action: 
Identify a Patient in an EHR who is enrolled in a ResearchStudy, extract relevant EHR data that can be mapped to a clinical research Electronic Data Capture (EDC) database, import into EDC Study Database to auto-populate eCRFs.
## Precondition: 
Patient records include demographics, MedicationStatement, Lab observation data, possibly problems, diagnosis. At least one patient has at least 2 sets of lab observations for at least 3 lab tests. Additional information, such as LOINC codes for the set of lab tests to be used and mappings to CDISC for these will be specified in advance.
The following Eligibility Criteria are listed in the sample Protocol #205718
1. Age
1. Gender
1. Diagnosis of Rhematoid Arthritis from past 12 months
1. Medications from past 12 months
1. HAQDI (Health assessment questionnaire disability index) score from past 12 months (or another patient reported outcome score such as SF-36)
1. lab test: At least one of the following lab tests with results: anti-CCP, erythrocyte sedimentation rate (ESR, or sed rate), C-reactive protein (CRP), Electrolytes from past 12 months
## Success Criteria: 
The App is able to import EHR data for at least one subject in each of 3 different EHRs (preferably including 1 Epic system, 1 Cerner system and 1 other system) and auto-populate eCRFs in an EDC database.
### Bonus point: 
Document the mapping of relevant CCDS content to CDISC standard data elements.
### Bonus point 2: 
identify and extract relevant unstructured data that may be relate to rheumatoid arthritis conditions.

# Scenario 3 
## Receive and apply Real World Evidence updates to the study database as new or changed data is recorded in the EHR or received from patients
## Objective: 
An App that could allow data to be collected from a patient in a Real World Evidence (RWE) Standard of Care (SoC) study, recording visits/encounters to, and reasons for visits/encounters to healthcare institutions and transfer this data back to a central investigator site in near real time so that follow up can be made while the study continues.
## Background: 
This track is intended to advance the use of FHIR resources and eSource data to collect specific patient data in as low-interventional manner as possible in order to support real world outcomes research. Healthcare Resource Utilization (HCRU) data are a critical component of RWE data packages used by companies to demonstrate to Healthcare Payers that a medicine can have a positive impact on their healthcare system.
Collecting this data can be challenging since a patient in a SoC setting may seek care from any number of healthcare institutions within their country. In order to track this data, it would be helpful if the patient could record in an App any such visits and even select reasons for visiting, to distinguish between a visit to a friend in a hospital and a visit to a hospital for their own welfare/care. Developing an App that would record such information and trigger a transfer of the data from the EHR to an investigator site (or an EDC system) in near real time so that the investigator can themselves interview the patient to get more details during a future scheduled clinical trial visit. Most RWE studies have few, or more likely no scheduled visits for patients. Alternatively, a patient may extract from or provide relevant information to an EHR using a SMART app that records healthcare institution visits with reasons for the visit and other useful data (such as questionnaires). Ideally data could be extracted directly from a target institution’s EHR and be transferred to a clinical study database.
## Action: 
Enter new data in EHR for a current ResearchSubject after new patient encounter is recorded in EHR. Or create an App which allows the recording of data by patient and remote site; integrate the captured data with the site EHR if possible and extract this data directly from remote EHR if possible. Output data to the sponsor in an agreed dataset format.
## Precondition: 
Patient is enrolled as a ResearchSubject for a ResearchStudy with available clinical data. Data that might be suitable for this scenario (for a sample HCRU study) may include duration of visit, procedures any diagnoses or treatments and questionnaires.
## Success Criteria: 
App can allow data entry by patient or collect data directly from and EHR and automatically integrate data back into the investigator EHR (or produce an integration preferred data file that could be imported into a separate research study database). Also can generate a near real time updated file for transfer back to the sponsor of this study specific data captured from remote sites.
Automation of data collection is ideal -- Upload of data directly from a remote site’s EHR is likely preferable than the more pragmatic manual data entry into the app.
### Bonus point : 
Use CDS Hooks to trigger update after new patient encounter is recorded.
