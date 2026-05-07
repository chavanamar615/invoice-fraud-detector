import pandas as pd
import mysql.connector
from datetime import datetime

# ─── Database Connection ────────────────────────────────────────────────────────
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Amar@2915",  # replace with your MySQL password
    database="invoice_fraud_db"
)
cursor = conn.cursor()

# ─── Load CSV ───────────────────────────────────────────────────────────────────
df = pd.read_csv("invoices_data.csv")
print(f"Total rows to insert: {len(df)}")

# ─── Clear existing data ────────────────────────────────────────────────────────
cursor.execute("DELETE FROM predictions")
cursor.execute("DELETE FROM invoices")
cursor.execute("ALTER TABLE invoices AUTO_INCREMENT = 1")
conn.commit()
print("Cleared existing data!")

# ─── Insert rows ────────────────────────────────────────────────────────────────
success = 0
failed  = 0

for _, row in df.iterrows():
    try:
        sql = """
            INSERT INTO invoices (vendor, amount, date, file_path)
            VALUES (%s, %s, %s, %s)
        """
        values = (
            str(row['vendor'])[:100],           # varchar(100)
            round(float(row['amount']), 2),     # decimal(10,2)
            str(row['date']),                   # date
            str(row['file_path'])[:255]         # varchar(255)
        )
        cursor.execute(sql, values)
        success += 1
    except Exception as e:
        print(f"Row failed: {e}")
        failed += 1

conn.commit()

# ─── Summary ────────────────────────────────────────────────────────────────────
print("=" * 50)
print("  Data Insertion Complete!")
print("=" * 50)
print(f"  Successfully inserted : {success}")
print(f"  Failed                : {failed}")
print("=" * 50)

cursor.close()
conn.close()