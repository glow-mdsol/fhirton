# -*- coding: utf-8 -*-

import urllib

from flask import Flask, abort, jsonify, render_template, request, redirect
from flask_socketio import SocketIO
from requests import HTTPError

import appconfig
from fhir import FHIRConnection
from rave import get_rave_subjects, push_demographics, push_conmeds

app = Flask(__name__)
app.config['SECRET_KEY'] = '!secret!'
socketio = SocketIO(app)

@app.route("/")
def index():
    return redirect("/inspect")


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
def inspect():
    return render_template("inspect.html",
                           fhir_servers=appconfig.SERVERS,
                           domains=appconfig.DOMAINS)


@app.route("/url/patients")
def retrieve_patients():
    passed_url = request.args.get('url')
    if not passed_url:
        return abort(404)
    target_url = urllib.parse.unquote(passed_url).strip()
    print("Seeking '%s'" % target_url)
    client = FHIRConnection(target_url)
    try:
        return jsonify(client.patients)
    except HTTPError as exc:
        print("HTTP Error: %s" % exc.response.body)
        return abort(exc.response.status_code)


@app.route("/url/patients/<patient_id>")
def retrieve_patient(patient_id=None):
    passed_url = request.args.get('url')
    if not passed_url:
        return abort(404)
    target_url = urllib.parse.unquote(passed_url)
    client = FHIRConnection(target_url)
    if not patient_id:
        return abort(404)
    print("Seeking Patient %s at %s" % (patient_id, target_url))
    patient = client.get_patient(patient_id=urllib.parse.unquote(patient_id))
    return jsonify(patient)

@app.route("/url/patients/<patient_id>/<domain>")
def retrieve_patient_domain(patient_id=None, domain=None):
    passed_url = request.args.get('url')
    if not passed_url:
        return abort(404)
    target_url = urllib.parse.unquote(passed_url)
    client = FHIRConnection(target_url)
    if not patient_id:
        return abort(404)
    if domain == 'dm':
        print("Seeking Patient %s at %s" % (patient_id, target_url))
        result = client.get_patient(patient_id=urllib.parse.unquote(patient_id))
    return jsonify(result)


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
