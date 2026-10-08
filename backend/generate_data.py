import os
import json
import random
import pandas as pd
import numpy as np

base_dir = "data"
os.makedirs(base_dir, exist_ok=True)
os.makedirs(f"{base_dir}/census", exist_ok=True)
os.makedirs(f"{base_dir}/groundwater", exist_ok=True)
os.makedirs(f"{base_dir}/jjm", exist_ok=True)
os.makedirs(f"{base_dir}/contamination", exist_ok=True)
os.makedirs(f"{base_dir}/health", exist_ok=True)
os.makedirs(f"{base_dir}/mock", exist_ok=True)

# 2a. block_id_map.csv
pur_blocks = ["Arsha", "Baghmundi", "Balarampur", "Barabazar", "Bundwan", "Hura", "Jaipur", "Jhalda-I", "Jhalda-II", "Kashipur", "Manbazar-I", "Manbazar-II", "Neturia", "Para", "Puncha", "Purulia-I", "Purulia-II", "Raghunathpur-I", "Raghunathpur-II", "Santuri"]
ban_blocks = ["Bankura-I", "Bankura-II", "Barjora", "Bishnupur", "Chhatna", "Gangajalghati", "Hirbandh", "Indpur", "Indus", "Jaypur", "Khatra", "Kotulpur", "Mejhia", "Onda", "Patrasayer", "Raipur", "Ranibandh", "Saltora", "Sarenga", "Simlapal", "Sonamukhi", "Taldangra"]
how_blocks = ["Amta-I", "Amta-II", "Bagnan-I", "Bagnan-II", "Domjur", "Jagatballavpur", "Panchla", "Sankrail", "Shyampur-I", "Shyampur-II", "Udaynarayanpur", "Uluberia-I", "Uluberia-II", "Bally-Jagachha"]

data = []
for i, b in enumerate(pur_blocks):
    data.append({"block_id": f"PUR_{i+1:02d}", "block_name": b, "district": "Purulia", "state": "West Bengal"})
for i, b in enumerate(ban_blocks):
    data.append({"block_id": f"BAN_{i+1:02d}", "block_name": b, "district": "Bankura", "state": "West Bengal"})
for i, b in enumerate(how_blocks):
    data.append({"block_id": f"HOW_{i+1:02d}", "block_name": b, "district": "Howrah", "state": "West Bengal"})

df_map = pd.DataFrame(data)
df_map.to_csv(f"{base_dir}/block_id_map.csv", index=False)

# 2b. census_indicators.csv
census_data = []
for _, row in df_map.iterrows():
    if row['district'] in ["Purulia", "Bankura"]:
        pop = random.randint(100000, 250000)
        area = random.uniform(150, 350)
        outdoor = random.uniform(40, 60)
    else:
        pop = random.randint(200000, 400000)
        area = random.uniform(50, 150)
        outdoor = random.uniform(15, 30)
    
    census_data.append({
        "block_id": row['block_id'],
        "total_population": pop,
        "area_sq_km": area,
        "population_density": pop / area,
        "pct_elderly": random.uniform(6, 10),
        "pct_children": random.uniform(10, 15),
        "pct_outdoor_workers": outdoor
    })
pd.DataFrame(census_data).to_csv(f"{base_dir}/census/census_indicators.csv", index=False)

# 2c. groundwater.csv
gw_data = []
for _, row in df_map.iterrows():
    if row['district'] == "Purulia":
        stage = random.choices(["Safe", "Semi-Critical"], weights=[0.8, 0.2])[0]
        ext = random.uniform(40, 75)
    elif row['district'] == "Bankura":
        stage = random.choices(["Safe", "Semi-Critical"], weights=[0.5, 0.5])[0]
        ext = random.uniform(60, 85)
    else:
        stage = random.choices(["Safe", "Semi-Critical", "Critical"], weights=[0.3, 0.5, 0.2])[0]
        ext = random.uniform(70, 95)
    gw_data.append({
        "block_id": row['block_id'],
        "extraction_stage": stage,
        "extraction_pct": ext
    })
