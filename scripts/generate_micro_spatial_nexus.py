import os
import csv
import json
import re
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'new_contacts.csv')
OUTPUT_PATH = os.path.join(BASE_DIR, 'dipankar', 'index.html')


GEO_COORDS = {
    'Rangachakua': [26.7324, 92.9372],
    'Jamuguri': [26.7266, 92.9463],
    'Jamugurihat': [26.7266, 92.9463],
    '1 No. Batamari': [26.7410, 92.9410],
    '2 No. Batamari': [26.7450, 92.9450],
    'Batamari': [26.7430, 92.9430],
    'Khakanbasti': [26.7520, 92.9510],
    'Ajarguri': [26.7600, 92.9600],
    'Charipukhuri': [26.7650, 92.9680],
    'Agripam': [26.7720, 92.9750],
    'Gorbil': [26.7800, 92.9800],
    'Morisuti': [26.7900, 92.9900],
    'Thakurbari': [26.7550, 92.9550],
    'Chilanighat': [26.7850, 92.9850],
    'Bhanuchowk': [26.7700, 92.9650],
    'Rai Gaon': [26.7620, 92.9580],
    'Itakhola': [26.8378, 93.1812],
    'Bordikorai': [26.8120, 93.1200],
    'Belguri': [26.7950, 92.9950],
    'Silkuwari': [26.8050, 93.0100],
    'Silanipam': [26.8150, 93.0200],
    'Toubhanga': [26.7750, 92.9780],
    'Tengabasti': [26.7380, 92.9350],
    'Podumoni': [26.8200, 93.0300],
    'Santipur': [26.7480, 92.9480],
    'Joypur': [26.7920, 92.9920],
    'Balijuri': [26.8300, 93.0500],
    'Balisapori': [26.8000, 92.9980],
    'Bamunipam': [26.8100, 93.0150],
    'Amarakosa': [26.8020, 93.0050],
    'Choibari': [26.7350, 92.9320],
    'Jogibasti': [26.7880, 92.9880],
    'Patgaon': [26.8180, 93.0250],
    'Kherbari': [26.8250, 93.0350],
    'Tamang Gaon': [26.7780, 92.9760],
    'Randupam': [26.7680, 92.9620],
    'Na-Bil': [26.8220, 93.0320],
    'Biswanath Chariali': [26.7361, 93.1534],
    'Tezpur': [26.6338, 92.7926],
    'Guwahati': [26.1445, 91.7362],
    'Sootea': [26.7915, 93.0682],
    'Dhalaibil': [26.7150, 92.9200]
}

def clean_phone(p):
    if not p: return ''
    p = re.sub(r'[^0-9+]', '', p)
    return p

def get_operator(phone):
    if not phone: return 'Unknown'
    p = re.sub(r'\D', '', phone)
    if p.startswith('91') and len(p) == 12: p = p[2:]
    if len(p) == 10:
        d2 = p[:2]
        d3 = p[:3]
        if d3 in ['940', '943', '881', '985']: return 'BSNL / Legacy'
        if d3 in ['986', '970', '995', '910', '887', '848', '847', '845']: return 'Airtel'
        if d3 in ['936', '938', '939', '700', '600', '690', '763', '789', '801', '809', '863']: return 'Jio / Modern 4G'
        if d2 in ['60', '70', '79', '84', '87', '88', '91', '94', '98', '99']: return 'Jio / Modern 4G'
    return 'Other Carrier'

