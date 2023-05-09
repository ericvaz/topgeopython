import pandas as pd
import requests
from tqdm import tqdm

def get_github_repo_info(user, repo):
    url = f"https://api.github.com/repos/{user}/{repo}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        repo_info = response.json()
        
        # Extract relevant information
        info = {
            "forks_count": repo_info["forks_count"],
            "stargazers_count": repo_info["stargazers_count"],
            "watchers_count": repo_info["watchers_count"],
        }
    except requests.exceptions.RequestException:
        info = {
            "forks_count": None,
            "stargazers_count": None,
            "watchers_count": None,
        }

    return info

# Read the overview CSV file
overview_df = pd.read_csv("overview_with_related.csv")

# Filter the DataFrame to keep only packages related to GIS
gis_packages_df = overview_df[overview_df["related"]]

# Add new columns to store GitHub repository information
gis_packages_df["forks_count"] = None
gis_packages_df["stargazers_count"] = None
gis_packages_df["watchers_count"] = None

# Update the DataFrame with GitHub repository information
for index, row in tqdm(gis_packages_df.iterrows(), total=gis_packages_df.shape[0]):
    package_name = row["package_name"]
    
    # Define the user and repo names; you may need to adjust this based on the package
    user = "package_author"  # Replace with the actual package author or organization
    repo = package_name

    repo_info = get_github_repo_info(user, repo)
    
    gis_packages_df.at[index, "forks_count"] = repo_info["forks_count"]
    gis_packages_df.at[index, "stargazers_count"] = repo_info["stargazers_count"]
    gis_packages_df.at[index, "watchers_count"] = repo_info["watchers_count"]

# Save the updated DataFrame as a new CSV file
gis_packages_df.to_csv("gis_packages_with_github_info.csv", index=False)

