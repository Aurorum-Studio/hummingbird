import requests
import json
import time
from datetime import datetime

# iNaturalist API 的基础 URL
BASE_URL = "https://api.inaturalist.org/v1/observations"

# 配置参数
PLACES = {
    "Washington": 46,  # 假设华盛顿的地点 ID 是 12
    "California": 14,  # 假设加利福尼亚的地点 ID 是 13
    "Mexico": 6793,  # 假设墨西哥的地点 ID 是 14
    "Florida": 21,  # 假设南卡罗来纳的地点 ID 是 15
    "Massachusetts": 2,  # 假设马萨诸塞的地点 ID 是 16
    "Honduras": 6929  # 假设洪都拉斯的地点 ID 是 17
}
TAXON_ID = 6317
START_YEAR = 1990
END_YEAR = 2025

results = {"years": list(range(START_YEAR, END_YEAR + 1))}

def fetch_observations(place_id, year, taxon_id, is_winter=False):
    month = 1 if is_winter else None
    params = {
        "place_id": place_id,
        "year": year,
        "taxon_id": taxon_id,
        "month": month,
        "per_page": 0
    }
    while True:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()["total_results"]
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 1))
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
        else:
            print(f"Error fetching data for {place_id} in {year}: {response.status_code}")
            return 0

for place_name, place_id in PLACES.items():
    print(f"Fetching data for {place_name}...")
    results[place_name] = {
        "observation_counts": [],
        "winter_observation_counts": []
    }
    for year in range(START_YEAR, END_YEAR + 1):
        total_count = fetch_observations(place_id, year, TAXON_ID)
        winter_count = fetch_observations(place_id, year, TAXON_ID, is_winter=True)
        results[place_name]["observation_counts"].append(total_count)
        results[place_name]["winter_observation_counts"].append(winter_count)
        time.sleep(1)  # Ensure 1 second delay between requests

with open("inaturalist_observations_1990_2025.json", "w") as f:
    json.dump(results, f, indent=4)

print("Data fetching complete. Results saved to inaturalist_observations_1990_2025.json")
