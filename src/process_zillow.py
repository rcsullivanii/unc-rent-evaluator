import pandas as pd
import os
import glob
from geopy.distance import geodesic
from tqdm import tqdm

# Location of Old Well
OLD_WELL_COORDS = (35.9120729, -79.0512301)

# Set of Zillow features to keep, including rent info
COLUMNS_TO_KEEP = [
    'zpid', 'zestimate', 'rentZestimate', 'latitude', 'longitude',
    'bedrooms', 'bathrooms', 'livingArea', 'yearBuilt',
    'lotSize', 'homeType', 'homeStatus'
]

def distance_to_old_well(row):
    try:
        return geodesic((row['latitude'], row['longitude']), OLD_WELL_COORDS).miles
    except:
        return None

def process_all_json(raw_dir, out_path):
    files = glob.glob(os.path.join(raw_dir, '*.json'))
    chunks = []

    print(f"Processing {len(files)} files...")

    for file in tqdm(files):
        try:
            temp = pd.read_json(file)

            # Keep only relevant columns (skip files that are missing them)
            missing_cols = set(COLUMNS_TO_KEEP) - set(temp.columns)
            if missing_cols:
                print(f"[WARN] Skipped {file}: missing columns {missing_cols}")
                continue

            temp = temp[COLUMNS_TO_KEEP]

            # Drop rows missing critical geo/rent fields
            temp.dropna(subset=['rentZestimate', 'latitude', 'longitude'], inplace=True)

            # Compute distance to Old Well
            temp['miles_to_old_well'] = temp.apply(distance_to_old_well, axis=1)

            # Filter to 5 miles from UNC
            temp = temp[temp['miles_to_old_well'] <= 5]

            chunks.append(temp)
        except Exception as e:
            print(f"[WARN] Skipped {file}: {e}")

    df = pd.concat(chunks, ignore_index=True)
    df.to_parquet(out_path)
    print(f"✅ Saved cleaned rent-focused Zillow data to: {out_path}")


if __name__ == "__main__":
    raw_dir = "data/raw"
    out_path = "data/processed/zillow_rent_cleaned.parquet"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    process_all_json(raw_dir, out_path)