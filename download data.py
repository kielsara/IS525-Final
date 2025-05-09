import os
import requests
import pandas as pd
from tqdm import tqdm

# ==== downloading data, creating .csv file ====
# Station code for LaGuardia Airport
station_file = "72503014732.csv"

# Output folder
os.makedirs("gsod_laguardia", exist_ok=True)

# Define the years wanted
start_year = 1929
end_year = 2025

base_url = "https://www.ncei.noaa.gov/data/global-summary-of-the-day/access"

all_dataframes = []

for year in tqdm(range(start_year, end_year + 1)):
    url = f"{base_url}/{year}/{station_file}"
    output_path = f"gsod_laguardia/{year}_{station_file}"

    try:
        # Attempt to download
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)

            df = pd.read_csv(output_path)
            df["YEAR"] = year  # Add year column for reference
            all_dataframes.append(df)
        else:
            print(f"⚠️ {year}: File not found or error ({response.status_code})")
    except Exception as e:
        print(f"❌ {year}: Download failed with error: {e}")

# Combine all years into one DataFrame
if all_dataframes:
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    combined_df.to_csv("laguardia_gsod_all_years.csv", index=False)
    print("✅ All available data saved to laguardia_gsod_all_years.csv")
else:
    print("❌ No data was downloaded.")