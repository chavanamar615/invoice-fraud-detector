import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)
np.random.seed(42)
Faker.seed(42)

genuine_vendors = list(set([fake.company() for _ in range(400)]))[:300]
fraud_vendors = list(set([fake.company() for _ in range(120)]))[:80]

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 6, 30)

def random_date():
    delta = end_date - start_date
    return (start_date + timedelta(days=random.randint(0, delta.days))).strftime("%Y-%m-%d")

def random_file_path(invoice_num):
    return f"data/invoices/INV-{invoice_num:05d}.pdf"

departments = ['IT', 'HR', 'Finance', 'Operations', 'Marketing', 'Legal', 'Admin']
payment_terms = ['Net 30', 'Net 60', 'Net 90', 'Immediate', 'Net 15']

data = []
invoice_num = 1

for _ in range(7000):
    data.append([
        invoice_num,
        random.choice(genuine_vendors),
        round(random.uniform(1000, 80000), 2),
        random_date(),
        random_file_path(invoice_num),
        random.randint(0, 30),
        random.choices([1, 2], weights=[95, 5])[0],
        random.choice(departments),
        random.choice(payment_terms),
        0
    ])
    invoice_num += 1

for _ in range(3000):
    data.append([
        invoice_num,
        random.choice(fraud_vendors),
        round(random.uniform(5000, 150000), 2),
        random_date(),
        random_file_path(invoice_num),
        random.randint(0, 30),
        random.choices([1, 2, 3, 4, 5], weights=[20, 35, 25, 15, 5])[0],
        random.choice(departments),
        random.choice(payment_terms),
        1
    ])
    invoice_num += 1

columns = ['invoice_number', 'vendor', 'amount', 'date', 'file_path',
           'days_overdue', 'duplicate_count', 'department', 'payment_term', 'label']

df = pd.DataFrame(data, columns=columns)
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv("invoices_data.csv", index=False)

print(f"Total invoices   : {len(df)}")
print(f"Genuine invoices : {len(df[df['label'] == 0])}")
print(f"Fraud invoices   : {len(df[df['label'] == 1])}")
print(f"Unique vendors   : {df['vendor'].nunique()}")
print(f"Amount range     : {df['amount'].min()} to {df['amount'].max()}")
print(f"Date range       : {df['date'].min()} to {df['date'].max()}")