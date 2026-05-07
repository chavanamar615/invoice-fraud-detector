import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)
np.random.seed(42)
Faker.seed(42)

# ─── Generate 300 unique genuine vendors ───────────────────────────────────────
genuine_vendors = list(set([fake.company() for _ in range(400)]))[:300]

# ─── Generate 80 unique fraud vendors ──────────────────────────────────────────
fraud_vendors = list(set([fake.company() for _ in range(120)]))[:80]

# ─── Date range: last 1.5 years ─────────────────────────────────────────────────
start_date = datetime(2023, 1, 1)
end_date   = datetime(2024, 6, 30)

def random_date():
    delta = end_date - start_date
    return (start_date + timedelta(days=random.randint(0, delta.days))).strftime("%Y-%m-%d")

def random_file_path(invoice_num):
    return f"data/invoices/INV-{invoice_num:05d}.pdf"

# ─── Departments ────────────────────────────────────────────────────────────────
departments = ['IT', 'HR', 'Finance', 'Operations', 'Marketing', 'Legal', 'Admin']

# ─── Payment terms ──────────────────────────────────────────────────────────────
payment_terms = ['Net 30', 'Net 60', 'Net 90', 'Immediate', 'Net 15']

data = []
invoice_num = 1

# ─── 7000 Genuine invoices ──────────────────────────────────────────────────────
for _ in range(7000):
    vendor          = random.choice(genuine_vendors)
    amount          = round(random.uniform(1000, 25000), 2)
    date            = random_date()
    file_path       = random_file_path(invoice_num)
    days_overdue    = random.randint(0, 15)
    duplicate_count = 1
    department      = random.choice(departments)
    payment_term    = random.choice(payment_terms)
    label           = 0  # genuine

    data.append([invoice_num, vendor, amount, date, file_path,
                 days_overdue, duplicate_count, department, payment_term, label])
    invoice_num += 1

# ─── 3000 Fraud invoices ────────────────────────────────────────────────────────
for _ in range(3000):
    vendor          = random.choice(fraud_vendors)
    amount          = round(random.uniform(40000, 150000), 2)  # unusually high
    date            = random_date()
    file_path       = random_file_path(invoice_num)
    days_overdue    = random.randint(0, 3)
    duplicate_count = random.randint(2, 6)                     # duplicated invoices
    department      = random.choice(departments)
    payment_term    = random.choice(payment_terms)
    label           = 1  # fraud

    data.append([invoice_num, vendor, amount, date, file_path,
                 days_overdue, duplicate_count, department, payment_term, label])
    invoice_num += 1

# ─── Build DataFrame ────────────────────────────────────────────────────────────
columns = ['invoice_number', 'vendor', 'amount', 'date', 'file_path',
           'days_overdue', 'duplicate_count', 'department', 'payment_term', 'label']

df = pd.DataFrame(data, columns=columns)
df = df.sample(frac=1).reset_index(drop=True)

# ─── Save CSV ───────────────────────────────────────────────────────────────────
df.to_csv("invoices_data.csv", index=False)

# ─── Summary ────────────────────────────────────────────────────────────────────
print("=" * 50)
print("  Invoice Data Generation Complete!")
print("=" * 50)
print(f"  Total invoices   : {len(df)}")
print(f"  Genuine invoices : {len(df[df['label'] == 0])}")
print(f"  Fraud invoices   : {len(df[df['label'] == 1])}")
print(f"  Unique vendors   : {df['vendor'].nunique()}")
print(f"  Date range       : {df['date'].min()} to {df['date'].max()}")
print("=" * 50)
print(df.head(5))