from flask import Flask, abort, request, jsonify
from flask import render_template

import appconfig
from database import StudyParticipant
from fhir import FHIRConnection
from rave import get_rave_subjects

app = Flask(__name__)




@app.route('/populate')
def populate():
    fhir = FHIRConnection("http://fhir.careevolution.com/apitest/fhir")
    fhir_subjects = fhir.patients
    rave_subjects = get_rave_subjects()
    return render_template("populate.html", rave_subjects=rave_subjects, fhir_subjects=fhir_subjects,
                           study_name=appconfig.STUDY)


@app.route("/post", methods=['POST'])
def initiate_transfer():
    rave_uuid = request.form.get('rave_uuid')
    fhir_id = request.form.get('fhir_id')
    dataset = request.form.get('dataset')
    if None in [rave_uuid, fhir_id, dataset]:
        print("Values: %s" % [rave_uuid, fhir_id, dataset])
        return abort(400)
    fhir = FHIRConnection("http://fhir.careevolution.com/apitest/fhir")
    if dataset == 'DM':
        demog = fhir.get_patient(fhir_id)
        if not demog:
            return abort(404)
        print("Got Patient: %s" % demog.json())
    elif dataset == 'CM':
        conmeds = fhir.get_patient_medications(fhir_id)
        if not conmeds:
            return abort(404)
        print("Got Conmeds: %s" % len(conmeds))
        for idx, conmed in enumerate(conmeds):
            print("{}: {}".format(idx, conmed))
    return jsonify(dict(status=200))

# @app.route('/Patient/<id>', methods=['GET', 'POST'])
# def patient(id=None):
#     if request.method == "GET":
#         pass
#     else:
#         if request.content_type == 'application/json+fhir' or request.get('_format') == 'application/json+fhir':
#             content = request.get_json()
#         elif request.content_type == 'application/xml+fhir' or request.get('_format') == 'application/xml+fhir':
#             content = request.get_data()
#         else:
#             # WHUT?
#             return abort(400)
#
#         subject = StudyParticipant.get_by_uuid(id)
#         if not subject:
#             return abort(404)


if __name__ == '__main__':
    app.run()
