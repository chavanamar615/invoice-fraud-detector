import mysql.connector
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
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

output_dir = "../data/invoices"
os.makedirs(output_dir, exist_ok=True)
styles = getSampleStyleSheet()

for row in invoices:
    invoice_num = f"INV-{int(row['id']):05d}"
    doc = SimpleDocTemplate(f"{output_dir}/{invoice_num}.pdf", pagesize=A4)
    elements = [
        Paragraph(f"Invoice Number : {invoice_num}",          styles['Normal']),
        Spacer(1, 10),
        Paragraph(f"Vendor         : {row['vendor']}",        styles['Normal']),
        Spacer(1, 10),
        Paragraph(f"Amount         : ${row['amount']}",       styles['Normal']),
        Spacer(1, 10),
        Paragraph(f"Date           : {row['date']}",          styles['Normal']),
        Spacer(1, 10),
        Paragraph(f"File Path      : {row['file_path']}",     styles['Normal']),
    ]
    doc.build(elements)
    print(f"Created: {invoice_num}.pdf | Vendor: {row['vendor']} | Amount: ${row['amount']}")

print(f"\nTotal PDFs created: {len(invoices)}")
print(f"Saved in: {output_dir}")