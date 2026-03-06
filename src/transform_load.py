'''
PART 2: Merge and transform the data
- Read in the two datasets from /data into two separate dataframes
- Profile, clean, and standardize date fields for both as needed
- Merge the two dataframe for the date range 10/1/2024 - 10/31/2025
- Conduct EDA to understand the relationship between weather and transit ridership over time
-- Create a line plot of daily transit ridership and daily average temperature over the whole time period
-- For February 2025, create a scatterplot of daily transit ridership vs. precipitation
-- Create a correlation heatmap of all numeric features in the merged dataframe
-- Load the merged dataframe as a CSV into /data
-- In a print statement, summarize any interesting trends you see in the merged dataset

'''
from __future__ import annotations

from pathlib import Path

import pandas as pd

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
WEATHER_INPUT_CSV = DATA_DIR / "weather_raw.csv"
TRANSIT_INPUT_CSV = DATA_DIR / "transit_raw.csv"
LINE_PLOT_PATH = DATA_DIR / "eda_line_ridership_vs_avgtemp.png"
SCATTER_PLOT_PATH = DATA_DIR / "eda_scatter_feb2025_ridership_vs_precip.png"
HEATMAP_PATH = DATA_DIR / "eda_corr_heatmap.png"
MERGED_OUTPUT_CSV = DATA_DIR / "weather_transit_merged.csv"


