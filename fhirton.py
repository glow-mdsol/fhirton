from flask import Flask, request, abort

from database import StudyParticipant

app = Flask(__name__)

@app.route("/Patient")
def get_patients():
    pass


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
