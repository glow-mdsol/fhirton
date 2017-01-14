FHIRTON
=======

This is the code from the HL7 Connectathon September 2016.  Feel free to do as you will with it, ;-)


Use Cases
---------
Possible Use cases to develop for the Connectathon.

## Study Registration
* FHIR Gateway advertises Clinical Study Resources
* EHR system consumes resources

## SDC
* Questionnaire
   * Transform Rave ODM into Questionnaire Resource
* QuestionnaireResponse
   * Process QuestionnaireResponse Resource and POST to Rave

# DAF
* DM
  * POST - Transform DAF-Patient resource into a DM record, Push to Rave
  * GET - Transform DM panel to DAF-patient (will probably be non-compliant?)
* VS 
  * POST - Transform DAF-VitalSigns resource into a VS record, Push to Rave
  * GET - Extract a VS CRF and transform to DAF-vitalsigns

Demographics
* DAF-Patient
  * Race => us-core (US Realm)
  * Ethnicity
* ~ Patient-clinicalTrials

## Research (2017)
* Prepopulating study research data from an EHR
    * __Action__: Prepopulate eCRFs in an EDC clinical database with data pulled via FHIR from an EHR using loose matching criteria. Multiple versions of a CRF type (e.g. vital signs) can be used to represent different types of clinical studies (e.g. observational vs. regulated).
    * __Success Criteria__: Data from the FHIR resources are extracted through the FHIR API and mapped to clinical research data element fields on CRFs. Each FHIR resource data element has been successfully imported for display in the CRFs, or documented in the mapping table as not for use in clinical research. The matching criteria is intentionally loose in this step, meaning the data may not be usable as-is and the assessment of data content suitability for research will be performed in step 2.
* Determine the FHIR resource EHR data content and quality assessed against the clinical research requirements
    * __Action__: evaluate the test data suitability for use in clinical research databases by assessing what actions would be needed to (1) load the data into non-regulated clinical research databases including those supporting observational studies, and (2) load the data into regulated clinical research database that requires CDISC standards alignment.
    * __Success Criteria__: The resulting table should function as a map highlighting potential data content issues to be addressed in future profile development activities. Summary statistics will be derived to assess the results recorded in the table.