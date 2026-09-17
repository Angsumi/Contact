# 🌐 Contact Intelligence & Geospatial Analytics Matrix

A privacy-focused, high-performance personal contact intelligence and spatial analytics dashboard. Transforms raw contact archives into interactive knowledge graphs, geospatial density maps, and exploratory visualizations.

🚀 **Live Deployment (GitHub Pages)**:
- 📋 **Original Contacts Hub (606 Records)**:
  - 📋 **Contacts Manager (Main Portal)**: [https://angsumi.online/Contact/](https://angsumi.online/Contact/)
  - 🌐 **NEXUS Visualizer**: [https://angsumi.online/Contact/visualizations/visualize_contacts_nexus.html](https://angsumi.online/Contact/visualizations/visualize_contacts_nexus.html)
  - 📈 **EDA Analytics Hub**: [https://angsumi.online/Contact/visualizations/eda_dashboard.html](https://angsumi.online/Contact/visualizations/eda_dashboard.html)
- 📍 **Dipankar Suite (1,279 Field Records - `/dipankar`)**:
  - 📍 **Dipankar Field Matrix**: [https://angsumi.online/Contact/dipankar/](https://angsumi.online/Contact/dipankar/)
  - 🌐 **Dipankar NEXUS Visualizer**: [https://angsumi.online/Contact/dipankar/visualize_nexus.html](https://angsumi.online/Contact/dipankar/visualize_nexus.html)
  - 📈 **Dipankar EDA Dashboard**: [https://angsumi.online/Contact/dipankar/eda_dashboard.html](https://angsumi.online/Contact/dipankar/eda_dashboard.html)

---

## 🔗 Inter-Dashboard Cross Navigation
All portals include integrated top navigation bars enabling instant switching between views:
- **From Original Portals (`/` & `/visualizations/`)**: Cross-links to Contacts Manager, NEXUS Visualizer, EDA Hub, and the Dipankar Field Suite.
- **From Dipankar Suite (`/dipankar/`)**: Dedicated internal navigation between **Dipankar Matrix** (`index.html`), **Dipankar NEXUS** (`visualize_nexus.html`), **Dipankar EDA** (`eda_dashboard.html`), plus a return link to the Original Contacts Hub (`../index.html`).

## 📁 Repository Structure

The repository is modularly organized into distinct folders:

```text
Contact/
├── index.html                   # Main entry point & interactive contacts manager (606 records)
├── template.html                # Base template for generating index.html
├── README.md                    # Project documentation
│
├── dipankar/                    # Dedicated folder for the 1,279 field contacts suite
│   ├── index.html               # Dipankar Field Matrix dashboard (accessible at /dipankar)
│   ├── visualize_nexus.html     # Dedicated Dipankar NEXUS Graph & GIS Map
│   └── eda_dashboard.html       # Dedicated Dipankar EDA & Demographics Visualizer
│
├── data/                        # Datasets and archives
│   ├── new_contacts.csv         # New 1,279 field-verified contacts dataset
│   ├── contacts.csv             # Cleaned & de-duplicated contacts dataset (606 records)
│   ├── contacts.csv.bak         # Dataset backup
│   └── dleted_contact.csv       # Archived deleted / merged records
│
├── visualizations/              # Standalone interactive visualization dashboards (606 records)
│   ├── visualize_contacts_nexus.html  # NEXUS Intelligence & Spatial Graph (606 Records)
│   └── eda_dashboard.html       # Multi-Disciplinary Exploratory Visualizations (606 Records)
│
├── scripts/                     # Python ETL pipelines & development servers
│   ├── generate_dipankar_suite.py # Generator for complete /dipankar suite
│   ├── generate_nexus_dashboard.py # Generator for original NEXUS dashboard
│   ├── build_index.py           # Injects CSV data into template to build index.html
│   ├── build_visualizer.py      # Spatial ETL & metadata enricher
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

- **Dipankar Field Matrix (`/dipankar`)**:
  - **1,279 Contact Field Analytics**: Landmark-level address parsing with 1,060 explicit landmark routes.
  - **Geospatial Village Micro-Clustering**: Leaflet GIS map with interactive pin-clustering covering Khakanbasti, Ajarguri, Charipukhuri, Agripam, Gorbil, Rangachakua, Morisuti, Batamari, and surrounding sectors.
  - **Physics Social Graph**: Vis-Network graph mapping contacts directly to their village clusters.
  - **Demographic & Telecom Intelligence**: Assamese surname distribution and mobile operator routing.
  - **Instant Live Search & Dialer**: Searchable directory with click-to-dial functionality and CSV export.
- **Contacts Manager (`index.html`)**:
  - Live search, multi-select category filters, vCard export, and contact editor.
  - Built-in analytics tabs and quick navigation to specialized dashboards.
- **NEXUS Visualizer (`visualizations/visualize_contacts_nexus.html`)**:
  - Executive KPI HUD, multi-dimensional relational social orbit, and 12-dimensional metadata radar.
- **EDA Hub (`visualizations/eda_dashboard.html`)**:
  - 8 high-resolution analytical visual reports and spatial survey route inspections.
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

