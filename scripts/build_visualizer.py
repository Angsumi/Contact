import os
import csv
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'contacts.csv')
DELETED_CSV_PATH = os.path.join(BASE_DIR, 'data', 'dleted_contact.csv')

# Load contacts.csv
with open(CSV_PATH, 'r', encoding='utf-8') as f:
    contacts = list(csv.DictReader(f))

# Load deleted contacts for comparison
try:
    with open(DELETED_CSV_PATH, 'r', encoding='utf-8') as f:
        deleted_contacts = list(csv.DictReader(f))
except Exception:
    deleted_contacts = []

# City Coordinates Registry
GEO_COORDS = {
    "Rangachakua": [26.7324, 92.9372],
    "Jamugurihat": [26.7266, 92.9463],
    "Guwahati": [26.1445, 91.7362],
    "Narayanpur": [26.9984, 93.8821],
    "Tezpur": [26.6338, 92.7926],
    "Sootea": [26.7915, 93.0682],
    "Dhemaji": [27.4816, 94.5779],
    "Bihpuria": [27.0267, 93.9317],
    "Gohpur": [26.8837, 93.6198],
    "Jorhat": [26.7509, 94.2037],
    "Dibrugarh": [27.4728, 94.9120],
    "Nagaon": [26.3452, 92.6840],
    "Itakhola": [26.8378, 93.1812],
    "Biswanath": [26.7361, 93.1534],
    "Biswanath Chariali": [26.7361, 93.1534],
    "Sivasagar": [26.9826, 94.6425],
    "Lakhimpur": [27.2349, 94.1037],
    "North Lakhimpur": [27.2349, 94.1037],
    "Lakhimpur Town": [27.2349, 94.1037],
    "Majuli": [26.9602, 94.2235],
    "Golaghat": [26.5239, 93.9667],
    "Rowta": [26.7029, 92.2344],
    "Tinsukia": [27.4922, 95.3468],
    "Diplunga": [26.8120, 93.1200],
    "Diphu": [25.8457, 93.4358],
    "Goreswar": [26.5350, 91.6880],
    "Dergaon": [26.7011, 93.9715],
    "Nalbari": [26.4468, 91.4363],
    "Barpeta": [26.3216, 91.0058],
    "Mangaldai": [26.4358, 92.0367],
    "Morigaon": [26.2575, 92.3381],
    "Silchar": [24.8333, 92.7789],
    "Bongaigaon": [26.4800, 90.5584],
    "Kokrajhar": [26.4014, 90.2716],
    "Goalpara": [26.1788, 90.6276],
    "Dhubri": [26.0207, 89.9742],
    "Karimganj": [24.8649, 92.3593],
    "Hailakandi": [24.6833, 92.5667],
    "Udalguri": [26.7452, 92.0962],
    "Hojai": [26.0020, 92.8596],
    "Charaideo": [26.9200, 94.8800],
    "South Salmara": [25.9600, 89.9200],
    "Majbat": [26.7800, 92.3400],
    "Bhalukpong": [27.0125, 92.6436],
    "Itanagar": [27.0844, 93.6053],
    "Naharlagun": [27.1064, 93.6938],
    "Pasighat": [28.0664, 95.3267],
    "Delhi": [28.6139, 77.2090],
    "New Delhi": [28.6139, 77.2090],
    "Bengaluru": [12.9716, 77.5946],
    "Bangalore": [12.9716, 77.5946],
    "Mumbai": [19.0760, 72.8777],
    "Kolkata": [22.5726, 88.3639],
    "Chennai": [13.0827, 80.2707],
    "Hyderabad": [17.3850, 78.4867],
    "Pune": [18.5204, 73.8567],
    "United States": [37.0902, -95.7129],
    "US": [37.0902, -95.7129],
    "Slovakia": [48.6690, 19.6990],
    "Australia": [-25.2744, 133.7751],
    "United Arab Emirates": [23.4241, 53.8478],
    "UAE": [23.4241, 53.8478],
    "United Kingdom": [55.3781, -3.4360],
    "UK": [55.3781, -3.4360],
    "London": [51.5074, -0.1278]
}

def clean_phone(p):
    if not p: return ""
    s = re.sub(r'[^0-9]', '', str(p))
    if len(s) >= 10:
        return s[-10:]
    return s

