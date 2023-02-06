import json
import requests
import pickle

from flask import Flask, jsonify, request
from helpers import get_clean_text, convert_text_to_vector

app = Flask(__name__)


@app.route("/")
def just_test():
    loaded_model = pickle.load(open("./models/random_forest_model.pickle", "rb"))
    text = (
        "pt transferred to [**hospital unit name 4**] c/ respiratory distress [**9-6**]"
    )
    cleaned_tex = get_clean_text(text)
    vector = convert_text_to_vector(cleaned_tex)
    prediction = loaded_model.predict(vector)
    icd = prediction[0]

    return jsonify({"prediction": icd})


@app.route("/check", methods=["POST"])
def check():
    response = requests.get("http://second_service:5000/search_patient/1")
    status_code = response.status_code
    status_ok = response.ok

    if status_ok and request.method == "POST":
        patient_id = request.form.get("patient_id")
        text = request.form.get("text")

        if text:
            loaded_model = pickle.load(
                open("./models/random_forest_model.pickle", "rb")
            )
            cleaned_tex = get_clean_text(text)
            vector = convert_text_to_vector(cleaned_tex)
            prediction = loaded_model.predict(vector)
            icd = prediction[0]

            # (patient_id, text, ICD codes, is_new_patient)
            response_content = response.content
            response_content_as_dict = json.loads(response_content)
            is_new_patient = not response_content_as_dict["ok"]
            return jsonify(
                {
                    "ok": True,
                    "patient_id": patient_id,
                    "text": text,
                    "ICD codes": icd,
                    "is_new_patient": is_new_patient,
                }
            )
        else:
            return jsonify({"ok": False, "error": "text is empty"})
    else:
        return jsonify({"ok": False, "error": response_content})


if __name__ == "__main__":
    app.run(debug=True)
