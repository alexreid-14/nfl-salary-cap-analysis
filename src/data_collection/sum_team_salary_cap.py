import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd

# Define the output directory
base_dir = Path(__file__).resolve().parents[2] 
output_dir = base_dir / "data" / "raw" / "team" / "summary"
output_dir.mkdir(parents=True, exist_ok=True)

# Get contracts for each team
teams = ["arizona-cardinals", "atlanta-falcons", "baltimore-ravens", "buffalo-bills",
         "carolina-panthers", "chicago-bears", "cincinnati-bengals", "cleveland-browns", "dallas-cowboys",
         "denver-broncos", "detroit-lions", "green-bay-packers", "houston-texans", "indianapolis-colts",
         "jacksonville-jaguars", "kansas-city-chiefs", "las-vegas-raiders", "los-angeles-chargers",
         "los-angeles-rams", "miami-dolphins", "minnesota-vikings", "new-england-patriots",
         "new-orleans-saints", "new-york-giants", "new-york-jets", "philadelphia-eagles", "pittsburgh-steelers",
         "san-francisco-49ers", "seattle-seahawks", "tampa-bay-buccaneers", "tennessee-titans", "washington-commanders"]

# Get contracts for each year
years = list(range(2015, 2026))


for year in years:

    team_cap_data = [] 

    for team in teams:

        # URL of the website containing the salary cap datas
        url = f"https://www.spotrac.com/nfl/{team}/cap/_/year/{year}/sort/cap_total"

        # Fetch the webpage
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the contract table
        table = soup.find("table", {"id": "table"})
        if not table:
            print(f"No table found for {team} in {year}")
            continue

        # Find all rows in the table
        rows = table.find("tbody").find_all("tr")

        for row in rows:
            cols = row.find_all("td")

            if len(cols) < 2:
                continue 
            category = cols[0].text.strip()
            amount = cols[1].text.strip()
            team_cap_data.append({
                "Team": team, 
                "Year": year, 
                "Category": category,
                "Amount": amount
                })

    df = pd.DataFrame(team_cap_data)
    df_pivot = df.pivot(index=["Team", "Year"], columns="Category", values="Amount").reset_index()
    df_pivot.columns.name = None 

    # Save as CSV in the raw data folder
    output_path = os.path.join(output_dir, f"nfl_{year}_team_salary_cap.csv")
    df_pivot.to_csv(output_path, index=False)
    print(f'player contract data successfully saved to {output_path}')

print("\n Data collection and export complete!")
