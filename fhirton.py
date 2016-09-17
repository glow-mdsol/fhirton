import requests
from flask import Flask, request, abort
from rwslib import RWSConnection

import appconfig
from database import StudyParticipant

app = Flask(__name__)


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


def get_rave_subjects():
    client = RWSConnection(username=appconfig.RAVE_USER,
                           password=appconfig.RAVE_PASSWORD)
    return []


@app.route('/populate')
def populate():
    fhir_subjects = get_fhir_subjects()
    rave_subjects = get_rave_subjects()

@app.route('/Patient/<id>', methods=['GET', 'POST'])
def patient(id=None):
    if request.method == "GET":
        pass
    else:
        if request.content_type == 'application/json+fhir' or request.get('_format') == 'application/json+fhir':
            content = request.get_json()
        elif request.content_type == 'application/xml+fhir' or request.get('_format') == 'application/xml+fhir':
            content = request.get_data()
        else:
            # WHUT?
            return abort(400)

        subject = StudyParticipant.get_by_uuid(id)
        if not subject:
            return abort(404)


if __name__ == '__main__':
    app.run()
