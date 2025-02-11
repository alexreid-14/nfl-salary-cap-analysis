import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd

# Define the output directory
base_dir = Path(__file__).resolve().parents[2] 
output_dir = base_dir / "data" / "raw" / "team" / "summary"
output_dir.mkdir(parents=True, exist_ok=True)

# Get contracts for each year
years = list(range(2015, 2026))


# Define the columns expected in the table
columns = [
    "Metric", "Value", "Rank", "Year"
    ]


# Create a list to store extracted team contracts 
team_salaries = []

for year in years:

    # URL of the website containing the salary cap datas
    url = f"https://www.spotrac.com/nfl/cap/_/year/{year}/sort/cap_maximum_space2"

    # Fetch the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the contract table
    table = soup.find("table", class_ = "table table-internal-sort mt-4 relative tablesorter tablesorter-default tablesorter7b75063d71045")
    if not table:
        print(f"No table found for {year}")
        continue

    # Find all rows in the table
    rows = table.find("tbody").find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        if cols: 
            player_salary = [col.text.strip() for col in cols]
            player_salary.append(year) 
            team_salaries.append(player_salary)

df = pd.DataFrame(team_salaries, columns=columns)

# Save as CSV in the raw data folder
output_path = os.path.join(output_dir, f"nfl_{team}_player_contracts_raw.csv")
df.to_csv(output_path, index=False)
print(f'player contract data successfully saved to {output_path}')

print("\n Data collection and export complete!")
