import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the years and stats
years = list(range(2015, 2025))
stat_categories = ["passing", "rushing", "receiving"]

# Define the output directory
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")

for category in stat_categories: 

    # Initialize a list to store all data
    all_data = []
    
    # Loop through each year
    for year in years:
        url = f"https://www.pro-football-reference.com/years/{year}/{category}.htm"

        # Fetch the webpage
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table
        table = soup.find("table", {"id": category})

        if table:
            headers = [th.text.strip() for th in table.find("thead").find_all("th")][1:]  # Skip first header (rank)
            rows = table.find("tbody").find_all("tr")

            for row in rows:
                columns = row.find_all("td")
                if columns:
                    player_data = [col.text.strip() for col in columns]

                    if player_data[0].lower() == "league average":  # Stop at the league average row
                        continue
                    # Ensure consistent row length
                    if len(player_data) == len(headers): 
                        player_data.append(year)  # Add season column
                        all_data.append(player_data)
                    else:
                        print(f"Skipping row in {year} due to length mismatch: {player_data}")

    # Convert to DataFrame
    df = pd.DataFrame(all_data, columns=headers + ["season"])

    # Save as CSV in the raw data folder
    output_path = os.path.join(output_dir, f"nfl_{category}_stats_raw.csv")
    df.to_csv(output_path, index=False)
    print(f'{category} data successfully saved to {output_path}')

print("\n🚀 **Data collection and export complete!**")