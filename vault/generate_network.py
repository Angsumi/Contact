import csv
import os
import re
import json
from collections import defaultdict

VAULT_DIR = os.path.dirname(os.path.abspath(__file__))
PEOPLE_DIR = os.path.join(VAULT_DIR, 'People')
ORGS_DIR = os.path.join(VAULT_DIR, 'Organizations')
ROLES_DIR = os.path.join(VAULT_DIR, 'Circles & Roles')
DISTRICTS_DIR = os.path.join(VAULT_DIR, 'Districts')
LOCS_DIR = os.path.join(VAULT_DIR, 'Locations')
OBSIDIAN_DIR = os.path.join(VAULT_DIR, '.obsidian')

# Clean out old notes
for d in [PEOPLE_DIR, ORGS_DIR, ROLES_DIR, DISTRICTS_DIR, LOCS_DIR, OBSIDIAN_DIR]:
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        if f.endswith('.md'):
            os.remove(os.path.join(d, f))

# Look for contacts.csv in the vault directory or parent
CSV_PATH = os.path.join(VAULT_DIR, 'contacts.csv')
if not os.path.exists(CSV_PATH):
    CSV_PATH = '/home/angsuman/extra_spac/Contact/contacts.csv'

with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

def clean_filename(name):
    name = re.sub(r'[/\\:*?"<>|#^\[\]]', '', name).strip()
    return name if name else 'Unnamed'

def split_items(s):
    if not s: return []
    parts = re.split(r'[,;]+', s)
    return [p.strip() for p in parts if p.strip()]

def slugify_tag(s):
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s.lower()).strip('-')
    return s

seen_filenames = {}
people_data = []

org_to_people = defaultdict(list)
role_to_people = defaultdict(list)
district_to_people = defaultdict(list)
city_to_people = defaultdict(list)
street_to_people = defaultdict(list)

# Hierarchy mapping: Location -> District
loc_to_district = defaultdict(set)
street_to_city = defaultdict(set)

for r in rows:
    raw_name = (r.get('First Name', '') + ' ' + r.get('Middle Name', '') + ' ' + r.get('Last Name', '')).strip()
    if not raw_name:
        raw_name = r.get('Organization Name', '').strip() or r.get('Phone 1 - Value', '').strip() or 'Contact'
    
    base_name = clean_filename(raw_name)
    if base_name not in seen_filenames:
        seen_filenames[base_name] = 1
        note_title = base_name
    else:
        seen_filenames[base_name] += 1
        p_val = r.get('Phone 1 - Value', '').replace(' ', '')
        suffix = p_val[-4:] if len(p_val) >= 4 else str(seen_filenames[base_name])
        note_title = f"{base_name} ({suffix})"

    orgs = [clean_filename(o) for o in split_items(r.get('Organization Name', '')) if o.strip()]
    roles = [clean_filename(t) for t in split_items(r.get('Organization Title', '')) if t.strip()]
    cities = [clean_filename(c) for c in split_items(r.get('Address 1 - City', '')) if c.strip()]
    streets = [clean_filename(s) for s in split_items(r.get('Address 1 - Street', '')) if s.strip()]
    regions = [clean_filename(reg) for reg in split_items(r.get('Address 1 - Region', '')) if reg.strip()]
    country = clean_filename(r.get('Address 1 - Country', '').strip()) or 'India'
    phone1 = r.get('Phone 1 - Value', '').strip()
    phone2 = r.get('Phone 2 - Value', '').strip()
    email = r.get('E-mail 1 - Value', '').strip()
    notes = r.get('Notes', '').strip()

    district_tags = [f"district/{slugify_tag(reg)}" for reg in regions if reg]

    person = {
        'title': note_title,
        'name': raw_name,
        'orgs': orgs,
        'roles': roles,
        'cities': cities,
        'streets': streets,
        'regions': regions,
        'district_tags': district_tags,
        'country': country,
        'phone1': phone1,
        'phone2': phone2,
        'email': email,
        'notes': notes,
    }
    people_data.append(person)

    for o in orgs: org_to_people[o].append(person)
    for ro in roles: role_to_people[ro].append(person)
    for reg in regions: district_to_people[reg].append(person)
    for c in cities:
        city_to_people[c].append(person)
        for reg in regions:
            loc_to_district[c].add(reg)
    for s in streets:
        street_to_people[s].append(person)
        for c in cities:
            street_to_city[s].add(c)

