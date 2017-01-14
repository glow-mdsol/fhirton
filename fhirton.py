from flask import Flask, abort, jsonify, render_template, request, redirect
from flask_socketio import SocketIO

import appconfig
from fhir import FHIRConnection
from rave import get_rave_subjects, push_demographics, push_conmeds

app = Flask(__name__)
app.config['SECRET_KEY'] = '!secret!'
socketio = SocketIO(app)

@app.route("/")
def index():
    return redirect("/populate")


@app.route('/populate')
def populate():
    fhir = FHIRConnection(appconfig.ENDPOINT)
    fhir_subjects = fhir.patients
    rave_subjects = get_rave_subjects()
    return render_template("populate.html",
                           rave_subjects=rave_subjects,
                           fhir_subjects=fhir_subjects,
                           study_name=appconfig.STUDY,
                           endpoint=appconfig.ENDPOINT)

@app.route('/inspect')
def populate():
    fhir = FHIRConnection(appconfig.ENDPOINT)
    fhir_subjects = fhir.patients
    return render_template("inspect.html")


@app.route("/post", methods=['POST'])
def initiate_transfer():
    rave_uuid = request.form.get('rave_uuid')
    fhir_id = request.form.get('fhir_id')
    dataset = request.form.get('dataset')
    if None in [rave_uuid, fhir_id, dataset]:
        print("Values: %s" % [rave_uuid, fhir_id, dataset])
        return abort(400)
    fhir = FHIRConnection(appconfig.ENDPOINT)
    if dataset == 'DM':
        demog = fhir.get_patient(fhir_id)
        if not demog:
            return abort(404)
        result = push_demographics(rave_uuid, demog)
        return jsonify(dict(status=200))
    elif dataset == 'CM':
        conmeds = fhir.get_patient_medications(fhir_id)
        if not conmeds:
            return abort(404)
        result = push_conmeds(rave_uuid, conmeds)
    return jsonify(dict(status=200))


if __name__ == '__main__':
    app.run()