pd.DataFrame(gw_data).to_csv(f"{base_dir}/groundwater/groundwater.csv", index=False)

# 2d. jjm_coverage.csv
jjm_data = []
for _, row in df_map.iterrows():
    hh = random.randint(20000, 80000)
    if row['district'] == "Purulia":
        pct = random.uniform(30, 55)
    elif row['district'] == "Bankura":
        pct = random.uniform(40, 65)
    else:
        pct = random.uniform(60, 85)
    jjm_data.append({
        "block_id": row['block_id'],
        "households_total": hh,
        "households_with_tap": int(hh * pct / 100),
        "pct_piped_coverage": pct
    })
pd.DataFrame(jjm_data).to_csv(f"{base_dir}/jjm/jjm_coverage.csv", index=False)

# 2e. contamination.csv
contam_data = []
for _, row in df_map.iterrows():
    if row['district'] == "Howrah":
        ars = random.choices([0, 1], weights=[0.7, 0.3])[0]
        flu = 0
    else:
        ars = 0
        flu = random.choices([0, 1], weights=[0.6, 0.4])[0]
    contam_data.append({
        "block_id": row['block_id'],
        "arsenic_affected": ars,
        "fluoride_affected": flu
    })
pd.DataFrame(contam_data).to_csv(f"{base_dir}/contamination/contamination.csv", index=False)

# 2f. health_capacity.csv
health_data = []
for _, row in df_map.iterrows():
    if row['district'] in ["Purulia", "Bankura"]:
        beds = random.uniform(0.3, 0.8)
    else:
        beds = random.uniform(0.8, 1.5)
    pop_row = next(r for r in census_data if r['block_id'] == row['block_id'])
    pop = pop_row['total_population']
    health_data.append({
        "block_id": row['block_id'],
        "health_facilities": random.randint(2, 10),
        "hospital_beds": int(beds * pop / 1000),
        "beds_per_1000": beds,
        "data_quality": "MOCK"
    })
pd.DataFrame(health_data).to_csv(f"{base_dir}/health/health_capacity.csv", index=False)

# 2g. resource_inventory.csv
res_data = []
for _, row in df_map.iterrows():
    res_data.append({
        "block_id": row['block_id'],
        "available_tankers": random.randint(0, 3),
        "available_cooling_units": random.randint(0, 2),
        "available_ors_packets": random.randint(500, 2000)
    })
pd.DataFrame(res_data).to_csv(f"{base_dir}/mock/resource_inventory.csv", index=False)

# 2h. blocks.geojson
geojson = {"type": "FeatureCollection", "features": []}

def make_polygon(lon, lat, size=0.05):
    return [
        [lon, lat],
        [lon+size, lat],
        [lon+size, lat+size],
        [lon, lat+size],
        [lon, lat]
    ]

districts = {
    "Purulia": {"lon": 85.6, "lat": 23.1, "cols": 5},
    "Bankura": {"lon": 86.5, "lat": 22.6, "cols": 6},
    "Howrah": {"lon": 87.8, "lat": 22.3, "cols": 4}
}
counters = {"Purulia": 0, "Bankura": 0, "Howrah": 0}

for _, row in df_map.iterrows():
    d = row['district']
    c = counters[d]
    col = c % districts[d]["cols"]
    r = c // districts[d]["cols"]
    
    lon = districts[d]["lon"] + col * 0.06
    lat = districts[d]["lat"] + r * 0.06
    
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [make_polygon(lon, lat)]
        },
        "properties": {
            "block_id": row['block_id'],
            "block_name": row['block_name'],
            "district": row['district']
        }
    }
    geojson["features"].append(feature)
    counters[d] += 1

# with open(f"{base_dir}/blocks.geojson", "w") as f:
#     json.dump(geojson, f)
# NOTE: blocks.geojson is now real Census 2011 data. Do not regenerate it.
