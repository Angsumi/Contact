# 🌐 Contact Intelligence & Geospatial Analytics Matrix

A privacy-focused, high-performance personal contact intelligence and spatial analytics dashboard. Transforms raw contact archives into interactive knowledge graphs, geospatial density maps, and exploratory visualizations.

🚀 **Live Deployment (GitHub Pages)**:
- 📋 **Contacts Manager (Main)**: [https://angsumi.online/Contact/](https://angsumi.online/Contact/)
- 🌐 **NEXUS Visualizer**: [https://angsumi.online/Contact/visualizations/visualize_contacts_nexus.html](https://angsumi.online/Contact/visualizations/visualize_contacts_nexus.html)
- 📈 **EDA Analytics Hub**: [https://angsumi.online/Contact/visualizations/eda_dashboard.html](https://angsumi.online/Contact/visualizations/eda_dashboard.html)

---

## 🔗 Inter-Dashboard Cross Navigation
All portals include integrated top navigation bars enabling instant switching between views:
- From **Contacts Manager**: Click the header buttons `📊 Analytics`, `🌐 NEXUS Visualizer`, or `📈 EDA Hub`.
- From **NEXUS Visualizer**: Click `📋 Contacts` or `📈 EDA Hub` directly in the top action bar.
- From **EDA Analytics Hub**: Click `📋 Contacts Manager` or `🌐 NEXUS Visualizer` in the sticky header.


## 📁 Repository Structure

The repository is modularly organized into distinct folders:

```text
Contact/
├── index.html                   # Main entry point & interactive contacts manager
├── template.html                # Base template for generating index.html
├── README.md                    # Project documentation
│
├── data/                        # Datasets and archives
│   ├── contacts.csv             # Cleaned & de-duplicated contacts dataset
│   ├── contacts.csv.bak         # Dataset backup
│   └── dleted_contact.csv       # Archived deleted / merged records
│
├── visualizations/              # Standalone interactive visualization dashboards
│   ├── visualize_contacts_nexus.html  # NEXUS Intelligence & Spatial Graph
│   └── eda_dashboard.html       # 9 Multi-Disciplinary Exploratory Visualizations
│
├── scripts/                     # Python ETL pipelines & development servers
│   ├── build_index.py           # Injects CSV data into template to build index.html
│   ├── build_visualizer.py      # Spatial ETL & metadata enricher
│   ├── generate_nexus_dashboard.py # Generator for NEXUS dashboard
│   └── server.py                # Local development server with CSV saveback API
│
└── assets/                      # Generated visualization graphics and maps
    ├── eda_01_organizations_hierarchy.png
    ├── eda_02_geographic_distribution.png
    ├── eda_03_telecom_distribution.png
    ├── eda_04_roles_and_taxonomy.png
    ├── eda_05_data_completeness_audit.png
    ├── eda_06_gis_house_survey_map.png
    ├── eda_07_surnames_distribution.png
    └── eda_08_positions_and_professions.png
```

---

## 🚀 Key Features

- **Contacts Manager (`index.html`)**:
  - Live search, multi-select category filters, vCard export, and contact editor.
  - Built-in analytics tabs and quick navigation to specialized dashboards.
- **NEXUS Visualizer (`visualizations/visualize_contacts_nexus.html`)**:
  - **Executive KPI HUD**: Active nodes, spatial footprint, institutional affinity, dual-line penetration.
  - **Interactive GIS Map (Leaflet.js + MarkerCluster)**: Assam Brahmaputra Valley micro-clustering (Sonitpur, Lakhimpur, Kamrup, Biswanath) with international links (USA, Slovakia, Australia, UAE, UK).
  - **Relational Social Orbit (Vis-Network)**: Physics-based graph network connecting contacts by universities, organizations, hometowns, and kinship tags.
  - **Demographic & Telecom Intelligence**: Assamese surname frequency distribution, clan clustering, and 10-digit carrier routing (Jio, Airtel, Vi, BSNL).
  - **12-Dimensional Metadata Completeness Radar (ECharts)**: Multi-axis completeness audit across all fields.
- **EDA Hub (`visualizations/eda_dashboard.html`)**:
  - 8 high-resolution analytical visual reports and spatial survey route inspections.

---

## 🛠️ Getting Started & Local Development

### 1. Run Local Server
```bash
python3 scripts/server.py
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

### 2. Rebuild HTML Builds
```bash
# Rebuild main index.html
python3 scripts/build_index.py

# Rebuild NEXUS visualizer
python3 scripts/generate_nexus_dashboard.py
```

---

## 🔒 Privacy & Security
All processing, visualization rendering, and analytics occur 100% client-side in your local browser environment.