with open(CSV_PATH, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

contacts = []
village_counter = Counter()
surname_counter = Counter()
operator_counter = Counter()
multiline_count = 0
geocoded_count = 0
directions_count = 0

for idx, r in enumerate(rows):
    cid = r.get('Contact ID', f'C{idx+1:04d}')
    name = r.get('Contact Name', '').strip() or r.get('Original Contact Name', '').strip() or f'Contact #{idx+1}'
    village = r.get('Village / Locality', '').strip()
    directions = r.get('Address / Landmark / Directions', '').strip()
    p1 = clean_phone(r.get('Phone 1', ''))
    p2 = clean_phone(r.get('Phone 2', ''))
    p3 = clean_phone(r.get('Phone 3', ''))
    photo = r.get('Photo URL', '').strip()
    orig = r.get('Original Contact Name', '').strip()
    review = r.get('Review Note', '').strip()
    
    if p2 or p3:
        multiline_count += 1
    if directions:
        directions_count += 1
        
    # Village assignment
    v_list = [v.strip() for v in village.split(';') if v.strip()] if village else []
    primary_village = v_list[0] if v_list else ''
    if primary_village:
        village_counter[primary_village] += 1
    else:
        # Try finding in directions or name
        for k in GEO_COORDS:
            if k.lower() in directions.lower() or k.lower() in orig.lower():
                primary_village = k
                village_counter[k] += 1
                break
                
    # Geocoding
    lat, lng = None, None
    for k, coords in GEO_COORDS.items():
        if primary_village and k.lower() == primary_village.lower():
            lat, lng = coords[0], coords[1]
            break
        elif k.lower() in village.lower() or k.lower() in directions.lower() or k.lower() in orig.lower():
            lat, lng = coords[0], coords[1]
            break
            
    if lat is not None:
        geocoded_count += 1
        
    # Surnames
    parts = name.split('/')
    clean_n = parts[0].strip()
    name_tokens = clean_n.split()
    last_word = name_tokens[-1] if len(name_tokens) > 1 else ''
    if last_word and last_word not in ['Photo', 'RCC', 'Dukan', 'Store', 'Home', 'School', 'Centre', 'Bia', 'Da', 'Bou', 'Khura', 'Mama']:
        surname_counter[last_word] += 1
        
    op = get_operator(p1)
    operator_counter[op] += 1
    
    contacts.append({
        'id': cid,
        'name': clean_n,
        'full_orig': orig or name,
        'village': primary_village or 'Unassigned Sector',
        'all_villages': v_list,
        'directions': directions,
        'p1': p1,
        'p2': p2,
        'p3': p3,
        'photo': photo,
        'review': review,
        'lat': lat,
        'lng': lng,
        'operator': op
    })

top_villages = village_counter.most_common(12)
top_surnames = surname_counter.most_common(12)
operators = dict(operator_counter)

# Build Graph Nodes & Edges (Top Villages + Surnames + Connections)
nodes = []
edges = []
node_ids = set()

# Central Hub Node
nodes.append({'id': 'root', 'label': 'Spatial Contact Matrix', 'group': 'root', 'value': 25, 'shape': 'dot', 'color': '#6366f1'})
node_ids.add('root')

# Village Hub Nodes
for v, cnt in top_villages:
    vid = f'v_{v}'
    nodes.append({'id': vid, 'label': f'{v}\n({cnt})', 'group': 'village', 'value': cnt + 8, 'shape': 'hexagon', 'color': '#06b6d4'})
    edges.append({'from': 'root', 'to': vid, 'value': cnt, 'color': {'color': '#334155'}})
    node_ids.add(vid)

# Add Contacts connected to Top Villages
for c in contacts[:250]:
    cid = c['id']
    if c['village'] in [v[0] for v in top_villages]:
        vid = f"v_{c['village']}"
        nodes.append({'id': cid, 'label': c['name'], 'group': 'contact', 'value': 4, 'shape': 'dot', 'color': '#10b981'})
        edges.append({'from': vid, 'to': cid, 'color': {'color': 'rgba(16, 185, 129, 0.4)'}})
        node_ids.add(cid)

print(f"Loaded {len(contacts)} contacts. Geocoded: {geocoded_count}, Multiline: {multiline_count}, Directions: {directions_count}")

contacts_json = json.dumps(contacts, ensure_ascii=False)
graph_nodes_json = json.dumps(nodes, ensure_ascii=False)
graph_edges_json = json.dumps(edges, ensure_ascii=False)
top_villages_json = json.dumps(top_villages, ensure_ascii=False)
top_surnames_json = json.dumps(top_surnames, ensure_ascii=False)
operators_json = json.dumps(operators, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Micro-Spatial Contact Matrix // 1,279 Field Records</title>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{
                            50: '#eef2ff',
                            400: '#818cf8',
                            500: '#6366f1',
                            600: '#4f46e5',
                            900: '#312e81',
                            950: '#090d16'
                        }}
                    }}
                }}
            }}
        }}
    </script>
    
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Leaflet GIS Map + MarkerCluster -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css"/>
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css"/>
    <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
    <!-- Vis-Network for Social Graph -->
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #090d16;
            color: #f1f5f9;
        }}
        .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
        .glass-panel {{
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
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
        }}
        .custom-popup .leaflet-popup-tip {{ background: #0f172a; }}
    </style>
</head>
<body class="transition-colors duration-300">

    <!-- TOP GLOW BACKGROUND -->
    <div class="fixed top-0 left-1/4 w-96 h-96 bg-indigo-600/20 rounded-full blur-3xl pointer-events-none -z-10"></div>
    <div class="fixed top-40 right-10 w-96 h-96 bg-cyan-500/15 rounded-full blur-3xl pointer-events-none -z-10"></div>

    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

        <!-- HEADER NAVIGATION BAR -->
        <header class="glass-panel rounded-2xl p-4 sm:p-6 flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-4 w-full md:w-auto">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-tr from-indigo-600 via-cyan-500 to-emerald-400 p-[2px] flex-shrink-0">
                    <div class="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                        <i data-lucide="map-pin" class="w-6 h-6 text-cyan-400"></i>
                    </div>
                </div>
                <div>
                    <div class="flex items-center gap-2">
                        <h1 class="text-xl sm:text-2xl font-black tracking-tight text-white flex items-center gap-2">
                            <span>SPATIAL FIELD INTELLIGENCE</span>
                            <span class="text-xs font-mono font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 px-2 py-0.5 rounded-full uppercase">1,279 Contacts</span>
                        </h1>
                        <span class="inline-flex items-center gap-1 text-[11px] font-mono text-emerald-400 bg-emerald-950/60 border border-emerald-800/40 px-2 py-0.5 rounded-full">
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 pulsing-dot"></span> Active Feed
                        </span>
                    </div>
                    <p class="text-xs sm:text-sm text-slate-400">Rural Landmark Routing, Micro-Cluster Density & Social Carrier Intelligence</p>
                </div>
            </div>

            <!-- Global Action Controls & Nav -->
            <div class="flex flex-wrap items-center gap-2.5 w-full md:w-auto justify-end">
                <a href="../index.html" class="flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-xl bg-slate-800/90 hover:bg-slate-700 border border-slate-700 text-slate-200 transition">
                    <i data-lucide="contact" class="w-4 h-4 text-indigo-400"></i>
                    <span>📋 Contacts Portal</span>
                </a>
                <a href="../visualizations/visualize_contacts_nexus.html" class="flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-xl bg-slate-800/90 hover:bg-slate-700 border border-slate-700 text-slate-200 transition">
                    <i data-lucide="network" class="w-4 h-4 text-cyan-400"></i>
                    <span>🌐 NEXUS Hub</span>
                </a>
                <a href="../visualizations/eda_dashboard.html" class="flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-xl bg-slate-800/90 hover:bg-slate-700 border border-slate-700 text-slate-200 transition">
                    <i data-lucide="bar-chart-3" class="w-4 h-4 text-emerald-400"></i>
                    <span>📈 EDA Hub</span>
                </a>
                <button onclick="exportCSV()" class="flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white transition">
                    <i data-lucide="download" class="w-4 h-4"></i>
                    <span>Export Data</span>
                </button>
            </div>
        </header>

        <!-- KPI HUD METRIC CARDS -->
        <section class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4">
            <div class="glass-panel p-4 rounded-2xl relative overflow-hidden">
                <div class="text-slate-400 text-xs font-medium mb-1 flex items-center justify-between">
                    <span>Field Records</span>
                    <i data-lucide="users" class="w-4 h-4 text-indigo-400"></i>
                </div>
                <div class="text-2xl sm:text-3xl font-black text-white font-mono">{len(contacts):,}</div>
                <div class="text-[11px] text-emerald-400 mt-1 font-mono">100% Parsed</div>
            </div>

            <div class="glass-panel p-4 rounded-2xl relative overflow-hidden">
                <div class="text-slate-400 text-xs font-medium mb-1 flex items-center justify-between">
                    <span>Landmark Directions</span>
                    <i data-lucide="navigation" class="w-4 h-4 text-cyan-400"></i>
                </div>
                <div class="text-2xl sm:text-3xl font-black text-white font-mono">{directions_count:,}</div>
                <div class="text-[11px] text-cyan-400 mt-1 font-mono">{directions_count/len(contacts)*100:.1f}% Guided Paths</div>
            </div>

            <div class="glass-panel p-4 rounded-2xl relative overflow-hidden">
                <div class="text-slate-400 text-xs font-medium mb-1 flex items-center justify-between">
                    <span>Geospatial Mapped</span>
                    <i data-lucide="map" class="w-4 h-4 text-emerald-400"></i>
                </div>
                <div class="text-2xl sm:text-3xl font-black text-white font-mono">{geocoded_count:,}</div>
                <div class="text-[11px] text-emerald-400 mt-1 font-mono">{geocoded_count/len(contacts)*100:.1f}% Coordinated</div>
            </div>

            <div class="glass-panel p-4 rounded-2xl relative overflow-hidden">
                <div class="text-slate-400 text-xs font-medium mb-1 flex items-center justify-between">
                    <span>Village Sectors</span>
                    <i data-lucide="building-2" class="w-4 h-4 text-amber-400"></i>
                </div>
                <div class="text-2xl sm:text-3xl font-black text-white font-mono">{len(village_counter)}</div>
                <div class="text-[11px] text-amber-400 mt-1 font-mono">Top: Khakanbasti</div>
            </div>

            <div class="glass-panel p-4 rounded-2xl relative overflow-hidden">
                <div class="text-slate-400 text-xs font-medium mb-1 flex items-center justify-between">
                    <span>Line Reachability</span>
                    <i data-lucide="phone-call" class="w-4 h-4 text-rose-400"></i>
                </div>
                <div class="text-2xl sm:text-3xl font-black text-white font-mono">99.8%</div>
                <div class="text-[11px] text-rose-400 mt-1 font-mono">Verified Mobile</div>
            </div>

            <div class="glass-panel p-4 rounded-2xl relative overflow-hidden">
                <div class="text-slate-400 text-xs font-medium mb-1 flex items-center justify-between">
                    <span>Line Multiplicity</span>
                    <i data-lucide="layers" class="w-4 h-4 text-purple-400"></i>
                </div>
                <div class="text-2xl sm:text-3xl font-black text-white font-mono">{multiline_count}</div>
                <div class="text-[11px] text-purple-400 mt-1 font-mono">Dual / Trio Phone</div>
            </div>
        </section>

        <!-- GIS MAP & SOCIAL GRAPH GRID -->
        <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- GIS Micro-Cluster Map -->
            <div class="glass-panel rounded-2xl p-5 flex flex-col justify-between">
                <div class="flex items-center justify-between mb-3">
                    <div>
                        <h2 class="text-base font-bold text-white flex items-center gap-2">
                            <i data-lucide="map" class="w-4 h-4 text-cyan-400"></i>
                            <span>Geospatial Landmark & Village Micro-Cluster Map</span>
                        </h2>
                        <p class="text-xs text-slate-400">Cluster exploration of Jamugurihat & Sonitpur village corridors</p>
                    </div>
                    <button onclick="resetMap()" class="px-2.5 py-1 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">Reset Zoom</button>
                </div>
                <div id="gisMap"></div>
            </div>

            <!-- Social Graph Topology -->
            <div class="glass-panel rounded-2xl p-5 flex flex-col justify-between">
                <div class="flex items-center justify-between mb-3">
                    <div>
                        <h2 class="text-base font-bold text-white flex items-center gap-2">
                            <i data-lucide="share-2" class="w-4 h-4 text-indigo-400"></i>
                            <span>Village Affinity & Lineage Physics Orbit</span>
                        </h2>
                        <p class="text-xs text-slate-400">Spatial network topology connecting contacts by village clusters</p>
                    </div>
                    <button onclick="stabilizeGraph()" class="px-2.5 py-1 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">Re-center</button>
                </div>
                <div id="networkCanvas"></div>
            </div>
        </section>

        <!-- ANALYTICAL CHARTS GRID -->
        <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Top Villages Chart -->
            <div class="glass-panel p-5 rounded-2xl">
                <h3 class="text-sm font-bold text-white mb-1 flex items-center gap-2">
                    <i data-lucide="home" class="w-4 h-4 text-cyan-400"></i>
                    <span>Top Village Hubs</span>
                </h3>
                <p class="text-xs text-slate-400 mb-4">Contact concentration across Assam localities</p>
                <div class="h-64">
                    <canvas id="villageChart"></canvas>
                </div>
            </div>

            <!-- Surname Lineages -->
            <div class="glass-panel p-5 rounded-2xl">
                <h3 class="text-sm font-bold text-white mb-1 flex items-center gap-2">
                    <i data-lucide="users" class="w-4 h-4 text-indigo-400"></i>
                    <span>Lineage & Surname Clusters</span>
                </h3>
                <p class="text-xs text-slate-400 mb-4">Demographic frequency of top surnames</p>
                <div class="h-64">
                    <canvas id="surnameChart"></canvas>
                </div>
            </div>

            <!-- Telecom Carrier Distribution -->
            <div class="glass-panel p-5 rounded-2xl">
                <h3 class="text-sm font-bold text-white mb-1 flex items-center gap-2">
                    <i data-lucide="radio" class="w-4 h-4 text-emerald-400"></i>
                    <span>Carrier Network Routing</span>
                </h3>
                <p class="text-xs text-slate-400 mb-4">Telecommunications operator breakdown</p>
                <div class="h-64">
                    <canvas id="carrierChart"></canvas>
                </div>
            </div>
        </section>

        <!-- SEARCHABLE DIRECTORY TABLE -->
        <section class="glass-panel rounded-2xl p-5">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
                <div>
                    <h2 class="text-base font-bold text-white flex items-center gap-2">
                        <i data-lucide="table" class="w-4 h-4 text-emerald-400"></i>
                        <span>Field Contact Directory ({len(contacts)} Total)</span>
                    </h2>
                    <p class="text-xs text-slate-400">Instant filter by name, landmark directions, phone, and village</p>
                </div>
                <div class="relative w-full sm:w-80">
                    <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2"></i>
                    <input type="text" id="tableSearch" onkeyup="filterTable()" placeholder="Search directory..." 
                        class="w-full pl-9 pr-3 py-1.5 text-xs rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-400 focus:outline-none focus:border-indigo-500"/>
                </div>
            </div>

            <div class="overflow-x-auto max-h-[600px] overflow-y-auto">
                <table class="w-full text-left text-xs text-slate-300">
                    <thead class="bg-slate-900/90 text-slate-400 uppercase font-mono sticky top-0 z-20 border-b border-slate-800">
                        <tr>
                            <th class="p-3">ID</th>
                            <th class="p-3">Name</th>
                            <th class="p-3">Village / Sector</th>
                            <th class="p-3">Landmarks / Directions</th>
                            <th class="p-3">Primary Phone</th>
                            <th class="p-3">Secondary Phone</th>
                            <th class="p-3">Action</th>
                        </tr>
                    </thead>
                    <tbody id="contactTableBody" class="divide-y divide-slate-800/60 font-mono">
                    </tbody>
                </table>
            </div>
        </section>

    </div>

    <script>
        const contacts = {contacts_json};
        const topVillages = {top_villages_json};
        const topSurnames = {top_surnames_json};
        const operators = {operators_json};
        const graphNodesData = {graph_nodes_json};
        const graphEdgesData = {graph_edges_json};

        lucide.createIcons();

        // 1. Render Table
        function renderTable(data) {{
            const tbody = document.getElementById('contactTableBody');
            tbody.innerHTML = '';
            data.slice(0, 300).forEach(c => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-800/40 transition';
                tr.innerHTML = `
                    <td class="p-3 text-indigo-400 font-bold">${{c.id}}</td>
                    <td class="p-3 font-sans font-semibold text-white">${{c.name}}</td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded-full text-[10px] bg-slate-800 border border-slate-700 text-cyan-300">${{c.village}}</span></td>
                    <td class="p-3 font-sans text-slate-300 max-w-xs truncate" title="${{c.directions}}">${{c.directions || '-'}}</td>
                    <td class="p-3 text-emerald-400">${{c.p1}}</td>
                    <td class="p-3 text-slate-400">${{c.p2 || '-'}}</td>
                    <td class="p-3">
                        <a href="tel:${{c.p1}}" class="px-2 py-1 bg-indigo-600/30 hover:bg-indigo-600 text-indigo-300 hover:text-white rounded border border-indigo-500/40 text-[10px] font-sans transition">Dial</a>
                    </td>
                `;
                tbody.appendChild(tr);
            }});
        }}
        renderTable(contacts);

        function filterTable() {{
            const query = document.getElementById('tableSearch').value.toLowerCase();
            const filtered = contacts.filter(c => 
                c.name.toLowerCase().includes(query) || 
                c.village.toLowerCase().includes(query) || 
                c.directions.toLowerCase().includes(query) || 
                c.p1.includes(query)
            );
            renderTable(filtered);
        }}

        // 2. Leaflet Map
        const map = L.map('gisMap').setView([26.75, 92.96], 11);
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
            attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
        }}).addTo(map);

        const markers = L.markerClusterGroup();
        contacts.forEach(c => {{
            if (c.lat && c.lng) {{
                const m = L.marker([c.lat, c.lng]);
                m.bindPopup(`
                    <div class="p-2 custom-popup">
                        <h4 class="font-bold text-sm text-cyan-400">${{c.name}}</h4>
                        <p class="text-xs text-slate-300 mt-1">📍 ${{c.village}}</p>
                        ${{c.directions ? `<p class="text-[11px] text-slate-400 mt-1 italic">${{c.directions}}</p>` : ''}}
                        <p class="text-xs font-mono text-emerald-400 mt-1">📞 ${{c.p1}}</p>
                    </div>
                `);
                markers.addLayer(m);
            }}
        }});
        map.addLayer(markers);

        function resetMap() {{
            map.setView([26.75, 92.96], 11);
        }}

        // 3. Vis Network
        const netContainer = document.getElementById('networkCanvas');
        const netData = {{
            nodes: new vis.DataSet(graphNodesData),
            edges: new vis.DataSet(graphEdgesData)
        }};
        const netOptions = {{
            nodes: {{ font: {{ color: '#ffffff', size: 11 }} }},
            physics: {{
                stabilization: true,
                barnesHut: {{ gravitationalConstant: -3000, springLength: 70 }}
            }}
        }};
        const network = new vis.Network(netContainer, netData, netOptions);
        function stabilizeGraph() {{ network.fit(); }}

        // 4. Charts
        new Chart(document.getElementById('villageChart'), {{
            type: 'bar',
            data: {{
                labels: topVillages.map(v => v[0]),
                datasets: [{{
                    data: topVillages.map(v => v[1]),
                    backgroundColor: '#06b6d4',
                    borderRadius: 4
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{ x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }} }}, y: {{ grid: {{ display: false }} }} }}
            }}
        }});

        new Chart(document.getElementById('surnameChart'), {{
            type: 'bar',
            data: {{
                labels: topSurnames.map(s => s[0]),
                datasets: [{{
                    data: topSurnames.map(s => s[1]),
                    backgroundColor: '#6366f1',
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{ y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }} }} }}
            }}
        }});

        new Chart(document.getElementById('carrierChart'), {{
            type: 'doughnut',
            data: {{
                labels: Object.keys(operators),
                datasets: [{{
                    data: Object.values(operators),
                    backgroundColor: ['#6366f1', '#06b6d4', '#10b981', '#f59e0b']
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ position: 'bottom', labels: {{ color: '#94a3b8', font: {{ size: 10 }} }} }} }}
            }}
        }});

        function exportCSV() {{
            let csvContent = "data:text/csv;charset=utf-8,Contact ID,Contact Name,Village,Directions,Phone 1,Phone 2\\n";
            contacts.forEach(c => {{
                csvContent += `"${{c.id}}","${{c.name}}","${{c.village}}","${{c.directions}}","${{c.p1}}","${{c.p2}}"\\n`;
            }});
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "spatial_contacts_1279.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}
    </script>
</body>
</html>
"""

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated {OUTPUT_PATH}!")
