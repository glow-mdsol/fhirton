from flask import Flask, abort, request

from database import StudyParticipant
from fhir import get_fhir_subjects
from rave import get_rave_subjects

app = Flask(__name__)




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
