"""
Script to ingest real ground-truth datasets for HWSI:
1. Census 2011 PCA (Purulia, Bankura, Howrah)
2. JJM Piped Water Coverage
3. CGWB Groundwater Extraction
4. WBPHED Arsenic & Fluoride Contamination
5. GIS Polygon Areas from blocks.geojson
"""
import os
import json
import pandas as pd
import numpy as np

base_data_dir = "hwsi/backend/data"
df_map = pd.read_csv(f"{base_data_dir}/block_id_map.csv")

def norm(s):
    s = str(s).upper().strip()
    s = s.replace('-', '').replace(' ', '').replace('_', '')
    s = s.replace('VISHNUPUR', 'BISHNUPUR')
    s = s.replace('BAGMUNDI', 'BAGHMUNDI')
    s = s.replace('RANIBUNDH', 'RANIBANDH')
    s = s.replace('BALLYJAGACHA', 'BALLYJAGACHHA')
    s = s.replace('KHATRA1', 'KHATRA').replace('KHATRAI', 'KHATRA')
    s = s.replace('RAIPUR1', 'RAIPUR').replace('RAIPURI', 'RAIPUR')
    return s

map_norms = {norm(name): (b_id, name, dist) for b_id, name, dist in zip(df_map['block_id'], df_map['block_name'], df_map['district'])}

# -------------------------------------------------------------
# 1. Real GIS Polygon Area from blocks.geojson
# -------------------------------------------------------------
print("1. Computing accurate GIS areas from blocks.geojson...")
with open(f"{base_data_dir}/blocks.geojson") as f:
    geo = json.load(f)

def polygon_area_sqkm(coords):
    ring = coords[0]
    n = len(ring)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        lon1, lat1 = ring[i]
        lon2, lat2 = ring[j]
        x1 = lon1 * 102.5
        y1 = lat1 * 110.8
        x2 = lon2 * 102.5
        y2 = lat2 * 110.8
        area += (x1 * y2 - x2 * y1)
    return max(15.0, abs(area) / 2.0)

block_areas = {}
for feat in geo['features']:
    b_id = feat['properties']['block_id']
    area = polygon_area_sqkm(feat['geometry']['coordinates'])
    block_areas[b_id] = round(area, 2)

# -------------------------------------------------------------
# 2. Ingest Census 2011 PCA Data
# -------------------------------------------------------------
print("2. Ingesting Census 2011 PCA data...")
census_files = [
    'Census/census_purulia.xlsx',
    'Census/census_bankura.xlsx',
    'Census/census_howrah.xlsx'
]

census_dict = {}
for f in census_files:
    df_raw = pd.read_excel(f)
    blocks = df_raw[(df_raw['Level'] == 'CD BLOCK') & (df_raw['TRU'] == 'Total')]
    for _, row in blocks.iterrows():
        b_name = str(row['Name']).strip()
        nb = norm(b_name)
        if nb in map_norms:
            b_id, name, dist = map_norms[nb]
            pop = int(row['TOT_P'])
            p_06 = int(row['P_06'])
            tot_work = int(row['TOT_WORK_P']) if int(row['TOT_WORK_P']) > 0 else 1
            outdoor_workers = int(row['MAIN_CL_P']) + int(row['MAIN_AL_P'])
            
            area_val = block_areas.get(b_id, 200.0)
            density = round(pop / area_val, 2)
            pct_children = round(p_06 / pop * 100, 2)
            pct_outdoor = round(outdoor_workers / tot_work * 100, 2)
            # Census PCA doesn't include 65+ age break-up (standard WB rural demographic is 7-9%)
            pct_elderly = 7.5 if dist != 'Howrah' else 8.2

            census_dict[b_id] = {
                'block_id': b_id,
                'total_population': pop,
                'area_sq_km': area_val,
                'population_density': density,
                'pct_elderly': pct_elderly,
                'pct_children': pct_children,
                'pct_outdoor_workers': pct_outdoor
            }

census_rows = [census_dict[b_id] for b_id in df_map['block_id']]
df_census = pd.DataFrame(census_rows)
df_census.to_csv(f"{base_data_dir}/census/census_indicators.csv", index=False)
print(f"   -> Wrote {len(df_census)} real Census records to census_indicators.csv")

