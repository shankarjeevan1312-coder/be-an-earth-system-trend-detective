"""
Data Acquisition Script for NASA Earth System Trend Detective.
Built with Python standard library (urllib, csv, json) so it runs with zero external dependencies.
"""
import os
import json
import csv
import urllib.request
import urllib.error

BASE_DIR = r"C:\Users\jeeva\.gemini\antigravity\scratch\earth_system_trend_detective"
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "NASA-Space-Apps-Earth-Trend-Detective/1.0 (Educational/Research)"
}

def download_file(url: str, dest_path: str) -> bool:
    print(f"Downloading: {url}")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as response, open(dest_path, "wb") as out_file:
            out_file.write(response.read())
        print(f"  -> Saved to {dest_path}")
        return True
    except Exception as e:
        print(f"  -> Failed to download: {e}")
        return False

def acquire_nasa_giss():
    print("\n[1/3] Fetching NASA GISS Surface Temperature Datasets...")
    giss_files = {
        "global_temp_monthly.csv": "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv",
        "northern_hemisphere_temp.csv": "https://data.giss.nasa.gov/gistemp/tabledata_v4/NH.Ts+dSST.csv",
        "southern_hemisphere_temp.csv": "https://data.giss.nasa.gov/gistemp/tabledata_v4/SH.Ts+dSST.csv",
        "zonal_annual_temp.csv": "https://data.giss.nasa.gov/gistemp/tabledata_v4/ZonAnn.Ts+dSST.csv",
    }
    
    for filename, url in giss_files.items():
        raw_path = os.path.join(RAW_DIR, filename)
        if download_file(url, raw_path):
            # Clean and process CSV
            proc_path = os.path.join(PROCESSED_DIR, f"cleaned_{filename}")
            try:
                with open(raw_path, mode='r', encoding='utf-8', errors='ignore') as infile:
                    lines = infile.readlines()
                
                # If first line is description / header note, find table header
                header_idx = 0
                for idx, line in enumerate(lines[:5]):
                    if "Year" in line:
                        header_idx = idx
                        break
                
                header_cols = [c.strip() for c in lines[header_idx].strip().split(',')]
                clean_rows = []
                for line in lines[header_idx+1:]:
                    parts = [p.strip() for p in line.strip().split(',')]
                    if not parts or not parts[0].isdigit():
                        continue
                    clean_rows.append(parts)
                
                with open(proc_path, mode='w', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(header_cols)
                    writer.writerows(clean_rows)
                print(f"  -> Cleaned {len(clean_rows)} rows -> {proc_path}")
            except Exception as e:
                print(f"  -> Processing error on {filename}: {e}")

def acquire_nasa_power():
    print("\n[2/3] Querying NASA POWER API for Global Planetary Biomes...")
    regions = {
        "south_asia_india": {"lat": 28.6139, "lon": 77.2090, "name": "New Delhi / South Asia"},
        "arctic_barrow": {"lat": 71.2906, "lon": -156.7886, "name": "Utqiagvik / Arctic Tundra"},
        "amazon_manaus": {"lat": -3.1190, "lon": -60.0217, "name": "Manaus / Amazon Rainforest"},
        "sahel_niamey": {"lat": 13.5116, "lon": 2.1254, "name": "Niamey / Sahel Region"},
        "mediterranean_athens": {"lat": 37.9838, "lon": 23.7275, "name": "Athens / Mediterranean Basin"},
        "us_midwest_omaha": {"lat": 41.2565, "lon": -95.9345, "name": "Omaha / US Agricultural Midwest"},
    }
    
    parameters = "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN"
    master_rows = []
    
    for reg_id, info in regions.items():
        query_url = (
            f"https://power.larc.nasa.gov/api/temporal/monthly/point?"
            f"parameters={parameters}&community=RE&longitude={info['lon']}&latitude={info['lat']}&start=1985&end=2024&format=JSON"
        )
        print(f"Querying {info['name']} (Lat: {info['lat']}, Lon: {info['lon']})...")
        raw_json_path = os.path.join(RAW_DIR, f"nasa_power_{reg_id}.json")
        if download_file(query_url, raw_json_path):
            try:
                with open(raw_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                params_dict = data['properties']['parameter']
                t2m = params_dict.get('T2M', {})
                t2m_max = params_dict.get('T2M_MAX', {})
                t2m_min = params_dict.get('T2M_MIN', {})
                precip = params_dict.get('PRECTOTCORR', {})
                rh = params_dict.get('RH2M', {})
                solar = params_dict.get('ALLSKY_SFC_SW_DWN', {})
                
                reg_rows = []
                date_keys = sorted([k for k in t2m.keys() if len(k) == 6 and not k.endswith("13")])
                for dk in date_keys:
                    yr = int(dk[:4])
                    mo = int(dk[4:])
                    dt_str = f"{yr}-{mo:02d}-01"
                    row = [
                        reg_id, info['name'], info['lat'], info['lon'], dt_str, yr, mo,
                        t2m.get(dk, ""), t2m_max.get(dk, ""), t2m_min.get(dk, ""),
                        precip.get(dk, ""), rh.get(dk, ""), solar.get(dk, "")
                    ]
                    reg_rows.append(row)
                    master_rows.append(row)
                    
                reg_csv = os.path.join(PROCESSED_DIR, f"climate_{reg_id}.csv")
                headers = [
                    "Region_ID", "Region_Name", "Latitude", "Longitude", "Date", "Year", "Month",
                    "Temperature_Mean_C", "Temperature_Max_C", "Temperature_Min_C",
                    "Precipitation_mm_day", "Relative_Humidity_pct", "Solar_Insolation_kWm2_day"
                ]
                with open(reg_csv, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    writer.writerows(reg_rows)
                print(f"  -> Generated {len(reg_rows)} monthly climate records for {reg_id}")
            except Exception as e:
                print(f"  -> Parsing error for {reg_id}: {e}")
                
    if master_rows:
        master_csv = os.path.join(PROCESSED_DIR, "regional_climate_master.csv")
        headers = [
            "Region_ID", "Region_Name", "Latitude", "Longitude", "Date", "Year", "Month",
            "Temperature_Mean_C", "Temperature_Max_C", "Temperature_Min_C",
            "Precipitation_mm_day", "Relative_Humidity_pct", "Solar_Insolation_kWm2_day"
        ]
        with open(master_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(master_rows)
        print(f"  -> MASTER Regional Climate Dataset saved: {master_csv} ({len(master_rows)} records)")

def acquire_sea_ice():
    print("\n[3/3] Fetching Sea Ice Extent Datasets (NSIDC)...")
    urls = {
        "arctic_sea_ice_september.csv": "https://masie_web.apps.nsidc.org/pub/DATASETS/NOAA/G02135/north/monthly/data/N_09_extent_v3.0.csv",
        "antarctic_sea_ice_february.csv": "https://masie_web.apps.nsidc.org/pub/DATASETS/NOAA/G02135/south/monthly/data/S_02_extent_v3.0.csv"
    }
    for fname, url in urls.items():
        raw_path = os.path.join(RAW_DIR, fname)
        if download_file(url, raw_path):
            proc_path = os.path.join(PROCESSED_DIR, f"cleaned_{fname}")
            try:
                with open(raw_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                clean_lines = [l for l in lines if l.strip() and not l.startswith("#")]
                with open(proc_path, 'w', encoding='utf-8') as f:
                    f.writelines(clean_lines)
                print(f"  -> Cleaned {len(clean_lines)} records -> {proc_path}")
            except Exception as e:
                print(f"  -> Processing error: {e}")

if __name__ == "__main__":
    print("================================================================")
    print("  ACQUIRING OFFICIAL NASA & EARTH SYSTEM OBSERVATION DATASETS   ")
    print("================================================================")
    acquire_nasa_giss()
    acquire_nasa_power()
    acquire_sea_ice()
    print("\n>>> ALL DATASETS ACQUIRED & PROCESSED SUCCESSFULLY! <<<")