def get_operator(phone10):
    if not phone10 or len(phone10) < 2:
        return "Other / Unknown"
    p2 = phone10[:2]
    if p2 in ['70', '60', '79', '62', '63', '77', '78', '80', '81', '82', '83', '85', '87', '89']:
        return "Jio"
    elif p2 in ['98', '99', '91', '86', '88', '75', '76', '96', '97']:
        return "Airtel"
    elif p2 in ['94', '95']:
        return "BSNL"
    elif p2 in ['93', '84', '90', '92']:
        return "Vi"
    else:
        return "Other / Regional"

enhanced_contacts = []
for idx, c in enumerate(contacts):
    first_name = (c.get('First Name') or '').strip()
    middle_name = (c.get('Middle Name') or '').strip()
    last_name = (c.get('Last Name') or '').strip()
    full_name = f"{first_name} {middle_name} {last_name}".replace('  ', ' ').strip()
    if not full_name:
        full_name = "Unnamed Contact"

    org_name = (c.get('Organization Name') or '').strip()
    org_title = (c.get('Organization Title') or '').strip()
    city = (c.get('Address 1 - City') or '').strip()
    region = (c.get('Address 1 - Region') or '').strip()
    country = (c.get('Address 1 - Country') or '').strip()
    street = (c.get('Address 1 - Street') or '').strip()
    formatted_addr = (c.get('Address 1 - Formatted') or '').strip()
    
    phone1 = (c.get('Phone 1 - Value') or '').strip()
    phone2 = (c.get('Phone 2 - Value') or '').strip()
    email1 = (c.get('E-mail 1 - Value') or '').strip()
    email2 = (c.get('E-mail 2 - Value') or '').strip()
    photo = (c.get('Custom Field 1 - Value') or c.get('Photo') or '').strip()
    if not photo.startswith('http'):
        photo = ''
    nickname = (c.get('Nickname') or '').strip()
    notes = (c.get('Notes') or '').strip()
    labels = (c.get('Labels') or '').strip()

    # Kinship & Honorific detection
    honorifics = []
    text_corpus = f"{first_name} {last_name} {nickname} {org_title} {notes}".lower()
    if re.search(r'\bda\b|\bdada\b', text_corpus) or ' da' in first_name.lower() or ' da' in last_name.lower():
        honorifics.append('Da (Elder Bro)')
    if re.search(r'\bba\b|\bbaideo\b', text_corpus) or ' ba' in first_name.lower():
        honorifics.append('Ba (Elder Sis)')
    if 'sir' in text_corpus or 'professor' in text_corpus or 'teacher' in text_corpus:
        honorifics.append('Sir / Teacher')
    if 'madam' in text_corpus or 'mam' in text_corpus:
        honorifics.append('Madam')
    if 'relative' in text_corpus or 'family' in text_corpus or 'uncle' in text_corpus or 'khura' in text_corpus or 'mama' in text_corpus:
        honorifics.append('Kinship / Family')
    if 'class-mate' in text_corpus or 'batch-mate' in text_corpus or 'student' in text_corpus:
        honorifics.append('Academic Peer')

    lat, lng = None, None
    if city in GEO_COORDS:
        lat, lng = GEO_COORDS[city]
    elif region in GEO_COORDS:
        lat, lng = GEO_COORDS[region]
    elif country in GEO_COORDS:
        lat, lng = GEO_COORDS[country]
    elif 'rangachakua' in formatted_addr.lower():
        lat, lng = GEO_COORDS['Rangachakua']
    elif 'jamugurihat' in formatted_addr.lower():
        lat, lng = GEO_COORDS['Jamugurihat']
    elif 'guwahati' in formatted_addr.lower():
        lat, lng = GEO_COORDS['Guwahati']
    elif 'tezpur' in formatted_addr.lower():
        lat, lng = GEO_COORDS['Tezpur']

    p1_clean = clean_phone(phone1)
    op = get_operator(p1_clean)

    contact_obj = {
        "id": idx + 1,
        "name": full_name,
        "first_name": first_name,
        "last_name": last_name,
        "org": org_name,
        "title": org_title,
        "city": city or "Unknown",
        "region": region or "Assam",
        "country": country or "India",
        "formatted_addr": formatted_addr,
        "phone1": phone1,
        "phone2": phone2,
        "email": email1 or email2,
        "photo": photo,
        "nickname": nickname,
        "notes": notes,
        "labels": labels,
        "honorifics": honorifics,
        "lat": lat,
        "lng": lng,
        "operator": op
    }
    enhanced_contacts.append(contact_obj)

print(f"Loaded {len(enhanced_contacts)} active contacts.")