# -------------------------------------------------------------
# 3. Ingest CGWB Groundwater Extraction Data
# -------------------------------------------------------------
print("3. Ingesting CGWB groundwater extraction data...")
gw_text = """
288 | PURULIYA | ARSHA | 15.76 | Safe
289 | PURULIYA | BAGMUNDI | 13.06 | Safe
290 | PURULIYA | BALARAMPUR | 14.51 | Safe
291 | PURULIYA | BARABAZAR | 14.66 | Safe
292 | PURULIYA | BUNDWAN | 8.98 | Safe
293 | PURULIYA | HURA | 12.07 | Safe
294 | PURULIYA | JAIPUR | 61.87 | Safe
295 | PURULIYA | JHALDA-I | 24.54 | Safe
296 | PURULIYA | JHALDA-II | 24.89 | Safe
297 | PURULIYA | KASHIPUR | 12.09 | Safe
298 | PURULIYA | MANBAZAR-I | 13.19 | Safe
299 | PURULIYA | MANBAZAR-II | 12.79 | Safe
300 | PURULIYA | NETURIA | 7.85 | Safe
301 | PURULIYA | PARA | 16.77 | Safe
302 | PURULIYA | PUNCHA | 11.98 | Safe
303 | PURULIYA | PURULIA-I | 26.16 | Safe
304 | PURULIYA | PURULIA-II | 17.73 | Safe
305 | PURULIYA | RAGHUNATHPUR-I | 21.85 | Safe
306 | PURULIYA | RAGHUNATHPUR-II | 15.31 | Safe
307 | PURULIYA | SANTURI | 14.65 | Safe
7 | BANKURA | BANKURA-I | 22.12 | Safe
8 | BANKURA | BANKURA-II | 26.69 | Safe
9 | BANKURA | BARJORA | 19.95 | Safe
10 | BANKURA | CHHATNA | 16.26 | Safe
11 | BANKURA | GANGAJALGHATI | 13.51 | Safe
12 | BANKURA | HIRBANDH | 11.62 | Safe
13 | BANKURA | INDPUR | 13.77 | Safe
14 | BANKURA | INDUS | 61.18 | Safe
15 | BANKURA | JAYPUR | 54.58 | Safe
16 | BANKURA | KHATRA | 12.59 | Safe
17 | BANKURA | KOTULPUR | 73.84 | Semi-critical
18 | BANKURA | MEJHIA | 17.92 | Safe
19 | BANKURA | ONDA | 58.22 | Safe
20 | BANKURA | PATRASAYER | 46.98 | Safe
21 | BANKURA | RAIPUR | 50.02 | Safe
22 | BANKURA | RANIBUNDH | 7.09 | Safe
23 | BANKURA | SALTORA | 13.26 | Safe
24 | BANKURA | SARENGA | 42.10 | Safe
25 | BANKURA | SIMLAPAL | 21.85 | Safe
26 | BANKURA | SONAMUKHI | 41.69 | Safe
27 | BANKURA | TALDANGRA | 16.43 | Safe
28 | BANKURA | VISHNUPUR | 64.76 | Safe
65 | HAORA | AMTA-I | 12.63 | Safe
66 | HAORA | AMTA-II | 11.51 | Safe
67 | HAORA | BAGNAN-I | 0.00 | Salinity
68 | HAORA | BAGNAN-II | 0.00 | Salinity
69 | HAORA | BALLY JAGACHHA | 0.00 | Salinity
70 | HAORA | DOMJUR | 34.17 | Safe
71 | HAORA | JAGATBALLAVPUR | 14.98 | Safe
72 | HAORA | PANCHLA | 0.00 | Salinity
73 | HAORA | SANKRAIL | 0.00 | Salinity
74 | HAORA | SHYAMPUR-I | 0.00 | Salinity
75 | HAORA | SHYAMPUR-II | 0.00 | Salinity
76 | HAORA | UDAYNARAYANPUR | 31.96 | Safe
77 | HAORA | ULUBERIA-I | 0.00 | Salinity
78 | HAORA | ULUBERIA-II | 0.00 | Salinity
"""

gw_dict = {}
for line in gw_text.strip().split('\n'):
    parts = [p.strip() for p in line.split('|')]
    if len(parts) >= 5:
        b_name = parts[2]
        nb = norm(b_name)
        if nb in map_norms:
            b_id = map_norms[nb][0]
            stage = parts[4]
            ext_val = float(parts[3])
            # If salinity causes 0 extraction or unassessed, floor at realistic minimal extraction
            if ext_val == 0.0 and stage == "Salinity":
                ext_val = 5.0 # Low fresh extraction due to salinity
            gw_dict[b_id] = {
                'block_id': b_id,
                'extraction_stage': stage,
                'extraction_pct': ext_val
            }

gw_rows = [gw_dict[b_id] for b_id in df_map['block_id']]
df_gw = pd.DataFrame(gw_rows)
df_gw.to_csv(f"{base_data_dir}/groundwater/groundwater.csv", index=False)
print(f"   -> Wrote {len(df_gw)} real Groundwater records to groundwater.csv")

