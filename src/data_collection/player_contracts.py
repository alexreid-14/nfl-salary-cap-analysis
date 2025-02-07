import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd

# URL of the website containing the salary cap data
url = "https://overthecap.com/contracts"

# Fetch the webpage
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all table rows that contain player data
rows = soup.find_all("tr", class_="sortable")
print(f"Found {len(rows)} rows of player data\n")

# Create a list to store extracted player data
players_data = []

# Extract table data
for row in rows:
    columns = row.find_all("td")    
    player_name = columns[0].text.strip()
    position = columns[1].text.strip()
    team = columns[2].text.strip()
    total_value = columns[3].text.strip()
    average_per_year = columns[4].text.strip()
    total_gauranteed = columns[5].text.strip()

    players_data.append([player_name, position, team, total_value, average_per_year, total_gauranteed])

# Convert to Pandas DataFrame
df = pd.DataFrame(players_data, columns=["Player", "Position", "Team", "Total Value", "Average Per Year", "Total Guaranteed"])

# Define the output directory
base_dir = Path(__file__).resolve().parents[2] 
output_dir = base_dir / "data" / "raw"


# Save as CSV in the raw data folder
output_path = os.path.join(output_dir, "nfl_player_salary_raw.csv")
df.to_csv(output_path, index=False)

# Print the first few rows for verification
print(df.head())
print(f"Data successfully saved to {output_path}")