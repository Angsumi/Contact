# 🗂️ Contact Network Vault (Obsidian Knowledge Graph)

A fully structured, bi-directionally linked personal contact and social network Obsidian vault. Converts unstructured contacts into an interconnected web of people, academic institutions, workplaces, geographic clusters, and kinship circles.

---

## 🏛️ Vault Architecture

```text
Contact_Network_Vault/
├── 00 🌐 Contacts & Social Network Master Index.md
├── People/             # Individual markdown dossiers with YAML frontmatter
├── Organizations/      # Universities, colleges, companies, and organizations
├── Districts/          # Administrative districts (Sonitpur, Lakhimpur, Kamrup, etc.)
├── Locations/          # Specific towns and geographic centroids
├── Circles & Roles/    # Kinship (Da, Ba, Sir), academic tiers, and peer groups
├── .obsidian/          # Obsidian workspace, graph physics, and appearance presets
├── contacts.csv        # Underlying canonical contact data
└── generate_network.py # Network generation and bi-directional linking script
```

---

## 🔍 How to Use in Obsidian

1. Launch **Obsidian**.
2. Click **Open another vault** (vault switcher in the lower-left corner).
3. Select **`Contact_Network_Vault`**.
4. Open the **Graph View** (`Ctrl + G`) to explore the visual interconnected network of relationships and communities.

---

## 🔄 Automated Regeneration
To update or re-generate all markdown notes from updated contact CSVs:
```bash
python3 generate_network.py
```
