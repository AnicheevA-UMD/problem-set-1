"""
You will run this problem set from main.py so set things up accordingly.
"""

import src.extract
import src.transform_load


def main() -> None:
    # Call functions from extract.py
    weather_path = src.extract.extract_weather_data()
    transit_path = src.extract.extract_transit_data()
    print(f"Weather extract saved to: {weather_path}")
    print(f"Transit extract saved to: {transit_path}")

    # Call functions from transform_load.py
    merged_path = src.transform_load.transform_merge_and_load()
    print(f"Merged dataset saved to: {merged_path}")


if __name__ == "__main__":
    main()