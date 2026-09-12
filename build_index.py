import csv
import json

with open('/home/angsuman/extra_spac/Contact/contacts.csv', 'r', encoding='utf-8') as f:
    contacts = list(csv.DictReader(f))

with open('/home/angsuman/extra_spac/Contact/template.html', 'r', encoding='utf-8') as f:
    template = f.read()

contacts_json = json.dumps(contacts, ensure_ascii=False)
final_html = template.replace('/*CONTACTS_DATA*/[]', contacts_json)

with open('/home/angsuman/extra_spac/Contact/index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"Successfully generated index.html with {len(contacts)} contacts! File size: {len(final_html)} bytes.")
