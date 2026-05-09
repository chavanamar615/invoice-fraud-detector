import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from xgboost import XGBClassifier
import joblib
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("invoices_data.csv")
print(f"Data loaded: {len(df)} rows | Genuine: {len(df[df['label']==0])} | Fraud: {len(df[df['label']==1])}")

le_vendor = LabelEncoder()
le_dept = LabelEncoder()
le_payment = LabelEncoder()

df['vendor'] = le_vendor.fit_transform(df['vendor'])
df['department'] = le_dept.fit_transform(df['department'])
df['payment_term'] = le_payment.fit_transform(df['payment_term'])

features = ['vendor', 'amount', 'days_overdue', 'duplicate_count', 'department', 'payment_term']
X = df[features]
y = df['label']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
print(f"Train: {len(X_train)} rows | Test: {len(X_test)} rows")

print("\nTraining Random Forest...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_f1 = f1_score(y_test, rf_pred)
print(f"Accuracy: {accuracy_score(y_test, rf_pred)*100:.2f}% | F1: {rf_f1*100:.2f}%")
print(classification_report(y_test, rf_pred, target_names=['Genuine', 'Fraud']))

print("Training XGBoost...")
xgb_model = XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
xgb_model.fit(X_train, y_train)
xgb_pred = xgb_model.predict(X_test)
xgb_f1 = f1_score(y_test, xgb_pred)
print(f"Accuracy: {accuracy_score(y_test, xgb_pred)*100:.2f}% | F1: {xgb_f1*100:.2f}%")
print(classification_report(y_test, xgb_pred, target_names=['Genuine', 'Fraud']))

if xgb_f1 >= rf_f1:
    best_model, best_name = xgb_model, "XGBoost"
else:
    best_model, best_name = rf_model, "Random Forest"

print(f"Winner: {best_name}")

joblib.dump(best_model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(le_vendor, "le_vendor.pkl")
joblib.dump(le_dept, "le_dept.pkl")
joblib.dump(le_payment, "le_payment.pkl")

print("Model and encoders saved successfully!")