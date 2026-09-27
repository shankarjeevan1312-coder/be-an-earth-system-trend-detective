"""
Acquire NSIDC Sea Ice v4.0 Datasets.
"""
import os
import urllib.request
import csv

BASE_DIR = r"C:\Users\jeeva\.gemini\antigravity\scratch\earth_system_trend_detective"
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

HEADERS = {
    "User-Agent": "NASA-Space-Apps-Earth-Trend-Detective/1.0"
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
        print(f"  -> Failed to download {url}: {e}")
        return False

def acquire_sea_ice_v4():
    urls = {
        "arctic_sea_ice_september_v4.csv": "https://noaadata.apps.nsidc.org/NOAA/G02135/north/monthly/data/N_09_extent_v4.0.csv",
        "antarctic_sea_ice_february_v4.csv": "https://noaadata.apps.nsidc.org/NOAA/G02135/south/monthly/data/S_02_extent_v4.0.csv",
        "arctic_sea_ice_daily_v4.csv": "https://noaadata.apps.nsidc.org/NOAA/G02135/north/daily/data/N_seaice_extent_daily_v4.0.csv"
    }
    
    for fname, url in urls.items():
        raw_path = os.path.join(RAW_DIR, fname)
        if download_file(url, raw_path):
            proc_path = os.path.join(PROCESSED_DIR, f"cleaned_{fname}")
            try:
                with open(raw_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                clean_lines = [l for l in lines if l.strip() and not l.strip().startswith("#")]
                with open(proc_path, 'w', encoding='utf-8') as f:
                    f.writelines(clean_lines)
                print(f"  -> Cleaned {len(clean_lines)} records -> {proc_path}")
            except Exception as e:
                print(f"  -> Processing error: {e}")

if __name__ == "__main__":
    acquire_sea_ice_v4()