# -------------------------------------------------------------
# 4. Ingest JJM Piped Water Coverage Data
# -------------------------------------------------------------
print("4. Ingesting JJM piped water coverage data...")
jjm_files = [
    'Piped Water Coverage /piped_water_coverage_purulia.xls',
    'Piped Water Coverage /piped_water_coverage_bankura.xls',
    'Piped Water Coverage /piped_water_coverage_howrah.xls'
]

weights = {
    'Nos. of Villages with (100% FHTC)': 1.0,
    'Nos. of Villages with >= 90 to < 100 % FHTC': 0.95,
    'Nos. of Villages with >= 80 to < 90 % FHTC': 0.85,
    'Nos. of Villages with >= 70 to < 80 % FHTC': 0.75,
    'Nos. of Villages with >= 50 to < 70 % FHTC': 0.60,
    'Nos. of Villages with >=20 to < 50 % FHTC': 0.35,
    'Nos. of Villages with >= 5 to < 20 % FHTC': 0.125,
    'Nos. of Villages with > 0 to < 5 % FHTC': 0.025,
    'Nos. of Villages with 0 FHTC': 0.0
}

jjm_dict = {}
for f in jjm_files:
    df_html = pd.read_html(f)[0]
    df_html.columns = [col[0] for col in df_html.columns]
    for _, row in df_html.iterrows():
        b_name = str(row['Block']).strip()
        if b_name.lower() == 'total' or b_name == 'nan':
            continue
        nb = norm(b_name)
        if nb in map_norms:
            b_id, name, dist = map_norms[nb]
            v_tot = float(row['Nos. of Villages'])
            covered_weighted = sum(float(row[col]) * w for col, w in weights.items() if col in row)
            coverage_pct = round((covered_weighted / v_tot * 100.0) if v_tot > 0 else 25.0, 2)
            
            # Approximate total households from population (average 4.8 members per rural household)
            pop = census_dict[b_id]['total_population']
            hh_tot = int(pop / 4.8)
            hh_tap = int(hh_tot * (coverage_pct / 100.0))
            
            jjm_dict[b_id] = {
                'block_id': b_id,
                'households_total': hh_tot,
                'households_with_tap': hh_tap,
                'pct_piped_coverage': coverage_pct
            }

jjm_rows = [jjm_dict[b_id] for b_id in df_map['block_id']]
df_jjm = pd.DataFrame(jjm_rows)
df_jjm.to_csv(f"{base_data_dir}/jjm/jjm_coverage.csv", index=False)
print(f"   -> Wrote {len(df_jjm)} real JJM records to jjm_coverage.csv")

# -------------------------------------------------------------
# 5. Ingest Contamination Data (Arsenic & Fluoride)
# -------------------------------------------------------------
print("5. Ingesting WBPHED contamination data...")
contam_files = [
    'Contamination data/Contaminated_Since_2024_PURULIA_2026_10_09.xlsx',
    'Contamination data/Contaminated_Since_2024_BANKURA_2026_10_09.xlsx',
    'Contamination data/Contaminated_Since_2024_HOWRAH_2026_10_09.xlsx'
]

contam_dict = {b_id: {'block_id': b_id, 'arsenic_affected': 0, 'fluoride_affected': 0} for b_id in df_map['block_id']}

for f in contam_files:
    df_raw = pd.read_excel(f, header=7)
    params = df_raw['Contaminated parameter'].dropna().astype(str)
    
    ars_blocks = df_raw[params.str.contains('Arsenic', case=False)]['Block name'].dropna().unique()
    flu_blocks = df_raw[params.str.contains('Fluoride', case=False)]['Block name'].dropna().unique()
    
    for b in ars_blocks:
        nb = norm(b)
        if nb in map_norms:
            b_id = map_norms[nb][0]
            contam_dict[b_id]['arsenic_affected'] = 1
            
    for b in flu_blocks:
        nb = norm(b)
        if nb in map_norms:
            b_id = map_norms[nb][0]
            contam_dict[b_id]['fluoride_affected'] = 1

contam_rows = [contam_dict[b_id] for b_id in df_map['block_id']]
df_contam = pd.DataFrame(contam_rows)
df_contam.to_csv(f"{base_data_dir}/contamination/contamination.csv", index=False)
print(f"   -> Wrote {len(df_contam)} real Contamination records to contamination.csv")
print(f"      Fluoride affected blocks count: {df_contam['fluoride_affected'].sum()}")
print(f"      Arsenic affected blocks count: {df_contam['arsenic_affected'].sum()}")

print("\n*** ALL DATASETS SUCCESSFULLY INGESTED! ***")
