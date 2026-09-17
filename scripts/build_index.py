import os
import csv
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'contacts.csv')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'template.html')
OUTPUT_PATH = os.path.join(BASE_DIR, 'index.html')

with open(CSV_PATH, 'r', encoding='utf-8') as f:
    contacts = list(csv.DictReader(f))

with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    template = f.read()

contacts_json = json.dumps(contacts, ensure_ascii=False)
final_html = template.replace('/*CONTACTS_DATA*/[]', contacts_json)

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"Successfully generated index.html with {len(contacts)} contacts! File size: {len(final_html)} bytes.")

