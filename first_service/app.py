import requests
import json

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def ping():
    return "<h2>pong</h2>"


@app.route("/check/<int:patient_id>/<string:text>")
def check(patient_id, text):
    response = requests.get("http://second_service:5000/search_patient/1")
    status_code = response.status_code
    status_ok = response.ok

    if status_ok:
        # (patient_id, text, ICD codes, is_new_patient)
        response_content = response.content
        response_content_as_dict = json.loads(response_content)
        is_new_patient = not response_content_as_dict["ok"]
        return jsonify(
            {
                "ok": True,
                "patient_id": patient_id,
                "text": text,
                "ICD codes": "",
                "is_new_patient": is_new_patient,
            }
        )

    else:
        return jsonify({"ok": False, "error": response_content})


if __name__ == "__main__":
    app.run(debug=True)
