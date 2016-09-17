# Use Cases

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