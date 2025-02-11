import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd

# Define the output directory
base_dir = Path(__file__).resolve().parents[2] 
output_dir = base_dir / "data" / "raw" / "team"
output_dir.mkdir(parents=True, exist_ok=True)

# Get contracts for each team
teams = ["arizona-cardinals", "atlanta-falcons", "baltimore-ravens", "buffalo-bills",
         "carolina-panthers", "chicago-bears", "cincinnati-bengals", "cleveland-browns", "dallas-cowboys",
         "denver-broncos", "detroit-lions", "green-bay-packers", "houston-texans", "indianapolis-colts",
         "jacksonville-jaguars", "kansas-city-chiefs", "las-vegas-raiders", "los-angeles-chargers",
         "los-angeles-rams", "miami-dolphins", "minnesota-vikings", "new-england-patriots",
         "new-orleans-saints", "new-york-giants", "new-york-jets", "philadelphia-eagles", "pittsburgh-steelers",
         "san-francisco-49ers", "seattle-seahawks", "tampa-bay-buccaneers", "tennessee-titans", "washington-commanders"]

# Get contracts for each cap type 
cap_types = ["table_active", "table_injured", "table_practice-squad", "table_dead"]

# Get contracts for each year
years = list(range(2015, 2026))


# Define the columns expected in the table
columns = [
    "Player", "Position", "Age", "Cap_Hit", "Cap_Hit_Percentage", "Dead_Cap", "Base_Salary", "Signing_Bonus", 
    "Per_Game_Bonus", "Roster_Bonus", "Option_Bonus", "Workout_Bonus", "Restructure_Proration", "Incentives",
    "Cap_Type", "Year"
    ]


for team in teams:
    # Create a list to store extracted team contracts 
    team_salaries = []

    for year in years:

        for cap in cap_types: 
            # URL of the website containing the salary cap datas
            url = f"https://www.spotrac.com/nfl/{team}/cap/_/year/{year}/sort/cap_total"

            # Fetch the webpage
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the contract table
            table = soup.find("table", {"id": {cap}})
            if not table:
                print(f"No table found for {team} - {cap} in {year}")
                continue

            # Find all rows in the table
            rows = table.find("tbody").find_all("tr")

            for row in rows:
                cols = row.find_all("td")
                if cols: 
                    player_salary = [col.text.strip() for col in cols]
                    player_salary[0] = player_salary[0].split("\n")[-1]
                    player_salary.append(cap)
                    player_salary.append(year) 
                    team_salaries.append(player_salary)

    df = pd.DataFrame(team_salaries, columns=columns)

     # Save as CSV in the raw data folder
    output_path = os.path.join(output_dir, f"nfl_{team}_player_salary_raw.csv")
    df.to_csv(output_path, index=False)
    print(f'player contract data successfully saved to {output_path}')

print("\n Data collection and export complete!")
