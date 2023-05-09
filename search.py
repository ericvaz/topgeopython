import pandas as pd
import requests
from tqdm import tqdm

def search_package(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    related_keywords = ["gis", "geography", "spatial analysis"]
    package_info_dict = {}

    try:
        response = requests.get(url)
        response.raise_for_status()

        package_info = response.json()
        description = package_info["info"]["summary"]

        if description is not None:
            description = description.lower()
            if any(keyword.lower() in description for keyword in related_keywords):
                package_info_dict["package_name"] = package_name
                package_info_dict["creator"] = package_info["info"]["author"]
                package_info_dict["summary"] = package_info["info"]["summary"]

    except requests.exceptions.RequestException:
        pass

    return package_info_dict

# Read the overview CSV file
overview_df = pd.read_csv("overview.csv")

# Add a new column with the search results
# Use tqdm.pandas() to display a progress bar
tqdm.pandas()
overview_df["related"] = overview_df["package_name"].progress_apply(search_package)

# Save the updated DataFrame as a new CSV file
overview_df.to_csv("overview_with_related.csv", index=False)