# 1. Write Individual Person Notes
for p in people_data:
    tags = ['contact', 'person']
    for ro in p['roles']:
        tag_val = slugify_tag(ro)
        if tag_val: tags.append(f"role/{tag_val}")
    for dt in p['district_tags']:
        tags.append(dt)
    
    org_links = [f"[[{o}]]" for o in p['orgs']]
    role_links = [f"[[{ro}]]" for ro in p['roles']]
    city_links = [f"[[{c}]]" for c in p['cities']]
    street_links = [f"[[{s}]]" for s in p['streets']]
    region_links = [f"[[{reg}]]" for reg in p['regions']]

    tag_yaml = '\n'.join([f"  - {t}" for t in tags])
    overview_roles = ', '.join(role_links) if role_links else '—'
    overview_orgs = ', '.join(org_links) if org_links else '—'
    all_locs = street_links + city_links + region_links
    overview_loc = ', '.join(all_locs) if all_locs else '—'
    phone1_val = p['phone1'] or '—'
    phone2_val = f"- **Secondary Phone**: `{p['phone2']}`\n" if p['phone2'] else ""
    email_val = f"- **Email**: {p['email']}\n" if p['email'] else ""
    notes_block = f"### 📝 Notes\n> [!note]\n> {p['notes']}\n\n" if p['notes'] else ""

    content = f"""---
title: "{p['title']}"
tags:
{tag_yaml}
type: contact
districts: {p['regions']}
phone: "{p['phone1']}"
email: "{p['email']}"
---

# 👤 {p['title']}

### 📌 Overview
- **Roles / Relationship**: {overview_roles}
- **Organizations**: {overview_orgs}
- **District / Region**: {', '.join(region_links) if region_links else '—'}
- **Location**: {overview_loc}

### 📞 Contact Details
- **Primary Phone**: `{phone1_val}`
{phone2_val}{email_val}
{notes_block}---
*Part of [[00 🌐 Contacts & Social Network Master Index|Contacts & Social Network Master Index]]*
"""
    note_path = os.path.join(PEOPLE_DIR, f"{p['title']}.md")
    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 2. Write Organization Hub Notes
