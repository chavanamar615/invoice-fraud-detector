import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import random

random.seed(42)
np.random.seed(42)

vendors_genuine = ['TechCorp', 'InfoSys', 'DataPro', 'NetSol', 'CloudBase', 'SoftNet', 'DigiTech', 'InfoPro']
vendors_fraud = ['FakeCorp', 'GhostInc', 'ShadowLtd', 'PhantomCo', 'DummyInc']

data = []

for i in range(0, 7000):
    vendor = random.choice(vendors_genuine)
    amount = random.randint(3000, 20000)
    days_overdue = random.randint(0, 10)
    duplicate_count = 1
    label = 0
    data.append([vendor, amount, days_overdue, duplicate_count, label])

for j in range(0, 3000):
    fraud_vendor = random.choice(vendors_fraud)
    fraud_amount = random.randint(40000, 100000)
    fraud_days_overdue = random.randint(0, 2)
    fraud_duplicate_count = random.randint(2, 5)
    fraud_label = 1
    data.append([fraud_vendor, fraud_amount, fraud_days_overdue, fraud_duplicate_count, fraud_label])

df = pd.DataFrame(data, columns=['vendor', 'amount', 'days_overdue', 'duplicate_count', 'label'])
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv("invoices_data.csv", index=False)

print("Done! Total rows:", len(df))
print(df.head())
print("Fraud:", df['label'].sum())
print("Genuine:", len(df) - df['label'].sum())