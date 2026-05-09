import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml_model'))

from flask import Flask, request, jsonify
import joblib
import numpy as np
import mysql.connector
from datetime import datetime

app = Flask(__name__)

model     = joblib.load('../ml_model/model.pkl')
scaler    = joblib.load('../ml_model/scaler.pkl')
le_vendor = joblib.load('../ml_model/le_vendor.pkl')
le_dept   = joblib.load('../ml_model/le_dept.pkl')
le_payment= joblib.load('../ml_model/le_payment.pkl')

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Amar@2915",
        database="invoice_fraud_db"
    )

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    vendor       = data['vendor']
    amount       = float(data['amount'])
    days_overdue = int(data['days_overdue'])
    duplicate    = int(data['duplicate_count'])
    department   = data['department']
    payment_term = data['payment_term']

    if vendor in le_vendor.classes_:
        vendor_enc = le_vendor.transform([vendor])[0]
    else:
        vendor_enc = -1

    if department in le_dept.classes_:
        dept_enc = le_dept.transform([department])[0]
    else:
        dept_enc = -1

    if payment_term in le_payment.classes_:
        payment_enc = le_payment.transform([payment_term])[0]
    else:
        payment_enc = -1

    features = np.array([[vendor_enc, amount, days_overdue, duplicate, dept_enc, payment_enc]])
    features_scaled = scaler.transform(features)

    prediction   = model.predict(features_scaled)[0]
    confidence   = round(float(max(model.predict_proba(features_scaled)[0])) * 100, 2)
    label        = "fraud" if prediction == 1 else "genuine"

    invoice_id = data.get('invoice_id', None)
    if invoice_id:
        try:
            conn   = get_db()
            cursor = conn.cursor()
            sql    = "INSERT INTO predictions (invoice_id, label, confidence, flagged_at) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (invoice_id, label, confidence, datetime.now()))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"DB error: {e}")

    return jsonify({
        "invoice_id" : invoice_id,
        "prediction" : label,
        "confidence" : confidence,
        "status"     : "flagged" if prediction == 1 else "clear"
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "running", "model": "XGBoost"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)