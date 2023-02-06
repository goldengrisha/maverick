import os

import psycopg2

from flask import Flask, jsonify

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        host="postgres",
        database="maverick-db",
        user=os.environ.get("POSTGRES_USER", "root"),
        password=os.environ.get("POSTGRES_PASS", "password"),
    )
    return conn


@app.route("/")
def ping():
    return "<h2>pong</h2>"


@app.route("/search_patient/<int:patient_id>")
def search_patient(patient_id):
    result = {"ok": False, "data": None}
    if patient_id is not None:
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("SELECT * FROM patient WHERE patient_id = %s", (patient_id,))
        user = cur.fetchone()
        cur.close()
        connection.close()

        if user is not None:
            result["ok"] = True
            result["data"] = user[0]
        else:
            result["data"] = "User not found"

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