for org_name, members in org_to_people.items():
    member_list = ""
    for m in sorted(members, key=lambda x: x['title']):
        role_str = f" (*{', '.join(m['roles'])}*)" if m['roles'] else ""
        loc_str = f" — {', '.join(m['cities'])}" if m['cities'] else ""
        member_list += f"- [[{m['title']}]] {role_str}{loc_str}\n"

    content = f"""---
title: "{org_name}"
tags:
  - organization
  - network-hub
type: organization
member_count: {len(members)}
---

# 🏢 {org_name}

> [!info] Organization Hub
> Connected to **{len(members)}** contacts in your network.

### 👥 Associated People
{member_list}
---
*Back to [[00 🌐 Contacts & Social Network Master Index]]*
"""
    org_path = os.path.join(ORGS_DIR, f"{org_name}.md")
    with open(org_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 3. Write Role / Circle Hub Notes
for role_name, members in role_to_people.items():
    member_list = ""
    for m in sorted(members, key=lambda x: x['title']):
        org_str = f" — {', '.join(m['orgs'])}" if m['orgs'] else ""
        loc_str = f" (*{', '.join(m['cities'])}*)" if m['cities'] else ""
        member_list += f"- [[{m['title']}]] {org_str}{loc_str}\n"

    content = f"""---
title: "{role_name}"
tags:
  - circle
  - role-hub
type: role
member_count: {len(members)}
---

# 🏷️ {role_name}

> [!info] Circle Hub
> **{len(members)}** contacts with the relationship/role **{role_name}**.

### 👥 People in this Circle
{member_list}
---
*Back to [[00 🌐 Contacts & Social Network Master Index]]*
"""
    role_path = os.path.join(ROLES_DIR, f"{role_name}.md")
    with open(role_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 4. Write District Hub Notes
for district_name, members in district_to_people.items():
    cities_in_dist = [c for c, dists in loc_to_district.items() if district_name in dists]
    city_links = [f"[[{c}]]" for c in cities_in_dist]

    member_list = ""
    for m in sorted(members, key=lambda x: x['title']):
        org_str = f" — {', '.join(m['orgs'])}" if m['orgs'] else ""
        role_str = f" (*{', '.join(m['roles'])}*)" if m['roles'] else ""
        member_list += f"- [[{m['title']}]] {role_str}{org_str}\n"

    content = f"""---
title: "{district_name}"
tags:
  - district
  - geo-hub
  - district/{slugify_tag(district_name)}
type: district
contact_count: {len(members)}
---

# 🗺️ District: {district_name}

> [!info] District Hub
> **{len(members)}** contacts and **{len(cities_in_dist)}** towns connected to **{district_name}**.

### 📍 Towns & Cities in {district_name}
{', '.join(city_links) if city_links else '—'}

### 👥 People in {district_name}
{member_list}
---
*Back to [[00 🌐 Contacts & Social Network Master Index]]*
"""
    dist_path = os.path.join(DISTRICTS_DIR, f"{district_name}.md")
    with open(dist_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 5. Write Location & Village Notes
for city_name, residents in city_to_people.items():
    dist_links = [f"[[{d}]]" for d in loc_to_district[city_name]]
    resident_list = ""
    for r in sorted(residents, key=lambda x: x['title']):
        org_str = f" — {', '.join(r['orgs'])}" if r['orgs'] else ""
        role_str = f" (*{', '.join(r['roles'])}*)" if r['roles'] else ""
        resident_list += f"- [[{r['title']}]] {role_str}{org_str}\n"

    content = f"""---
title: "{city_name}"
tags:
  - location
  - city
type: location
contact_count: {len(residents)}
---

# 📍 {city_name}

> [!info] Location Hub
> **{len(residents)}** contacts connected to **{city_name}** {f'in {", ".join(dist_links)}' if dist_links else ''}.

### 🗺️ District / Region
{', '.join(dist_links) if dist_links else '—'}

### 👥 People Connected to {city_name}
{resident_list}
---
*Back to [[00 🌐 Contacts & Social Network Master Index]]*
"""
    city_path = os.path.join(LOCS_DIR, f"{city_name}.md")
    with open(city_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Also create notes for villages / streets
for street_name, residents in street_to_people.items():
    if street_name in city_to_people or street_name in district_to_people:
        continue
    c_links = [f"[[{c}]]" for c in street_to_city[street_name]]
    resident_list = ""
    for r in sorted(residents, key=lambda x: x['title']):
        org_str = f" — {', '.join(r['orgs'])}" if r['orgs'] else ""
        role_str = f" (*{', '.join(r['roles'])}*)" if r['roles'] else ""
        resident_list += f"- [[{r['title']}]] {role_str}{org_str}\n"

    content = f"""---
title: "{street_name}"
tags:
  - location
  - village
type: village
contact_count: {len(residents)}
---

# 🏡 {street_name}

> [!info] Village / Area
> **{len(residents)}** contacts in **{street_name}** {f'({", ".join(c_links)})' if c_links else ''}.

### 👥 Residents & Contacts
{resident_list}
---
*Back to [[00 🌐 Contacts & Social Network Master Index]]*
"""
    street_path = os.path.join(LOCS_DIR, f"{street_name}.md")
    with open(street_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 6. Master Index MOC
top_orgs = sorted(org_to_people.items(), key=lambda x: -len(x[1]))[:15]
top_cities = sorted(city_to_people.items(), key=lambda x: -len(x[1]))[:15]
top_roles = sorted(role_to_people.items(), key=lambda x: -len(x[1]))[:15]
top_districts = sorted(district_to_people.items(), key=lambda x: -len(x[1]))[:15]

org_moc = "".join([f"- [[{org_name}]] — **{len(members)}** contacts\n" for org_name, members in top_orgs])
city_moc = "".join([f"- [[{city_name}]] — **{len(residents)}** contacts\n" for city_name, residents in top_cities])
role_moc = "".join([f"- [[{role_name}]] — **{len(members)}** contacts\n" for role_name, members in top_roles])
dist_moc = "".join([f"- [[{dist_name}]] — **{len(members)}** contacts\n" for dist_name, members in top_districts])

moc_content = f"""---
title: "Contacts & Social Network Master Index"
tags:
  - second-brain
  - index
  - moc
  - contacts
---

# 🌐 Contacts & Social Network Master Graph

Welcome to your standalone, self-contained **Personal Relationship & Professional Social Graph**.

> [!tip] Graph View Controls (`Ctrl + G`)
> - Nodes are **colorized by District / Region** (Blue for Sonitpur, Green for Lakhimpur, Amber for Biswanath, Purple for Kamrup, etc.).
> - **Gold Nodes** are Organization Hubs (Universities, Colleges, Companies).
> - **Magenta Nodes** are Geo Hubs (Districts, Cities, Villages).
> - **Cyan Nodes** are Relationship Circles (Classmates, Scholars, Colleagues).

---

### 📊 Network Summary
- 👤 **People**: **{len(people_data)}**
- 🏢 **Organizations**: **{len(org_to_people)}**
- 🏷️ **Circles & Roles**: **{len(role_to_people)}**
- 🗺️ **Districts**: **{len(district_to_people)}**
- 📍 **Towns & Villages**: **{len(city_to_people) + len(street_to_people)}**

---

### 🗺️ Geographic Districts
{dist_moc}
---

### 🏢 Key Organization Hubs (Universities, Colleges, Offices)
{org_moc}
---

### 🏷️ Key Relationship Circles
{role_moc}
---

### 📍 Key Towns & Cities
{city_moc}
"""

moc_path = os.path.join(VAULT_DIR, "00 🌐 Contacts & Social Network Master Index.md")
with open(moc_path, 'w', encoding='utf-8') as f:
    f.write(moc_content)

# 7. Enhanced graph.json color groups and physics
DISTRICT_COLORS = {
    'sonitpur': {'name': 'Sonitpur', 'rgb': 3900150},          # Vibrant Blue
    'lakhimpur': {'name': 'Lakhimpur', 'rgb': 1096065},        # Emerald Green
    'biswanath': {'name': 'Biswanath', 'rgb': 16096779},       # Warm Amber
    'kamrup-metro': {'name': 'Kamrup Metro', 'rgb': 9133302},    # Purple
    'dhemaji': {'name': 'Dhemaji', 'rgb': 15485081},           # Pink
    'jorhat': {'name': 'Jorhat', 'rgb': 439956},               # Cyan
    'nagaon': {'name': 'Nagaon', 'rgb': 16347926},             # Orange
    'sivasagar': {'name': 'Sivasagar', 'rgb': 14753096},       # Crimson
    'arunachal-pradesh': {'name': 'Arunachal Pradesh', 'rgb': 1357990}, # Teal
    'udalguri': {'name': 'Udalguri', 'rgb': 8696854},          # Lime
    'dibrugarh': {'name': 'Dibrugarh', 'rgb': 6514417},        # Indigo
    'karbi-anglong': {'name': 'Karbi Anglong', 'rgb': 11032055}, # Violet
    'golaghat': {'name': 'Golaghat', 'rgb': 15381256},         # Yellow
    'tinsukia': {'name': 'Tinsukia', 'rgb': 165063},           # Sky Blue
    'majuli': {'name': 'Majuli', 'rgb': 2278750},             # Bright Green
    'barpeta': {'name': 'Barpeta', 'rgb': 16007006},           # Rose
    'darrang': {'name': 'Darrang', 'rgb': 14251782},           # Ochre
    'assam': {'name': 'Assam General', 'rgb': 6583435}         # Slate
}

color_groups = []
# District Color Rules
for slug, info in DISTRICT_COLORS.items():
    color_groups.append({
        'query': f"tag:#district/{slug}",
        'color': {'a': 1, 'rgb': info['rgb']}
    })

# Hub Type Rules
color_groups.append({'query': 'path:Organizations', 'color': {'a': 1, 'rgb': 16766720}})      # Gold (#ffd700)
color_groups.append({'query': 'path:Districts', 'color': {'a': 1, 'rgb': 16711935}})          # Magenta (#ff00ff)
color_groups.append({'query': 'path:Locations', 'color': {'a': 1, 'rgb': 16744703}})          # Light Pink/Coral
color_groups.append({'query': 'path:"Circles & Roles"', 'color': {'a': 1, 'rgb': 32767}})    # Neon Cyan (#00ffff)

graph_config = {
    "collapse-filter": False,
    "search": "",
    "showTags": False,
    "showAttachments": False,
    "hideUnresolved": False,
    "showOrphans": True,
    "collapse-color-groups": False,
    "colorGroups": color_groups,
    "collapse-display": False,
    "showArrow": True,
    "textFadeMultiplier": 0,
    "nodeSizeMultiplier": 1.35,
    "lineSizeMultiplier": 1.1,
    "collapse-forces": False,
    "centerStrength": 0.48,
    "repelStrength": 16,
    "linkStrength": 1,
    "linkDistance": 45,
    "scale": 0.22,
    "close": False
}

with open(os.path.join(OBSIDIAN_DIR, 'graph.json'), 'w', encoding='utf-8') as f:
    json.dump(graph_config, f, indent=2)

print(f"Independent Graph generation complete! People: {len(people_data)}, Orgs: {len(org_to_people)}, Districts: {len(district_to_people)}, Roles: {len(role_to_people)}, Locations: {len(city_to_people) + len(street_to_people)}")