def transform_merge_and_load() -> Path:
    """
    Part 2 entrypoint (in progress):
    - Read in the two datasets
    - Profile, clean, and standardize date fields
    - Merge for 2024-10-01 to 2025-10-31
    - Add unique row ID
    - Write merged CSV (so EDA can be conducted from the merged output)
    - Create a line plot of daily transit ridership vs daily average temperature

    Returns:
        Path to the merged CSV written to /data.
    """
    # Read raw extracts created by src/extract.py
    weather_df = pd.read_csv(WEATHER_INPUT_CSV)
    transit_df = pd.read_csv(TRANSIT_INPUT_CSV)

    # Profile: confirm successful reads and inspect available columns
    print(f"Weather rows/cols: {weather_df.shape}")
    print(f"Transit rows/cols: {transit_df.shape}")
    print(f"Weather columns: {list(weather_df.columns)}")
    print(f"Transit columns: {list(transit_df.columns)}")

    # Standardize to a shared merge key named 'date' (datetime64[ns], day-level)
    if "datetime" in weather_df.columns:
        weather_df["date"] = pd.to_datetime(weather_df["datetime"], errors="coerce")
    elif "date" in weather_df.columns:
        weather_df["date"] = pd.to_datetime(weather_df["date"], errors="coerce")
    else:
        raise KeyError("Weather dataset missing expected date column (tried 'datetime' and 'date').")

    if "date" in transit_df.columns:
        transit_df["date"] = pd.to_datetime(transit_df["date"], errors="coerce")
    elif "service_date" in transit_df.columns:
        transit_df["date"] = pd.to_datetime(transit_df["service_date"], errors="coerce")
    elif "day" in transit_df.columns:
        transit_df["date"] = pd.to_datetime(transit_df["day"], errors="coerce")
    else:
        raise KeyError("Transit dataset missing expected date column (tried 'date', 'service_date', 'day').")

    # Clean: drop rows where the standardized date could not be parsed
    weather_df = weather_df.dropna(subset=["date"]).copy()
    transit_df = transit_df.dropna(subset=["date"]).copy()

    # Standardize to day-level (strip time component) to support a clean daily merge
    weather_df["date"] = weather_df["date"].dt.floor("D")
    transit_df["date"] = transit_df["date"].dt.floor("D")

    # Filter to required range
    start_date = pd.to_datetime("2024-10-01")
    end_date = pd.to_datetime("2025-10-31")

    weather_df = weather_df.loc[(weather_df["date"] >= start_date) & (weather_df["date"] <= end_date)].copy()
    transit_df = transit_df.loc[(transit_df["date"] >= start_date) & (transit_df["date"] <= end_date)].copy()

    # Merge on daily date
    merged_df = pd.merge(
        transit_df,
        weather_df,
        on="date",
        how="inner",
        suffixes=("_transit", "_weather"),
    ).sort_values("date")

    print(f"Merged rows/cols: {merged_df.shape}")

    # Add unique row ID (required output data standard)
    merged_df = merged_df.reset_index(drop=True)
    merged_df.insert(0, "row_id", merged_df.index + 1)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    merged_df.to_csv(MERGED_OUTPUT_CSV, index=False)
    print(f"Merged CSV written to: {MERGED_OUTPUT_CSV}")

    # ------------------------------------------------------------
    # EDA: Line plot of daily ridership and daily average temperature
    # (using known column names)
    # ------------------------------------------------------------

    ridership_col = "total_rides"
    temp_col = "temp"

    merged_df[ridership_col] = pd.to_numeric(merged_df[ridership_col], errors="coerce")
    merged_df[temp_col] = pd.to_numeric(merged_df[temp_col], errors="coerce")

    fig, ax1 = plt.subplots(figsize=(14, 6))

    ax1.plot(
        merged_df["date"],
        merged_df[ridership_col],
        color="tab:blue",
        linewidth=1.5,
    )
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Daily ridership (total_rides)", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    ax2 = ax1.twinx()
    ax2.plot(
        merged_df["date"],
        merged_df[temp_col],
        color="tab:red",
        linewidth=1.5,
    )
    ax2.set_ylabel("Daily average temperature (temp)", color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")

    plt.title("Daily Transit Ridership vs. Daily Average Temperature (Chicago)")
    fig.tight_layout()
    fig.savefig(LINE_PLOT_PATH, dpi=150)
    plt.close(fig)

    print(f"Saved line plot to: {LINE_PLOT_PATH}")

    # ------------------------------------------------------------
    # EDA: February 2025 scatterplot (ridership vs precipitation)
    # ------------------------------------------------------------

    precip_col = "precip"

    merged_df[precip_col] = pd.to_numeric(merged_df[precip_col], errors="coerce")

    feb_start = pd.to_datetime("2025-02-01")
    feb_end = pd.to_datetime("2025-02-28")

    feb_df = merged_df.loc[(merged_df["date"] >= feb_start) & (merged_df["date"] <= feb_end)].copy()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(
        feb_df[precip_col],
        feb_df[ridership_col],
        alpha=0.7,
    )
    ax.set_xlabel("Precipitation (precip)")
    ax.set_ylabel("Daily ridership (total_rides)")
    ax.set_title("February 2025: Daily Ridership vs. Precipitation")
    fig.tight_layout()
    fig.savefig(SCATTER_PLOT_PATH, dpi=150)
    plt.close(fig)

    print(f"Saved February 2025 scatterplot to: {SCATTER_PLOT_PATH}")

    # ------------------------------------------------------------
    # EDA: Correlation heatmap of all numeric features (merged data)
    # ------------------------------------------------------------

    numeric_df = merged_df.select_dtypes(include="number").copy()
    corr = numeric_df.corr(numeric_only=True)

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Correlation Heatmap (Numeric Features)")
    fig.tight_layout()
    fig.savefig(HEATMAP_PATH, dpi=150)
    plt.close(fig)

    print(f"Saved correlation heatmap to: {HEATMAP_PATH}\n")

    # ------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------
    
    print("Notes on Trends")
    print(
    "There is a low-to-moderate positive correlation between the number of warmer days and warmer weather and number of public transit rides.\n"
    "This is evident from the line plots as well as the heatmap and actually surprised me - as, for some reason, I've expected there to be an increase during the rain days as well.\n"
    "Looking more into outside research, however, clears it up in that severe rain in general keeps people from traveling period - not just via public transit.\n"
    "Additionally, the line chart shows a mild downward trend where ridership generally decreases during the colder times of the year - something that is supported by the heatmap as well and, again, makes sense after I've looked at outside research. \n"
    "\n"
    "When it comes to the scatterplot, it stands apart in that the number of rides is in general steady and precipitation has no great effect.\n"
    "Looking into the dataset to understand more, it become clear that for February 2025, precipitation just doesn't play that much of a role and, instead, the main deciding factor is whether a given day is a weekday or a weekend, with weekdays being the more ride-heavy days.\n"
    "Also, looking at the severity rating, it does seem like February 2025 was relatively mild in terms of inclement weather - which is supported by the scatterplot showing that the biggest amount of precipitation was 0.07 inches - far shorter of the .3 inches of rainfall that would be considered significant.\n"
    "\n"
    "The overall takeaway is that while weather does play a relatively notable role - and mild and long spells of warm weather do increase daily ridership and severe weather events reduce it - in general the strongest factor present - and one that can be easily missed as it isn't numerical - is what the type of day it is, with weekdays producing the most ridership by far. \n"
    "Ultimately, people will follow their routines and overall seasonal temperature trends (higher ridership for warm; lower for cold seasons) have a more pronounced effect compared to specific precipitation events - unless they are particularly severe and disrupt the said routines entirely."
    "\n"
    )
    
    return MERGED_OUTPUT_CSV
transform_merge_and_load()
