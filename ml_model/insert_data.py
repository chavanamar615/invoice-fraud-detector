import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Amar@2915",
    database="invoice_fraud_db"
)
cursor = conn.cursor()

df = pd.read_csv("invoices_data.csv")
print(f"Total rows to insert: {len(df)}")

cursor.execute("DELETE FROM predictions")
cursor.execute("DELETE FROM invoices")
cursor.execute("ALTER TABLE invoices AUTO_INCREMENT = 1")
conn.commit()
print("Cleared existing data!")

success = 0
failed = 0

for _, row in df.iterrows():
    try:
        sql = "INSERT INTO invoices (vendor, amount, date, file_path) VALUES (%s, %s, %s, %s)"
        values = (
            str(row['vendor'])[:100],
            round(float(row['amount']), 2),
            str(row['date']),
            str(row['file_path'])[:255]
        )
        cursor.execute(sql, values)
        success += 1
    except Exception as e:
        print(f"Row failed: {e}")
        failed += 1

conn.commit()
print(f"Successfully inserted : {success}")
print(f"Failed                : {failed}")

cursor.close()
conn.close()