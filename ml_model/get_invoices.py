import mysql.connector
import pandas as pd
import os

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Amar@2915",
    database="invoice_fraud_db"
)

cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM invoices LIMIT 20")
invoices = cursor.fetchall()
cursor.close()
conn.close()

df = pd.DataFrame(invoices)
output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'temp_invoices.csv')
df.to_csv(output_path, index=False)

print(f"Total invoices fetched : {len(df)}")
print(f"Saved to               : {output_path}")
print(df[['id', 'vendor', 'amount', 'date']].to_string(index=False))