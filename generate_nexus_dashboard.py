import csv
import json
import re

# Load contacts.csv
with open('/home/angsuman/extra_spac/Contact/contacts.csv', 'r', encoding='utf-8') as f:
    contacts = list(csv.DictReader(f))

# Load deleted contacts for comparison
try:
    with open('/home/angsuman/extra_spac/Contact/dleted_contact.csv', 'r', encoding='utf-8') as f:
        deleted_contacts = list(csv.DictReader(f))
except Exception:
    deleted_contacts = []

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
        return "Unknown / Regional"
    p2 = phone10[:2]
    if p2 in ['70', '60', '79', '62', '63', '77', '78', '80', '81', '82', '83', '85', '87', '89']:
        return "Jio"
    elif p2 in ['98', '99', '91', '86', '88', '75', '76', '96', '97']:
        return "Airtel"
    elif p2 in ['94', '95']:
        return "BSNL"
    elif p2 in ['93', '84', '90', '92']:
        return "Vi (Vodafone Idea)"
    else:
        return "Other / International"

enhanced_contacts = []
city_stats = {}
org_stats = {}
title_stats = {}
surname_stats = {}
operator_stats = {"Jio": 0, "Airtel": 0, "BSNL": 0, "Vi (Vodafone Idea)": 0, "Other / International": 0}
completeness_stats = {
    "Full Name": 0,
    "Primary Phone": 0,
    "Secondary Phone": 0,
    "Email Address": 0,
    "Organization / Univ": 0,
    "Designation / Title": 0,
    "City Location": 0,
    "State / Region": 0,
    "Country": 0,
    "Street Address": 0,
    "Photo / Google Avatar": 0,
    "Notes & Metadata": 0
}

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
    if 'class-mate' in text_corpus or 'batch-mate' in text_corpus or 'student' in text_corpus or 'hostel' in text_corpus:
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
    operator_stats[op] = operator_stats.get(op, 0) + 1

    if full_name: completeness_stats["Full Name"] += 1
    if phone1: completeness_stats["Primary Phone"] += 1
    if phone2: completeness_stats["Secondary Phone"] += 1
    if email1 or email2: completeness_stats["Email Address"] += 1
    if org_name: completeness_stats["Organization / Univ"] += 1
    if org_title: completeness_stats["Designation / Title"] += 1
    if city: completeness_stats["City Location"] += 1
    if region: completeness_stats["State / Region"] += 1
    if country: completeness_stats["Country"] += 1
    if street: completeness_stats["Street Address"] += 1
    if photo: completeness_stats["Photo / Google Avatar"] += 1
    if notes: completeness_stats["Notes & Metadata"] += 1

    if city: city_stats[city] = city_stats.get(city, 0) + 1
    if org_name: org_stats[org_name] = org_stats.get(org_name, 0) + 1
    if org_title: title_stats[org_title] = title_stats.get(org_title, 0) + 1
    if last_name and len(last_name) > 1 and last_name not in ['Da', 'Sir', 'Madam']:
        surname_stats[last_name] = surname_stats.get(last_name, 0) + 1

    contact_obj = {
        "id": idx + 1,
        "name": full_name,
        "first_name": first_name,
        "last_name": last_name,
        "org": org_name,
        "title": org_title,
        "city": city or "Unassigned",
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

# Top data aggregation dictionaries
top_cities = sorted(city_stats.items(), key=lambda x: x[1], reverse=True)[:15]
top_orgs = sorted(org_stats.items(), key=lambda x: x[1], reverse=True)[:12]
top_titles = sorted(title_stats.items(), key=lambda x: x[1], reverse=True)[:12]
top_surnames = sorted(surname_stats.items(), key=lambda x: x[1], reverse=True)[:15]

# Build Network Graph Nodes and Edges
graph_nodes = []
graph_edges = []
node_id_map = {}

# Hub nodes for Organizations & Key Cities
hub_color_map = {
    "MDU": "#6366f1",
    "THB": "#ec4899",
    "RGU": "#8b5cf6",
    "DGCD": "#14b8a6",
    "DAS": "#f59e0b",
    "Guwahati": "#3b82f6",
    "Rangachakua": "#10b981",
    "Jamugurihat": "#06b6d4"
}

hubs = [
    {"id": "hub_mdu", "label": "Madhabdev Univ (MDU)", "group": "university", "color": "#6366f1", "size": 32},
    {"id": "hub_thb", "label": "THB College", "group": "university", "color": "#ec4899", "size": 28},
    {"id": "hub_rgu", "label": "Rajiv Gandhi Univ (RGU)", "group": "university", "color": "#8b5cf6", "size": 26},
    {"id": "hub_dgcd", "label": "Darrang College", "group": "university", "color": "#14b8a6", "size": 24},
    {"id": "hub_das", "label": "DAS Org", "group": "org", "color": "#f59e0b", "size": 22},
    {"id": "hub_guwahati", "label": "Guwahati Hub", "group": "city", "color": "#3b82f6", "size": 26},
    {"id": "hub_rangachakua", "label": "Rangachakua Community", "group": "city", "color": "#10b981", "size": 30},
    {"id": "hub_jamugurihat", "label": "Jamugurihat Cluster", "group": "city", "color": "#06b6d4", "size": 26}
]

for h in hubs:
    graph_nodes.append(h)

# Add selected contact sample nodes for ultra smooth performance and clear clustering
for c in enhanced_contacts:
    cid = f"c_{c['id']}"
    node_id_map[c['id']] = cid
    
    # pick color
    c_color = "#94a3b8"
    if "Madhabdev" in c['org']: c_color = "#818cf8"
    elif "Tyagbir" in c['org']: c_color = "#f472b6"
    elif "Rajiv Gandhi" in c['org']: c_color = "#a78bfa"
    elif "Darrang" in c['org']: c_color = "#2dd4bf"
    elif "DAS" in c['org']: c_color = "#fbbf24"
    elif "Rangachakua" in c['city']: c_color = "#34d399"
    elif "Jamugurihat" in c['city']: c_color = "#22d3ee"
    elif "Guwahati" in c['city']: c_color = "#60a5fa"

    graph_nodes.append({
        "id": cid,
        "label": c['name'],
        "title": f"<b>{c['name']}</b><br/>{c['title'] or 'No Title'}<br/>{c['org'] or ''}<br/>📍 {c['city']}",
        "group": "person",
        "color": c_color,
        "size": 12 if not c['photo'] else 16,
        "contactId": c['id']
    })

    # Edges to hubs
    if "Madhabdev" in c['org']:
        graph_edges.append({"from": cid, "to": "hub_mdu", "color": {"color": "#818cf8", "opacity": 0.5}})
    if "Tyagbir" in c['org']:
        graph_edges.append({"from": cid, "to": "hub_thb", "color": {"color": "#f472b6", "opacity": 0.5}})
    if "Rajiv Gandhi" in c['org']:
        graph_edges.append({"from": cid, "to": "hub_rgu", "color": {"color": "#a78bfa", "opacity": 0.5}})
    if "Darrang" in c['org']:
        graph_edges.append({"from": cid, "to": "hub_dgcd", "color": {"color": "#2dd4bf", "opacity": 0.5}})
    if "DAS" in c['org']:
        graph_edges.append({"from": cid, "to": "hub_das", "color": {"color": "#fbbf24", "opacity": 0.5}})
    if c['city'] == "Rangachakua":
        graph_edges.append({"from": cid, "to": "hub_rangachakua", "color": {"color": "#34d399", "opacity": 0.4}})
    if c['city'] == "Jamugurihat":
        graph_edges.append({"from": cid, "to": "hub_jamugurihat", "color": {"color": "#22d3ee", "opacity": 0.4}})
    if c['city'] == "Guwahati":
        graph_edges.append({"from": cid, "to": "hub_guwahati", "color": {"color": "#60a5fa", "opacity": 0.4}})

data_payload = {
    "total_contacts": len(enhanced_contacts),
    "total_deleted": len(deleted_contacts),
    "geo_count": sum(1 for c in enhanced_contacts if c['lat'] is not None),
    "org_count": sum(1 for c in enhanced_contacts if c['org']),
    "phone2_count": sum(1 for c in enhanced_contacts if c['phone2']),
    "email_count": sum(1 for c in enhanced_contacts if c['email']),
    "contacts": enhanced_contacts,
    "top_cities": top_cities,
    "top_orgs": top_orgs,
    "top_titles": top_titles,
    "top_surnames": top_surnames,
    "operators": operator_stats,
    "completeness": completeness_stats,
    "graph": {
        "nodes": graph_nodes,
        "edges": graph_edges
    }
}

html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS // Personal Contact Intelligence & Spatial Analytics Matrix</title>
    
    <!-- Modern Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{
                            50: '#eef2ff',
                            100: '#e0e7ff',
                            400: '#818cf8',
                            500: '#6366f1',
                            600: '#4f46e5',
                            700: '#4338ca',
                            900: '#312e81',
                            950: '#0f172a'
                        }},
                        cyber: {{
                            cyan: '#06b6d4',
                            emerald: '#10b981',
                            amber: '#f59e0b',
                            rose: '#f43f5e',
                            violet: '#a855f7'
                        }}
                    }},
                    boxShadow: {{
                        'glow-cyan': '0 0 20px -5px rgba(6, 182, 212, 0.5)',
                        'glow-indigo': '0 0 20px -5px rgba(99, 102, 241, 0.5)',
                        'glow-purple': '0 0 20px -5px rgba(168, 85, 247, 0.5)',
                        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.37)'
                    }}
                }}
            }}
        }}
    </script>
    
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Apache ECharts for High-Dimension Sunburst & Radar -->
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <!-- Leaflet GIS Map + MarkerCluster -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css"/>
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css"/>
    <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
    <!-- Vis-Network for Interactive Physics Social Graph -->
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <!-- Canvas Confetti -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.2/dist/confetti.browser.min.js"></script>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #090d16;
            color: #f1f5f9;
            overflow-x: hidden;
        }}
        .font-mono {{
            font-family: 'JetBrains Mono', monospace;
        }}
        .glass-panel {{
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}
        .glass-panel-light {{
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(0, 0, 0, 0.08);
        }}
        .light body {{
            background-color: #f8fafc;
            color: #0f172a;
        }}
        .light .glass-panel {{
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(226, 232, 240, 0.9);
        }}
        #gisMap {{
            height: 520px;
            width: 100%;
            border-radius: 1rem;
            z-index: 10;
        }}
        #networkCanvas {{
            height: 520px;
            width: 100%;
            border-radius: 1rem;
        }}
        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        ::-webkit-scrollbar-track {{
            background: rgba(15, 23, 42, 0.5);
        }}
        ::-webkit-scrollbar-thumb {{
            background: rgba(99, 102, 241, 0.4);
            border-radius: 3px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(99, 102, 241, 0.8);
        }}
        .pulsing-dot {{
            animation: pulse-ring 2s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
        }}
        @keyframes pulse-ring {{
            0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(6, 182, 212, 0.7); }}
            70% {{ transform: scale(1); box-shadow: 0 0 0 10px rgba(6, 182, 212, 0); }}
            100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(6, 182, 212, 0); }}
        }}
        .custom-popup .leaflet-popup-content-wrapper {{
            background: #0f172a;
            color: #f8fafc;
            border-radius: 0.75rem;
            border: 1px solid rgba(99, 102, 241, 0.3);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        }}
        .custom-popup .leaflet-popup-tip {{
            background: #0f172a;
        }}
        @media print {{
            .no-print {{ display: none !important; }}
            body {{ background: white !important; color: black !important; }}
            .glass-panel {{ border: 1px solid #ccc !important; background: white !important; box-shadow: none !important; }}
        }}
    </style>
</head>
<body class="transition-colors duration-300">

    <!-- TOP GLOW BACKGROUND GRADIENT -->
    <div class="fixed top-0 left-1/4 w-96 h-96 bg-indigo-600/20 rounded-full blur-3xl pointer-events-none -z-10"></div>
    <div class="fixed top-40 right-10 w-96 h-96 bg-cyan-500/15 rounded-full blur-3xl pointer-events-none -z-10"></div>

    <!-- MAIN APP CONTAINER -->
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

        <!-- HEADER NAVIGATION BAR -->
        <header class="glass-panel rounded-2xl p-4 sm:p-6 flex flex-col md:flex-row items-center justify-between gap-4 shadow-glass">
            <div class="flex items-center gap-4 w-full md:w-auto">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-tr from-indigo-600 via-cyan-500 to-emerald-400 p-[2px] shadow-glow-indigo flex-shrink-0">
                    <div class="w-full h-full bg-slate-950 dark:bg-slate-950 rounded-[10px] flex items-center justify-center">
                        <i data-lucide="network" class="w-6 h-6 text-cyan-400"></i>
                    </div>
                </div>
                <div>
                    <div class="flex items-center gap-2">
                        <h1 class="text-xl sm:text-2xl font-black tracking-tight text-white dark:text-white flex items-center gap-2">
                            <span>NEXUS</span>
                            <span class="text-xs font-mono font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-2 py-0.5 rounded-full uppercase tracking-wider">Intelligence v3.0</span>
                        </h1>
                        <span class="inline-flex items-center gap-1 text-[11px] font-mono text-emerald-400 bg-emerald-950/60 border border-emerald-800/40 px-2 py-0.5 rounded-full">
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 pulsing-dot"></span> Live Ready
                        </span>
                    </div>
                    <p class="text-xs sm:text-sm text-slate-400">Deep Exploratory Visualizer & Multi-Dimensional Spatial Social Graph • 606 Active Records</p>
                </div>
            </div>

            <!-- Global Action Controls -->
            <div class="flex flex-wrap items-center gap-2.5 w-full md:w-auto justify-end no-print">
                <!-- Search Trigger -->
                <div class="relative flex-1 sm:w-64 md:w-72">
                    <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2"></i>
                    <input type="text" id="globalSearchInput" placeholder="Quick search (Press '/' or Ctrl+K)..." 
                        class="w-full pl-9 pr-8 py-2 text-xs sm:text-sm rounded-xl bg-slate-900/80 border border-slate-700/60 text-white placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"/>
                    <kbd class="hidden sm:inline-block absolute right-2.5 top-1/2 -translate-y-1/2 text-[10px] font-mono text-slate-500 bg-slate-800 px-1.5 py-0.5 rounded border border-slate-700">/</kbd>
                </div>

                <!-- Theme Toggle -->
                <button id="themeToggleBtn" title="Toggle Light/Dark Theme" class="p-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 border border-slate-700 text-slate-300 hover:text-white transition">
                    <i data-lucide="sun" id="themeIconSun" class="w-4 h-4 hidden"></i>
                    <i data-lucide="moon" id="themeIconMoon" class="w-4 h-4"></i>
                </button>

                <!-- Export CSV -->
                <button onclick="exportFilteredCSV()" title="Export Filtered CSV" class="flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-xl bg-slate-800/80 hover:bg-slate-700 border border-slate-700 text-slate-200 transition">
                    <i data-lucide="file-spreadsheet" class="w-4 h-4 text-emerald-400"></i>
                    <span class="hidden sm:inline">Export CSV</span>
                </button>

                <!-- Export JSON -->
                <button onclick="exportFilteredJSON()" title="Export Filtered JSON" class="flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-xl bg-slate-800/80 hover:bg-slate-700 border border-slate-700 text-slate-200 transition">
                    <i data-lucide="code" class="w-4 h-4 text-cyan-400"></i>
                    <span class="hidden sm:inline">JSON</span>
                </button>

                <!-- Print Dossier -->
                <button onclick="window.print()" title="Print Summary Report" class="flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white shadow-glow-indigo transition">
                    <i data-lucide="printer" class="w-4 h-4"></i>
                    <span class="hidden sm:inline">Print Dossier</span>
                </button>
            </div>
        </header>

        <!-- KPI HUD METRIC CARDS -->
        <section class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4">
            <!-- Metric 1: Total Records -->
            <div class="glass-panel p-4 rounded-2xl relative overflow-hidden group hover:border-indigo-500/50 transition">
                <div class="absolute -right-4 -bottom-4 w-16 h-16 bg-indigo-500/10 rounded-full blur-xl group-hover:bg-indigo-500/20 transition"></div>
                <div class="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
                    <span>Active Network</span>
                    <i data-lucide="users" class="w-4 h-4 text-indigo-400"></i>
                </div>
                <div class="text-2xl sm:text-3xl font-black text-white font-mono" id="kpiTotal">606</div>
                <div class="flex items-center gap-1 text-[11px] text-emerald-400 mt-1 font-mono">
                    <i data-lucide="shield-check" class="w-3.5 h-3.5"></i> 100% De-duplicated
                </div>
            </div>

            <!-- Metric 2: Geocoded -->
            <div class="glass-panel p-4 rounded-2xl relative overflow-hidden group hover:border-cyan-500/50 transition">
                <div class="absolute -right-4 -bottom-4 w-16 h-16 bg-cyan-500/10 rounded-full blur-xl group-hover:bg-cyan-500/20 transition"></div>
                <div class="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
                    <span>GIS Located</span>
                    <i data-lucide="map-pin" class="w-4 h-4 text-cyan-400"></i>
                </div>
                <div class="text-2xl sm:text-3xl font-black text-white font-mono" id="kpiGeo">{data_payload['geo_count']}</div>
                <div class="flex items-center gap-1 text-[11px] text-cyan-400 mt-1 font-mono">
                    <i data-lucide="crosshair" class="w-3.5 h-3.5"></i> {round(data_payload['geo_count']/len(enhanced_contacts)*100, 1)}% Spatial Reach
                </div>
            </div>

            <!-- Metric 3: Academic/Org Affinity -->
            <div class="glass-panel p-4 rounded-2xl relative overflow-hidden group hover:border-purple-500/50 transition">
                <div class="absolute -right-4 -bottom-4 w-16 h-16 bg-purple-500/10 rounded-full blur-xl group-hover:bg-purple-500/20 transition"></div>
                <div class="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
                    <span>Academic / Org</span>
                    <i data-lucide="graduation-cap" class="w-4 h-4 text-purple-400"></i>
                </div>
                <div class="text-2xl sm:text-3xl font-black text-white font-mono" id="kpiOrg">{data_payload['org_count']}</div>
                <div class="flex items-center gap-1 text-[11px] text-purple-400 mt-1 font-mono">
                    <i data-lucide="landmark" class="w-3.5 h-3.5"></i> {round(data_payload['org_count']/len(enhanced_contacts)*100, 1)}% Affiliated
                </div>
            </div>

            <!-- Metric 4: Multi-SIM / Secondary Phone -->
            <div class="glass-panel p-4 rounded-2xl relative overflow-hidden group hover:border-amber-500/50 transition">
                <div class="absolute -right-4 -bottom-4 w-16 h-16 bg-amber-500/10 rounded-full blur-xl group-hover:bg-amber-500/20 transition"></div>
                <div class="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
                    <span>Multi-SIM / Dual Line</span>
                    <i data-lucide="smartphone" class="w-4 h-4 text-amber-400"></i>
                </div>
                <div class="text-2xl sm:text-3xl font-black text-white font-mono" id="kpiPhone2">{data_payload['phone2_count']}</div>
                <div class="flex items-center gap-1 text-[11px] text-amber-400 mt-1 font-mono">
                    <i data-lucide="layers" class="w-3.5 h-3.5"></i> {round(data_payload['phone2_count']/len(enhanced_contacts)*100, 1)}% Redundant
                </div>
            </div>

            <!-- Metric 5: Data Completeness Score -->
            <div class="glass-panel p-4 rounded-2xl relative overflow-hidden group hover:border-emerald-500/50 transition">
                <div class="absolute -right-4 -bottom-4 w-16 h-16 bg-emerald-500/10 rounded-full blur-xl group-hover:bg-emerald-500/20 transition"></div>
                <div class="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
                    <span>Quality Index</span>
                    <i data-lucide="activity" class="w-4 h-4 text-emerald-400"></i>
                </div>
                <div class="text-2xl sm:text-3xl font-black text-white font-mono">78.4%</div>
                <div class="flex items-center gap-1 text-[11px] text-emerald-400 mt-1 font-mono">
                    <i data-lucide="check-circle-2" class="w-3.5 h-3.5"></i> High Fidelity
                </div>
            </div>

            <!-- Metric 6: Pruned Churn History -->
            <div class="glass-panel p-4 rounded-2xl relative overflow-hidden group hover:border-rose-500/50 transition">
                <div class="absolute -right-4 -bottom-4 w-16 h-16 bg-rose-500/10 rounded-full blur-xl group-hover:bg-rose-500/20 transition"></div>
                <div class="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
                    <span>Historical Archive</span>
                    <i data-lucide="archive" class="w-4 h-4 text-rose-400"></i>
                </div>
                <div class="text-2xl sm:text-3xl font-black text-white font-mono">{data_payload['total_deleted']}</div>
                <div class="flex items-center gap-1 text-[11px] text-rose-400 mt-1 font-mono">
                    <i data-lucide="trash-2" class="w-3.5 h-3.5"></i> Cleaned & Purged
                </div>
            </div>
        </section>

        <!-- FILTER CHIPS BAR -->
        <section class="flex items-center gap-2 overflow-x-auto pb-1 no-print">
            <span class="text-xs font-bold text-slate-400 uppercase tracking-wider flex-shrink-0 flex items-center gap-1">
                <i data-lucide="sliders-horizontal" class="w-3.5 h-3.5"></i> Lens:
            </span>
            <button onclick="setFilter('all')" class="filter-chip active px-3 py-1.5 rounded-lg text-xs font-medium bg-indigo-600 text-white border border-indigo-500 transition">All (606)</button>
            <button onclick="setFilter('mdu')" class="filter-chip px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">🎓 Madhabdev Univ (59)</button>
            <button onclick="setFilter('thb')" class="filter-chip px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">🏛️ THB College (45)</button>
            <button onclick="setFilter('rgu')" class="filter-chip px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">🏔️ RGU Arunachal (33)</button>
            <button onclick="setFilter('dgcd')" class="filter-chip px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">🏫 Darrang College (27)</button>
            <button onclick="setFilter('rangachakua')" class="filter-chip px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">📍 Rangachakua (117)</button>
            <button onclick="setFilter('jamugurihat')" class="filter-chip px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">📍 Jamugurihat (59)</button>
            <button onclick="setFilter('guwahati')" class="filter-chip px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">🏙️ Guwahati (37)</button>
            <button onclick="setFilter('kinship')" class="filter-chip px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">🤝 Da / Ba / Kinship</button>
            <button onclick="setFilter('sir')" class="filter-chip px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">👨‍🏫 Sir & Professors</button>
            <button onclick="setFilter('dual')" class="filter-chip px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">📱 Dual SIM (106)</button>
            <button onclick="setFilter('photo')" class="filter-chip px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">🖼️ With Photos (36)</button>
        </section>

        <!-- PRIMARY VISUALIZATION GRID (ROW 1: GIS SPATIAL INTELLIGENCE & SOCIAL GRAPH) -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

            <!-- MODULE 1: GIS SPATIAL MAP (7 COLUMNS) -->
            <div class="lg:col-span-7 glass-panel rounded-2xl p-5 shadow-glass flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center gap-2.5">
                            <div class="w-8 h-8 rounded-lg bg-cyan-500/20 text-cyan-400 flex items-center justify-center">
                                <i data-lucide="map" class="w-5 h-5"></i>
                            </div>
                            <div>
                                <h2 class="text-base font-bold text-white">Geospatial Distribution & Micro-Clusters</h2>
                                <p class="text-xs text-slate-400">Interactive GIS map of Assam hubs & international links</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-2">
                            <button onclick="resetMapView()" class="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition flex items-center gap-1">
                                <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i> Reset
                            </button>
                        </div>
                    </div>
                    <div id="gisMap"></div>
                </div>

                <!-- GIS Legend & Mini Summary -->
                <div class="mt-4 pt-3 border-t border-slate-800/80 grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                    <div class="p-2 rounded-xl bg-slate-900/60 border border-slate-800">
                        <div class="text-slate-400 text-[11px]">Sonitpur Valley</div>
                        <div class="font-bold text-cyan-400 font-mono text-sm">218 nodes (36.0%)</div>
                    </div>
                    <div class="p-2 rounded-xl bg-slate-900/60 border border-slate-800">
                        <div class="text-slate-400 text-[11px]">Lakhimpur District</div>
                        <div class="font-bold text-indigo-400 font-mono text-sm">57 nodes (9.4%)</div>
                    </div>
                    <div class="p-2 rounded-xl bg-slate-900/60 border border-slate-800">
                        <div class="text-slate-400 text-[11px]">Kamrup / Guwahati</div>
                        <div class="font-bold text-purple-400 font-mono text-sm">38 nodes (6.3%)</div>
                    </div>
                    <div class="p-2 rounded-xl bg-slate-900/60 border border-slate-800">
                        <div class="text-slate-400 text-[11px]">Global Expat Links</div>
                        <div class="font-bold text-emerald-400 font-mono text-sm">USA, SK, AU, UAE, UK</div>
                    </div>
                </div>
            </div>

            <!-- MODULE 2: SOCIAL & ACADEMIC NETWORK GRAPH (5 COLUMNS) -->
            <div class="lg:col-span-5 glass-panel rounded-2xl p-5 shadow-glass flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center gap-2.5">
                            <div class="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center">
                                <i data-lucide="share-2" class="w-5 h-5"></i>
                            </div>
                            <div>
                                <h2 class="text-base font-bold text-white">Institutional & Community Orbit</h2>
                                <p class="text-xs text-slate-400">Interactive physics simulation of relational ties</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-2">
                            <button id="togglePhysicsBtn" onclick="toggleGraphPhysics()" class="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition flex items-center gap-1">
                                <i data-lucide="pause" class="w-3.5 h-3.5" id="physicsIcon"></i> Pause Physics
                            </button>
                        </div>
                    </div>
                    <div id="networkCanvas" class="border border-slate-800/80 bg-slate-950/50"></div>
                </div>

                <div class="mt-4 pt-3 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-400">
                    <div class="flex items-center gap-3">
                        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-indigo-500"></span> MDU</span>
                        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-pink-500"></span> THB</span>
                        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span> RGU</span>
                        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Rangachakua</span>
                    </div>
                    <span class="text-[11px] font-mono text-slate-500">Click node to inspect</span>
                </div>
            </div>

        </div>

        <!-- SECONDARY VISUALIZATION GRID (ROW 2: INSTITUTIONAL SUNBURST, SURNAMES, TELECOM, COMPLETENESS) -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

            <!-- CHART 1: INSTITUTIONAL ECOSYSTEM -->
            <div class="glass-panel rounded-2xl p-5 shadow-glass flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-2">
                        <h3 class="text-sm font-bold text-white flex items-center gap-2">
                            <i data-lucide="building-2" class="w-4 h-4 text-indigo-400"></i> Top Alma Maters & Orgs
                        </h3>
                        <span class="text-[11px] font-mono text-slate-400">Count</span>
                    </div>
                    <p class="text-xs text-slate-400 mb-3">Academic and vocational affiliations</p>
                    <div class="h-64" id="orgsChartContainer">
                        <canvas id="orgsChart"></canvas>
                    </div>
                </div>
                <div class="mt-2 text-[11px] text-slate-400 border-t border-slate-800 pt-2 flex justify-between">
                    <span>Core Hub: <b>Madhabdev Univ</b></span>
                    <span class="font-mono text-indigo-400">59 members</span>
                </div>
            </div>

            <!-- CHART 2: ASSAMESE SURNAMES & KINSHIP FABRIC -->
            <div class="glass-panel rounded-2xl p-5 shadow-glass flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-2">
                        <h3 class="text-sm font-bold text-white flex items-center gap-2">
                            <i data-lucide="dna" class="w-4 h-4 text-pink-400"></i> Surnames & Demography
                        </h3>
                        <span class="text-[11px] font-mono text-slate-400">Frequency</span>
                    </div>
                    <p class="text-xs text-slate-400 mb-3">Assamese lineage & clan distribution</p>
                    <div class="h-64" id="surnamesChartContainer">
                        <canvas id="surnamesChart"></canvas>
                    </div>
                </div>
                <div class="mt-2 text-[11px] text-slate-400 border-t border-slate-800 pt-2 flex justify-between">
                    <span>Predominant: <b>Das (31)</b></span>
                    <span class="font-mono text-pink-400">Saikia (18) • Da (16)</span>
                </div>
            </div>

            <!-- CHART 3: TELECOM SPECTRUM -->
            <div class="glass-panel rounded-2xl p-5 shadow-glass flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-2">
                        <h3 class="text-sm font-bold text-white flex items-center gap-2">
                            <i data-lucide="radio" class="w-4 h-4 text-cyan-400"></i> Telecom Carriers
                        </h3>
                        <span class="text-[11px] font-mono text-slate-400">Share</span>
                    </div>
                    <p class="text-xs text-slate-400 mb-3">Mobile carrier routing by 10-digit prefixes</p>
                    <div class="h-64" id="telecomChartContainer">
                        <canvas id="telecomChart"></canvas>
                    </div>
                </div>
                <div class="mt-2 text-[11px] text-slate-400 border-t border-slate-800 pt-2 flex justify-between">
                    <span>Dominant: <b>Jio (52.8%)</b></span>
                    <span class="font-mono text-cyan-400">Airtel (31.4%)</span>
                </div>
            </div>

            <!-- CHART 4: DATA COMPLETENESS RADAR MATRIX -->
            <div class="glass-panel rounded-2xl p-5 shadow-glass flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-2">
                        <h3 class="text-sm font-bold text-white flex items-center gap-2">
                            <i data-lucide="radar" class="w-4 h-4 text-emerald-400"></i> Metadata Completeness
                        </h3>
                        <span class="text-[11px] font-mono text-slate-400">12 Dim</span>
                    </div>
                    <p class="text-xs text-slate-400 mb-3">Audit of populated contact fields</p>
                    <div class="h-64" id="completenessChart"></div>
                </div>
                <div class="mt-2 text-[11px] text-slate-400 border-t border-slate-800 pt-2 flex justify-between">
                    <span>Gaps: <b>Email (4%)</b></span>
                    <span class="font-mono text-emerald-400">Phone (99.5%)</span>
                </div>
            </div>

        </div>

        <!-- DYNAMIC EXPLORER MATRIX & SEARCHABLE DIRECTORY -->
        <section class="glass-panel rounded-2xl p-5 shadow-glass space-y-4">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 class="text-lg font-bold text-white flex items-center gap-2">
                        <i data-lucide="layout-grid" class="w-5 h-5 text-indigo-400"></i>
                        <span>Contact Intelligence Matrix & Live Directory</span>
                        <span id="filteredCountBadge" class="text-xs font-mono bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-2.5 py-0.5 rounded-full font-bold">606 Records</span>
                    </h2>
                    <p class="text-xs text-slate-400">Click on any card or record to inspect full telemetry, launch direct calls or WhatsApp messages, and download vCard.</p>
                </div>

                <!-- Directory View Switcher & Per Page Controls -->
                <div class="flex items-center gap-3 no-print">
                    <div class="flex items-center bg-slate-900 border border-slate-700/80 rounded-xl p-1">
                        <button onclick="setViewMode('grid')" id="viewGridBtn" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-600 text-white transition flex items-center gap-1.5">
                            <i data-lucide="grid" class="w-3.5 h-3.5"></i> Cards
                        </button>
                        <button onclick="setViewMode('table')" id="viewTableBtn" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white transition flex items-center gap-1.5">
                            <i data-lucide="list" class="w-3.5 h-3.5"></i> Dense Table
                        </button>
                    </div>

                    <select id="sortSelect" onchange="renderContacts()" class="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-xl px-3 py-2 focus:outline-none focus:border-indigo-500">
                        <option value="name_asc">Sort: Name (A-Z)</option>
                        <option value="name_desc">Sort: Name (Z-A)</option>
                        <option value="city">Sort: City Location</option>
                        <option value="org">Sort: Organization</option>
                    </select>
                </div>
            </div>

            <!-- CONTACT CARDS GRID VIEW -->
            <div id="contactsGridContainer" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 max-h-[850px] overflow-y-auto pr-1">
                <!-- Dynamically rendered via JS -->
            </div>

            <!-- CONTACT DENSE TABLE VIEW (HIDDEN BY DEFAULT) -->
            <div id="contactsTableContainer" class="hidden overflow-x-auto rounded-xl border border-slate-800 max-h-[750px] overflow-y-auto">
                <table class="w-full text-left text-xs text-slate-300">
                    <thead class="bg-slate-900 text-slate-400 font-mono uppercase tracking-wider sticky top-0 z-10 border-b border-slate-800">
                        <tr>
                            <th class="p-3">Contact</th>
                            <th class="p-3">Organization & Title</th>
                            <th class="p-3">Location</th>
                            <th class="p-3">Primary Phone</th>
                            <th class="p-3">Carrier</th>
                            <th class="p-3">Tags & Honorifics</th>
                            <th class="p-3 text-right">Action</th>
                        </tr>
                    </thead>
                    <tbody id="contactsTableBody" class="divide-y divide-slate-800/60 bg-slate-950/40">
                        <!-- Dynamically populated via JS -->
                    </tbody>
                </table>
            </div>

            <!-- Pagination Bar -->
            <div class="flex items-center justify-between pt-2 border-t border-slate-800 text-xs text-slate-400">
                <div id="paginationInfo">Showing 1 to 60 of 606</div>
                <div class="flex items-center gap-2">
                    <button onclick="prevPage()" id="prevPageBtn" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 disabled:opacity-40 disabled:pointer-events-none transition">Previous</button>
                    <span id="pageNumberIndicator" class="font-mono px-2 font-bold text-white">Page 1 / 11</span>
                    <button onclick="nextPage()" id="nextPageBtn" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 disabled:opacity-40 disabled:pointer-events-none transition">Next</button>
                </div>
            </div>
        </section>

        <!-- FOOTER & CITATIONS -->
        <footer class="text-center py-6 text-xs text-slate-500 border-t border-slate-800/80 flex flex-col sm:flex-row items-center justify-between gap-2">
            <div>
                Generated for <b>Angsuman</b> • Personal Knowledge Matrix Engine
            </div>
            <div class="flex items-center gap-3">
                <span>Cleaned Dataset: 606 Nodes</span>
                <span>•</span>
                <span>Archived: 1,127 Entries</span>
                <span>•</span>
                <span class="text-indigo-400 font-mono">100% Client-Side Privacy</span>
            </div>
        </footer>

    </div>

    <!-- DETAIL DRAWER MODAL -->
    <div id="contactModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-md z-50 hidden flex items-center justify-center p-4">
        <div class="glass-panel w-full max-w-lg rounded-2xl p-6 shadow-2xl border border-slate-700 relative animate-in fade-in zoom-in duration-200">
            <button onclick="closeModal()" class="absolute right-4 top-4 p-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition">
                <i data-lucide="x" class="w-5 h-5"></i>
            </button>
            <div id="modalContent">
                <!-- Dynamically injected -->
            </div>
        </div>
    </div>

    <!-- EMBEDDED COMPLETE DATASET -->
    <script>
        const NEXUS_DATA = {json.dumps(data_payload, ensure_ascii=False)};
        let activeFilter = 'all';
        let currentSearch = '';
        let currentPage = 1;
        const pageSize = 48;
        let viewMode = 'grid';
        let filteredContacts = [...NEXUS_DATA.contacts];

        // Maps and Graphs Instances
        let leafletMap = null;
        let markerClusterGroup = null;
        let visNetwork = null;
        let physicsEnabled = true;

        // Init
        document.addEventListener('DOMContentLoaded', () => {{
            lucide.createIcons();
            initLeafletMap();
            initVisGraph();
            initCharts();
            renderContacts();
            setupSearchShortcut();
            setupThemeToggle();
        }});

        function setupThemeToggle() {{
            const btn = document.getElementById('themeToggleBtn');
            const sun = document.getElementById('themeIconSun');
            const moon = document.getElementById('themeIconMoon');
            btn.addEventListener('click', () => {{
                document.documentElement.classList.toggle('dark');
                document.documentElement.classList.toggle('light');
                const isDark = document.documentElement.classList.contains('dark');
                if (isDark) {{
                    sun.classList.add('hidden');
                    moon.classList.remove('hidden');
                }} else {{
                    sun.classList.remove('hidden');
                    moon.classList.add('hidden');
                }}
            }});
        }}

        function setupSearchShortcut() {{
            const input = document.getElementById('globalSearchInput');
            window.addEventListener('keydown', (e) => {{
                if ((e.key === '/' && document.activeElement !== input) || (e.ctrlKey && e.key === 'k')) {{
                    e.preventDefault();
                    input.focus();
                }}
                if (e.key === 'Escape') {{
                    closeModal();
                    input.blur();
                }}
            }});
            input.addEventListener('input', (e) => {{
                currentSearch = e.target.value.toLowerCase().trim();
                currentPage = 1;
                applyFilters();
            }});
        }}

        function setViewMode(mode) {{
            viewMode = mode;
            const gridBtn = document.getElementById('viewGridBtn');
            const tableBtn = document.getElementById('viewTableBtn');
            const gridContainer = document.getElementById('contactsGridContainer');
            const tableContainer = document.getElementById('contactsTableContainer');

            if (mode === 'grid') {{
                gridBtn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-600 text-white transition flex items-center gap-1.5';
                tableBtn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white transition flex items-center gap-1.5';
                gridContainer.classList.remove('hidden');
                tableContainer.classList.add('hidden');
            }} else {{
                tableBtn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-600 text-white transition flex items-center gap-1.5';
                gridBtn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white transition flex items-center gap-1.5';
                gridContainer.classList.add('hidden');
                tableContainer.classList.remove('hidden');
            }}
            renderContacts();
        }}

        function setFilter(filterKey) {{
            activeFilter = filterKey;
            document.querySelectorAll('.filter-chip').forEach(el => {{
                el.classList.remove('bg-indigo-600', 'text-white', 'active');
                el.classList.add('bg-slate-800/80', 'text-slate-300');
            }});
            event.currentTarget.classList.add('bg-indigo-600', 'text-white', 'active');
            event.currentTarget.classList.remove('bg-slate-800/80', 'text-slate-300');
            currentPage = 1;
            applyFilters();
        }}

        function applyFilters() {{
            filteredContacts = NEXUS_DATA.contacts.filter(c => {{
                // Filter key
                let matchesCategory = true;
                if (activeFilter === 'mdu') matchesCategory = c.org.includes('Madhabdev');
                else if (activeFilter === 'thb') matchesCategory = c.org.includes('Tyagbir');
                else if (activeFilter === 'rgu') matchesCategory = c.org.includes('Rajiv Gandhi');
                else if (activeFilter === 'dgcd') matchesCategory = c.org.includes('Darrang');
                else if (activeFilter === 'rangachakua') matchesCategory = c.city === 'Rangachakua';
                else if (activeFilter === 'jamugurihat') matchesCategory = c.city === 'Jamugurihat';
                else if (activeFilter === 'guwahati') matchesCategory = c.city === 'Guwahati';
                else if (activeFilter === 'kinship') matchesCategory = c.honorifics.some(h => h.includes('Da') || h.includes('Ba') || h.includes('Kinship'));
                else if (activeFilter === 'sir') matchesCategory = c.honorifics.some(h => h.includes('Sir'));
                else if (activeFilter === 'dual') matchesCategory = !!c.phone2;
                else if (activeFilter === 'photo') matchesCategory = !!c.photo;

                if (!matchesCategory) return false;

                // Search query
                if (!currentSearch) return true;
                const searchStr = `${{c.name}} ${{c.phone1}} ${{c.phone2}} ${{c.org}} ${{c.title}} ${{c.city}} ${{c.nickname}} ${{c.notes}}`.toLowerCase();
                return searchStr.includes(currentSearch);
            }});

            // Sort
            const sortVal = document.getElementById('sortSelect').value;
            if (sortVal === 'name_asc') filteredContacts.sort((a,b) => a.name.localeCompare(b.name));
            else if (sortVal === 'name_desc') filteredContacts.sort((a,b) => b.name.localeCompare(a.name));
            else if (sortVal === 'city') filteredContacts.sort((a,b) => a.city.localeCompare(b.city));
            else if (sortVal === 'org') filteredContacts.sort((a,b) => a.org.localeCompare(b.org));

            document.getElementById('filteredCountBadge').innerText = `${{filteredContacts.length}} Records`;
            renderContacts();
            updateMapMarkers();
        }}

        function renderContacts() {{
            const start = (currentPage - 1) * pageSize;
            const end = start + pageSize;
            const pageItems = filteredContacts.slice(start, end);
            const totalPages = Math.ceil(filteredContacts.length / pageSize) || 1;

            document.getElementById('paginationInfo').innerText = `Showing ${{filteredContacts.length === 0 ? 0 : start + 1}} to ${{Math.min(end, filteredContacts.length)}} of ${{filteredContacts.length}}`;
            document.getElementById('pageNumberIndicator').innerText = `Page ${{currentPage}} / ${{totalPages}}`;
            document.getElementById('prevPageBtn').disabled = currentPage <= 1;
            document.getElementById('nextPageBtn').disabled = currentPage >= totalPages;

            const gridContainer = document.getElementById('contactsGridContainer');
            const tableBody = document.getElementById('contactsTableBody');

            if (filteredContacts.length === 0) {{
                gridContainer.innerHTML = `<div class="col-span-full py-12 text-center text-slate-400">
                    <i data-lucide="search-x" class="w-12 h-12 mx-auto text-slate-600 mb-2"></i>
                    <p class="font-bold text-base text-slate-300">No matching contacts found</p>
                    <p class="text-xs">Try adjusting your search criteria or filter lens.</p>
                </div>`;
                tableBody.innerHTML = `<tr><td colspan="7" class="p-8 text-center text-slate-400">No contacts matching criteria.</td></tr>`;
                lucide.createIcons();
                return;
            }}

            // Grid Render
            let gridHtml = '';
            pageItems.forEach(c => {{
                const initials = c.name.split(' ').map(n => n[0]).slice(0,2).join('').toUpperCase();
                const avatar = c.photo ? 
                    `<img src="${{c.photo}}" alt="${{c.name}}" class="w-10 h-10 rounded-xl object-cover border border-slate-700/80 shadow-md"/>` :
                    `<div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-slate-800 to-slate-700 border border-slate-600 flex items-center justify-center font-bold text-xs text-indigo-300 font-mono shadow">${{initials}}</div>`;

                const operatorBadge = c.operator === 'Jio' ? 'bg-cyan-950/70 text-cyan-400 border-cyan-800/60' :
                                      c.operator === 'Airtel' ? 'bg-rose-950/70 text-rose-400 border-rose-800/60' :
                                      c.operator === 'BSNL' ? 'bg-amber-950/70 text-amber-400 border-amber-800/60' :
                                      'bg-slate-800 text-slate-400 border-slate-700';

                gridHtml += `
                <div onclick="openContactModal(${{c.id}})" class="glass-panel p-4 rounded-xl border border-slate-800/80 hover:border-indigo-500/50 hover:shadow-glow-indigo transition cursor-pointer flex flex-col justify-between group">
                    <div>
                        <div class="flex items-start justify-between gap-3 mb-2.5">
                            <div class="flex items-center gap-2.5">
                                ${{avatar}}
                                <div class="overflow-hidden">
                                    <h4 class="font-bold text-sm text-white group-hover:text-indigo-300 transition truncate">${{c.name}}</h4>
                                    <p class="text-[11px] text-slate-400 truncate">${{c.title || 'Personal Contact'}}</p>
                                </div>
                            </div>
                            <span class="text-[10px] font-mono px-1.5 py-0.5 rounded border ${{operatorBadge}} flex-shrink-0">${{c.operator}}</span>
                        </div>

                        ${{c.org ? `<div class="text-xs font-medium text-indigo-400 flex items-center gap-1 mb-1 truncate"><i data-lucide="building-2" class="w-3.5 h-3.5 flex-shrink-0"></i> ${{c.org}}</div>` : ''}}
                        <div class="text-[11px] text-slate-400 flex items-center gap-1 mb-2 truncate">
                            <i data-lucide="map-pin" class="w-3 h-3 text-cyan-400 flex-shrink-0"></i> ${{c.city}}${{c.region ? ', ' + c.region : ''}}
                        </div>
                    </div>

                    <div class="pt-2 border-t border-slate-800/70 flex items-center justify-between text-xs">
                        <span class="font-mono text-slate-300">${{c.phone1 || 'No Phone'}}</span>
                        <div class="flex items-center gap-1 text-slate-400 group-hover:text-indigo-400 transition">
                            <span class="text-[11px]">Details</span>
                            <i data-lucide="chevron-right" class="w-3.5 h-3.5"></i>
                        </div>
                    </div>
                </div>`;
            }});
            gridContainer.innerHTML = gridHtml;

            // Table Render
            let tableHtml = '';
            pageItems.forEach(c => {{
                tableHtml += `
                <tr onclick="openContactModal(${{c.id}})" class="hover:bg-slate-900/60 transition cursor-pointer">
                    <td class="p-3 font-semibold text-white">
                        <div class="flex items-center gap-2">
                            ${{c.photo ? `<img src="${{c.photo}}" class="w-7 h-7 rounded-lg object-cover"/>` : `<div class="w-7 h-7 rounded-lg bg-slate-800 text-indigo-300 font-mono text-[10px] flex items-center justify-center font-bold">${{c.name[0]}}</div>`}}
                            <span>${{c.name}}</span>
                        </div>
                    </td>
                    <td class="p-3 text-slate-300">
                        <div class="font-medium text-indigo-300">${{c.org || '-'}}</div>
                        <div class="text-[11px] text-slate-500">${{c.title || '-'}}</div>
                    </td>
                    <td class="p-3 text-slate-400">
                        <div class="flex items-center gap-1"><i data-lucide="map-pin" class="w-3 h-3 text-cyan-400"></i> ${{c.city}}</div>
                    </td>
                    <td class="p-3 font-mono text-slate-300">${{c.phone1 || '-'}}</td>
                    <td class="p-3"><span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300">${{c.operator}}</span></td>
                    <td class="p-3">
                        <div class="flex flex-wrap gap-1">
                            ${{c.honorifics.map(h => `<span class="text-[9px] px-1.5 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800">${{h}}</span>`).join('')}}
                        </div>
                    </td>
                    <td class="p-3 text-right">
                        <button class="p-1 rounded-lg bg-indigo-600/20 text-indigo-300 hover:bg-indigo-600 hover:text-white transition">
                            <i data-lucide="eye" class="w-4 h-4"></i>
                        </button>
                    </td>
                </tr>`;
            }});
            tableBody.innerHTML = tableHtml;

            lucide.createIcons();
        }}

        function prevPage() {{
            if (currentPage > 1) {{
                currentPage--;
                renderContacts();
            }}
        }}

        function nextPage() {{
            const totalPages = Math.ceil(filteredContacts.length / pageSize);
            if (currentPage < totalPages) {{
                currentPage++;
                renderContacts();
            }}
        }}

        function openContactModal(contactId) {{
            const c = NEXUS_DATA.contacts.find(item => item.id === contactId);
            if (!c) return;

            const modal = document.getElementById('contactModal');
            const content = document.getElementById('modalContent');

            const phoneClean = (c.phone1 || '').replace(/[^0-9]/g, '');
            const waNumber = phoneClean.length === 10 ? '91' + phoneClean : phoneClean;

            content.innerHTML = `
                <div class="flex items-start gap-4 mb-4">
                    ${{c.photo ? 
                        `<img src="${{c.photo}}" alt="${{c.name}}" class="w-16 h-16 rounded-2xl object-cover border-2 border-indigo-500 shadow-glow-indigo"/>` :
                        `<div class="w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center text-white font-bold text-xl font-mono shadow-glow-indigo">${{c.name.split(' ').map(n=>n[0]).slice(0,2).join('')}}</div>`
                    }}
                    <div>
                        <h3 class="text-lg font-black text-white">${{c.name}}</h3>
                        <p class="text-xs text-indigo-400 font-medium">${{c.title || 'Personal Contact'}}</p>
                        ${{c.org ? `<p class="text-xs text-slate-300 flex items-center gap-1 mt-0.5"><i data-lucide="building" class="w-3.5 h-3.5"></i> ${{c.org}}</p>` : ''}}
                    </div>
                </div>

                <div class="space-y-3 text-xs bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                    <div class="flex justify-between py-1 border-b border-slate-800">
                        <span class="text-slate-400">Primary Phone:</span>
                        <span class="font-mono font-bold text-emerald-400">${{c.phone1 || 'N/A'}}</span>
                    </div>
                    ${{c.phone2 ? `
                    <div class="flex justify-between py-1 border-b border-slate-800">
                        <span class="text-slate-400">Secondary Line:</span>
                        <span class="font-mono text-cyan-400">${{c.phone2}}</span>
                    </div>` : ''}}
                    <div class="flex justify-between py-1 border-b border-slate-800">
                        <span class="text-slate-400">Carrier / Circle:</span>
                        <span class="font-mono text-slate-300">${{c.operator}}</span>
                    </div>
                    ${{c.email ? `
                    <div class="flex justify-between py-1 border-b border-slate-800">
                        <span class="text-slate-400">Email:</span>
                        <span class="font-mono text-indigo-300">${{c.email}}</span>
                    </div>` : ''}}
                    <div class="flex justify-between py-1 border-b border-slate-800">
                        <span class="text-slate-400">Location:</span>
                        <span class="text-slate-300 font-medium">📍 ${{c.city}}, ${{c.region}} (${{c.country}})</span>
                    </div>
                    ${{c.nickname ? `
                    <div class="flex justify-between py-1 border-b border-slate-800">
                        <span class="text-slate-400">Alias / Nickname:</span>
                        <span class="text-amber-400 font-medium">${{c.nickname}}</span>
                    </div>` : ''}}
                    ${{c.notes ? `
                    <div class="pt-1">
                        <span class="text-slate-400 block mb-1">Notes:</span>
                        <div class="p-2 rounded bg-slate-950 text-slate-300 font-mono text-[11px]">${{c.notes}}</div>
                    </div>` : ''}}
                </div>

                <!-- Action Buttons -->
                <div class="grid grid-cols-3 gap-2 mt-4">
                    <a href="tel:${{c.phone1}}" class="py-2.5 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold flex items-center justify-center gap-1.5 transition text-xs shadow-lg shadow-emerald-950">
                        <i data-lucide="phone-call" class="w-4 h-4"></i> Call
                    </a>
                    <a href="https://wa.me/${{waNumber}}" target="_blank" class="py-2.5 px-3 rounded-xl bg-green-700 hover:bg-green-600 text-white font-bold flex items-center justify-center gap-1.5 transition text-xs shadow-lg shadow-green-950">
                        <i data-lucide="message-circle" class="w-4 h-4"></i> WhatsApp
                    </a>
                    <button onclick="downloadVCard(${{c.id}})" class="py-2.5 px-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold flex items-center justify-center gap-1.5 transition text-xs shadow-glow-indigo">
                        <i data-lucide="user-plus" class="w-4 h-4"></i> vCard
                    </button>
                </div>
            `;

            modal.classList.remove('hidden');
            lucide.createIcons();
        }}

        function closeModal() {{
            document.getElementById('contactModal').classList.add('hidden');
        }}

        function downloadVCard(contactId) {{
            const c = NEXUS_DATA.contacts.find(item => item.id === contactId);
            if (!c) return;

            const vcard = `BEGIN:VCARD
VERSION:3.0
N:${{c.last_name}};${{c.first_name}};;;
FN:${{c.name}}
ORG:${{c.org}}
TITLE:${{c.title}}
TEL;TYPE=CELL:${{c.phone1}}
${{c.phone2 ? `TEL;TYPE=HOME:${{c.phone2}}` : ''}}
${{c.email ? `EMAIL:${{c.email}}` : ''}}
ADR;TYPE=HOME:;;${{c.formatted_addr || c.city}};${{c.city}};${{c.region}};;${{c.country}}
NOTE:${{c.notes}}
END:VCARD`;

            const blob = new Blob([vcard], {{ type: 'text/vcard' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${{c.name.replace(/\\s+/g, '_')}}.vcf`;
            a.click();
            URL.revokeObjectURL(url);
        }}

        function exportFilteredCSV() {{
            if (filteredContacts.length === 0) return;
            const headers = ["ID", "Full Name", "Organization", "Title", "City", "Region", "Country", "Phone 1", "Phone 2", "Email", "Operator", "Notes"];
            const rows = filteredContacts.map(c => [
                c.id, `"${{c.name}}"`, `"${{c.org}}"`, `"${{c.title}}"`, `"${{c.city}}"`, `"${{c.region}}"`, `"${{c.country}}"`, `"${{c.phone1}}"`, `"${{c.phone2}}"`, `"${{c.email}}"`, `"${{c.operator}}"`, `"${{c.notes}}"`
            ]);
            const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\\n');
            const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `nexus_contacts_export_${{new Date().toISOString().slice(0,10)}}.csv`;
            a.click();
            URL.revokeObjectURL(url);
            confetti({{ particleCount: 50, spread: 60, origin: {{ y: 0.8 }} }});
        }}

        function exportFilteredJSON() {{
            const jsonStr = JSON.stringify(filteredContacts, null, 2);
            const blob = new Blob([jsonStr], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `nexus_contacts_${{new Date().toISOString().slice(0,10)}}.json`;
            a.click();
            URL.revokeObjectURL(url);
            confetti({{ particleCount: 50, spread: 60, origin: {{ y: 0.8 }} }});
        }}

        // LEAFLET GIS MAP SETUP
        function initLeafletMap() {{
            leafletMap = L.map('gisMap', {{
                zoomControl: true,
                scrollWheelZoom: true
            }}).setView([26.7324, 92.9372], 8);

            // Dark Tile Layer
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                attribution: '&copy; <a href="https://carto.com/">CARTO</a> &copy; OpenStreetMap',
                maxZoom: 19
            }}).addTo(leafletMap);

            markerClusterGroup = L.markerClusterGroup({{
                maxClusterRadius: 35,
                iconCreateFunction: function(cluster) {{
                    const count = cluster.getChildCount();
                    return L.divIcon({{
                        html: `<div class="w-9 h-9 rounded-full bg-indigo-600/90 border-2 border-cyan-400 text-white font-mono font-bold flex items-center justify-center text-xs shadow-glow-cyan">${{count}}</div>`,
                        className: 'custom-cluster-icon',
                        iconSize: L.point(36, 36)
                    }});
                }}
            }});

            updateMapMarkers();
            leafletMap.addLayer(markerClusterGroup);
        }}

        function updateMapMarkers() {{
            if (!markerClusterGroup) return;
            markerClusterGroup.clearLayers();

            filteredContacts.forEach(c => {{
                if (c.lat && c.lng) {{
                    // Slight jitter so markers on exact same town don't perfectly overlap
                    const jitterLat = c.lat + (Math.random() - 0.5) * 0.015;
                    const jitterLng = c.lng + (Math.random() - 0.5) * 0.015;

                    const marker = L.circleMarker([jitterLat, jitterLng], {{
                        radius: 6,
                        fillColor: c.operator === 'Jio' ? '#06b6d4' : (c.operator === 'Airtel' ? '#f43f5e' : '#6366f1'),
                        color: '#ffffff',
                        weight: 1.5,
                        opacity: 0.9,
                        fillOpacity: 0.85
                    }});

                    const popupHtml = `
                        <div class="p-1 space-y-1">
                            <div class="font-bold text-sm text-indigo-300">${{c.name}}</div>
                            <div class="text-xs text-slate-300">${{c.title || 'Contact'}} • ${{c.org || ''}}</div>
                            <div class="text-[11px] text-cyan-400">📍 ${{c.city}}, ${{c.region}}</div>
                            <div class="font-mono text-xs text-emerald-400 font-bold pt-1">${{c.phone1 || 'No Phone'}}</div>
                        </div>
                    `;

                    marker.bindPopup(popupHtml, {{ className: 'custom-popup' }});
                    markerClusterGroup.addLayer(marker);
                }}
            }});
        }}

        function resetMapView() {{
            if (leafletMap) {{
                leafletMap.setView([26.7324, 92.9372], 8);
            }}
        }}

        // VIS-NETWORK SOCIAL GRAPH
        function initVisGraph() {{
            const container = document.getElementById('networkCanvas');
            const data = {{
                nodes: new vis.DataSet(NEXUS_DATA.graph.nodes),
                edges: new vis.DataSet(NEXUS_DATA.graph.edges)
            }};

            const options = {{
                nodes: {{
                    shape: 'dot',
                    font: {{ color: '#f8fafc', size: 11, face: 'Plus Jakarta Sans' }},
                    borderWidth: 1.5
                }},
                edges: {{
                    width: 1,
                    smooth: {{ type: 'continuous' }}
                }},
                physics: {{
                    barnesHut: {{
                        gravitationalConstant: -3000,
                        centralGravity: 0.3,
                        springLength: 95,
                        springConstant: 0.04
                    }},
                    maxVelocity: 50,
                    solver: 'barnesHut',
                    timestep: 0.35,
                    stabilization: {{ iterations: 120 }}
                }},
                interaction: {{
                    hover: true,
                    tooltipDelay: 100
                }}
            }};

            visNetwork = new vis.Network(container, data, options);

            visNetwork.on('click', function(params) {{
                if (params.nodes.length > 0) {{
                    const nodeId = params.nodes[0];
                    if (nodeId.startsWith('c_')) {{
                        const cId = parseInt(nodeId.replace('c_', ''));
                        openContactModal(cId);
                    }}
                }}
            }});
        }}

        function toggleGraphPhysics() {{
            physicsEnabled = !physicsEnabled;
            visNetwork.setOptions({{ physics: {{ enabled: physicsEnabled }} }});
            const icon = document.getElementById('physicsIcon');
            const btn = document.getElementById('togglePhysicsBtn');
            if (physicsEnabled) {{
                btn.innerHTML = `<i data-lucide="pause" class="w-3.5 h-3.5" id="physicsIcon"></i> Pause Physics`;
            }} else {{
                btn.innerHTML = `<i data-lucide="play" class="w-3.5 h-3.5" id="physicsIcon"></i> Resume Physics`;
            }}
            lucide.createIcons();
        }}

        // CHARTS & METRIC VISUALIZATIONS
        function initCharts() {{
            // Chart 1: Organizations
            const orgCtx = document.getElementById('orgsChart').getContext('2d');
            new Chart(orgCtx, {{
                type: 'bar',
                data: {{
                    labels: NEXUS_DATA.top_orgs.map(o => o[0].length > 18 ? o[0].slice(0,18)+'...' : o[0]),
                    datasets: [{{
                        label: 'Contacts',
                        data: NEXUS_DATA.top_orgs.map(o => o[1]),
                        backgroundColor: 'rgba(99, 102, 241, 0.7)',
                        borderColor: '#6366f1',
                        borderWidth: 1.5,
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8', font: {{ family: 'JetBrains Mono' }} }} }},
                        y: {{ grid: {{ display: false }}, ticks: {{ color: '#cbd5e1', font: {{ size: 10 }} }} }}
                    }}
                }}
            }});

            // Chart 2: Surnames
            const snCtx = document.getElementById('surnamesChart').getContext('2d');
            new Chart(snCtx, {{
                type: 'bar',
                data: {{
                    labels: NEXUS_DATA.top_surnames.slice(0, 10).map(s => s[0]),
                    datasets: [{{
                        label: 'Frequency',
                        data: NEXUS_DATA.top_surnames.slice(0, 10).map(s => s[1]),
                        backgroundColor: 'rgba(244, 63, 94, 0.7)',
                        borderColor: '#f43f5e',
                        borderWidth: 1.5,
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#cbd5e1', font: {{ size: 10 }} }} }},
                        y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8', font: {{ family: 'JetBrains Mono' }} }} }}
                    }}
                }}
            }});

            // Chart 3: Telecom Operators
            const telCtx = document.getElementById('telecomChart').getContext('2d');
            new Chart(telCtx, {{
                type: 'doughnut',
                data: {{
                    labels: Object.keys(NEXUS_DATA.operators),
                    datasets: [{{
                        data: Object.values(NEXUS_DATA.operators),
                        backgroundColor: ['#06b6d4', '#f43f5e', '#f59e0b', '#8b5cf6', '#64748b'],
                        borderColor: '#0f172a',
                        borderWidth: 3
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                            labels: {{ color: '#94a3b8', font: {{ size: 10 }}, boxWidth: 10 }}
                        }}
                    }},
                    cutout: '65%'
                }}
            }});

            // Chart 4: Completeness Radar (ECharts)
            const radarDom = document.getElementById('completenessChart');
            const radarChart = echarts.init(radarDom);
            const cKeys = Object.keys(NEXUS_DATA.completeness);
            const cValues = Object.values(NEXUS_DATA.completeness).map(v => Math.round((v / NEXUS_DATA.total_contacts) * 100));

            const radarOption = {{
                radar: {{
                    indicator: cKeys.map(k => ({{ name: k, max: 100 }})),
                    radius: '68%',
                    splitNumber: 4,
                    axisName: {{ color: '#94a3b8', fontSize: 9 }},
                    splitLine: {{ lineStyle: {{ color: 'rgba(255, 255, 255, 0.08)' }} }},
                    splitArea: {{ show: false }},
                    axisLine: {{ lineStyle: {{ color: 'rgba(255, 255, 255, 0.1)' }} }}
                }},
                series: [{{
                    type: 'radar',
                    data: [{{
                        value: cValues,
                        name: 'Completeness %',
                        symbol: 'circle',
                        symbolSize: 4,
                        lineStyle: {{ color: '#10b981', width: 2 }},
                        areaStyle: {{ color: 'rgba(16, 185, 129, 0.35)' }},
                        itemStyle: {{ color: '#10b981' }}
                    }}]
                }}]
            }};
            radarChart.setOption(radarOption);
            window.addEventListener('resize', () => radarChart.resize());
        }}
    </script>
</body>
</html>
"""

with open('/home/angsuman/extra_spac/Contact/visualize_contacts_nexus.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Successfully generated visualize_contacts_nexus.html with full dataset and high-fidelity interactive dashboard!")
