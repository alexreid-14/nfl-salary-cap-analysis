import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd

# Define the years and stats
years = list(range(2015, 2025))
stat_categories = ["passing", "rushing", "receiving", "defense_advanced"]

HEADERS = {
    "passing": [
        "Player", "Age", "Team", "Position", "Games_Played", "Games_Started", "QB_Record", "Pass_Completions", "Pass_Att", 
        "Completion_Percentage", "Passing_Yds", "Passing_TD", "Passing_TD_Percentage", "Interceptions", "Interception_Percentage", "Passing_First_Downs", "Passing_Success_Rate", "Longest_Pass", "Yards_Gained_Per_Pass_Attempt",
        "Adjusted_Yards_Gained_Per_Pass_Attempt", "Yards_Gained_Per_Completion", "Yards_Per_Game", "Passer_Rating", "QBR", "Times_Sacked", "Sack_Yards", "Sack_Percentage", "Net_Yards_Gained_Per_Pass_Attempt", "Adjusted_Net_Yards_Per_Pass_Attempt",
        "4th_Quarter_Comebacks", "Game_Winning_Drives", "Awards"
    ],
    "rushing": [
        "Player", "Age", "Team", "Position", "Games_Played", "Games_Started", "Rush_Attempts", "Rush_Yards", "Rush_TD", 
        "First_Downs_Rushing", "Rushing_Success_Rate", "Longest_Rush", "Rush_Yards_Per_Attempt", "Rush_Yards_Per_Game", "Rush_Attempts_Per_Game", "Rush_Fumbles", "Awards"
    ],
    "receiving": [
        "Player", "Age", "Team", "Position", "Games_Played", "Games_Started", "Targets", "Receptions", "Receiving_Yards", 
        "Yards_Per_Reception", "Receiving_TD", "First_Downs_Receiving", "Receiving_Success_Rate", "Longest_Reception", "Receptions_Per_Game", "Receiving_Yards_Per_Game", "Catch_Percentage", "Yards_Per_Target", 
        "Receiving_Fumbles", "Awards"
    ],
    "defense_advanced":[
        "Player", "Age", "Team", "Position", "Games_Played", "Games_Started", "Interceptions", "Times_Targeted", 
        "Completions_When_Targeted", "Completion_Percentage", "Yards_Allowed", "Yards_Per_Reception", 
        "Yards_Per_Target", "Recieving_TD_Allowed", "Passing_Rating_Allowed", "Average_Depth_Of_Target", "Total_Air_Yards", "Total_YAC", 
        "Times_Blitzed", "QB_Hurries", "QB_Hits", "Passes_Batted", "Sacks", "Pressures", "Combined_Tackles", "Missed_Tackles", "Missed_Tackle_Percentage", "Awards" 
    ]
}


# Define the output directory
base_dir = Path(__file__).resolve().parents[2] 
output_dir = base_dir / "data" / "raw" / "stats"
output_dir.mkdir(parents=True, exist_ok=True)

for category in stat_categories: 

    # Initialize a list to store all data
    all_data = []

    # Loop through each year
    for year in years:
        url = f"https://www.pro-football-reference.com/years/{year}/{category}.htm"

        # Fetch the webpage
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        print(response.status_code, url)

        # Find the table
        table = soup.find("table", {"id": category})
        if not table:
            print(f"No table found for {category} in {year}")
            continue

        if table:
            rows = table.find("tbody").find_all("tr")

            for row in rows:
                columns = row.find_all("td")
                if columns:
                    player_data = [col.text.strip() for col in columns]

                    if player_data[0].lower() == "league average":  # Stop at the league average row
                        continue
                    # Ensure consistent row length
                    expected_columns = HEADERS[category]
                    if len(player_data) == len(expected_columns): 
                        player_data.append(year)  # Add season column
                        all_data.append(player_data)
                    else:
                        print(f"Skipping row in {year} due to length mismatch")
                        print(f"Expected Columns: {len(expected_columns)}")
                        print(f"Sample Row Columns: {len(player_data)}")
                        print(f"Expected Columns: {expected_columns}")
                        print(f"Row Data: {player_data}\n")

    # Convert to DataFrame
    df = pd.DataFrame(all_data, columns=HEADERS[category] + ["season"])

    # Save as CSV in the raw data folder
    output_path = os.path.join(output_dir, f"nfl_{category}_stats_raw.csv")
    df.to_csv(output_path, index=False)
    print(f'{category} data successfully saved to {output_path}')

print("\n Data collection and export complete!")