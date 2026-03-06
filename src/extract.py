'''
PART 1: EXTRACT WEATHER AND TRANSIT DATA

Pull in data from two dataset
1. Weather data from visualcrossing's weather API (https://www.visualcrossing.com/weather-api)
- You will need to sign up for a free account to get an API key
-- You only get 1000 rows free per day, so be careful to build your query correctly up front
-- Though not best practice, include your API key directly in your code for this assignment
- Write code below to get weather data for Chicago, IL for the date range 10/1/2024 - 10/31/2025
- The default data fields should be sufficient
2. Daily transit ridership data for the Chicago Transit Authority (CTA)
- Here is the URL: ttps://data.cityofchicago.org/api/views/6iiy-9s97/rows.csv?accessType=DOWNLOAD"

Load both as CSVs into /data
- Make sure your code is line with the standards we're using in this class 
'''



from __future__ import annotations

from pathlib import Path

import pandas as pd


# -----------------------------
# Configuration
# -----------------------------

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

WEATHER_OUTPUT_CSV = DATA_DIR / "weather_raw.csv"
TRANSIT_OUTPUT_CSV = DATA_DIR / "transit_raw.csv"

WEATHER_REQUEST_URL = (
    "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    "Chicago%2C%20IL/2024-10-01/2025-10-31?"
    "unitGroup=us"
    "&include=days"
    "&key=HLZGYUJLP8JVQJH3V7XM855SY"
    "&contentType=csv"
)

CTA_TRANSIT_CSV_URL = (
    "https://data.cityofchicago.org/api/views/6iiy-9s97/rows.csv?accessType=DOWNLOAD"
)


# -----------------------------------------
# Extract Visual Crossing weather data (CSV)
# -----------------------------------------

def extract_weather_data() -> Path:
    """
    Extract daily weather data for Chicago, IL from Visual Crossing and save to /data.

    Returns:
        Path to the written CSV file.
    """
    # Ensure the /data directory exists before writing outputs.
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Pull the CSV directly from the API into a DataFrame, then write to disk.
    weather_df = pd.read_csv(WEATHER_REQUEST_URL)
    weather_df.to_csv(WEATHER_OUTPUT_CSV, index=False)

    return WEATHER_OUTPUT_CSV


# -----------------------------------
# Extract CTA transit ridership (CSV)
# -----------------------------------

def extract_transit_data() -> Path:
    """
    Extract CTA daily ridership data from the City of Chicago open data portal
    and save to /data.

    Returns:
        Path to the written CSV file.
    """
    # Ensure the /data directory exists before writing outputs.
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Pull the published CSV directly into a DataFrame, then write to disk.
    transit_df = pd.read_csv(CTA_TRANSIT_CSV_URL)
    transit_df.to_csv(TRANSIT_OUTPUT_CSV, index=False)

    return TRANSIT_OUTPUT_CSV


# -------------------------
# Local test hook
# -------------------------

if __name__ == "__main__":
    weather_path = extract_weather_data()
    transit_path = extract_transit_data()
    print(f"Weather extract saved to: {weather_path}")
    print(f"Transit extract saved to: {transit_path}")