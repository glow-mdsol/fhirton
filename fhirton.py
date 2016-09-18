from flask import Flask, abort, jsonify, render_template, request
from flask_socketio import SocketIO

import appconfig
from fhir import FHIRConnection
from rave import get_rave_subjects

app = Flask(__name__)
app.config['SECRET_KEY'] = '!secret!'
socketio = SocketIO(app)


@app.route('/populate')
def populate():
    endpoint = "http://fhir.careevolution.com/apitest/fhir"
    fhir = FHIRConnection(endpoint)
    fhir_subjects = fhir.patients
    rave_subjects = get_rave_subjects()
    return render_template("populate.html",
                           rave_subjects=rave_subjects,
                           fhir_subjects=fhir_subjects,
                           study_name=appconfig.STUDY,
                           endpoint=endpoint)


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


if __name__ == '__main__':
    app.run()
