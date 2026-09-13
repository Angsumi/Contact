# 🌐 Contact Intelligence & Geospatial Analytics Matrix

A privacy-focused, high-performance personal contact intelligence and spatial analytics dashboard. Transforms raw contact archives into interactive knowledge graphs, geospatial density maps, and exploratory visualizations.

---

## 🚀 Key Features

- **NEXUS Visualizer (`visualize_contacts_nexus.html`)**:
  - **Executive KPI HUD**: Active nodes, spatial footprint, institutional affinity, dual-line penetration, and quality metrics.
  - **Interactive GIS Map (Leaflet.js + MarkerCluster)**: Assam Brahmaputra Valley micro-clustering (Sonitpur, Lakhimpur, Kamrup, Biswanath) with international links (USA, Slovakia, Australia, UAE, UK).
  - **Relational Social Orbit (Vis-Network)**: Physics-based graph network connecting contacts by universities, organizations, hometowns, and kinship tags.
  - **Demographic & Telecom Intelligence**: Assamese surname frequency distribution, clan clustering, and 10-digit carrier routing (Jio, Airtel, Vi, BSNL).
  - **12-Dimensional Metadata Completeness Radar (ECharts)**: Multi-axis completeness audit across all fields.
  - **Live Search & Filter Directory**: Instant `/` hotkey search, quick filter pills, glass card view, and dense enterprise table.
  - **Direct Actions**: Instant phone dialer, WhatsApp chat launcher (`wa.me`), and `.vcf` vCard generation.

- **Data Processing Pipeline**:
  - `build_visualizer.py` & `generate_nexus_dashboard.py`: Python ETL scripts for data cleansing, geocoding, kinship tagging, and carrier extraction.
  - `server.py`: Local lightweight HTTP server for testing and live updates.

---

## 🛠️ Getting Started

### 1. View Visualizer Locally
Open `visualize_contacts_nexus.html` directly in any web browser:
```bash
xdg-open visualize_contacts_nexus.html
```

### 2. Run Local Server
```bash
python3 server.py
```
Visit `http://localhost:8000/visualize_contacts_nexus.html` in your browser.

---

## 🔒 Privacy & Security
All processing, visualization rendering, and analytics occur 100% client-side in your local environment.
