import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd

# Define the output directory
base_dir = Path(__file__).resolve().parents[2] 
output_dir = base_dir / "data" / "raw" / "contracts"
output_dir.mkdir(parents=True, exist_ok=True)

# Get contracts for each player position 
positions = ["quarterback", "running-back", "fullback", "wide-receiver", "tight-end",
 "left-tackle", "left-guard", "center", "right-guard", "right-tackle", "interior-defensive-line", "edge-rusher",
 "linebacker", "safety", "cornerback", "kicker", "punter", "long-snapper"]

# Define the columns expected in the table
columns = [
    "Player", "Team", "Year_Signed", "Contract_Length", "Total_Value",
    "APY", "Guaranteed_Money", "Cap_Percentage", "Inflated_Value",
    "Inflated_APY", "Inflated_Guaranteed", "Position" ]

# Create a list to store extracted player contracts
all_contracts = []

for position in positions:
    # URL of the website containing the salary cap datas
    url = f"https://overthecap.com/contract-history/{position}"

    # Fetch the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the contract table
    table = soup.find("table", class_="position-table sortable")
    if not table:
        print(f"No table found for {position}")
        continue

    # Find all rows in the table
    rows = table.find("tbody").find_all("tr")
    print(f"Found {len(rows)} rows of player data\n")


    for row in rows:
        cols = row.find_all("td")
        if cols: 
            player_name = cols[0].text.strip()
            team = cols[1].text.strip()
            years_signed = cols[2].text.strip()
            contract_length = cols[3].text.strip()
            total_value = cols[5].text.strip()
            apy = cols[6].text.strip()
            guaranteed_money = cols[7].text.strip()
            cap_percentage = cols[9].text.strip()
            inflated_value = cols[11].text.strip()
            inflated_apy = cols[12].text.strip()
            inflated_gauranteed = cols[13].text.strip()

            all_contracts.append([
                player_name, team, years_signed, contract_length, total_value,
                apy, guaranteed_money, cap_percentage, inflated_value, inflated_apy, inflated_gauranteed, position
                ])

df = pd.DataFrame(all_contracts, columns=columns)

 # Save as CSV in the raw data folder
output_path = os.path.join(output_dir, f"nfl_player_contracts_raw.csv")
df.to_csv(output_path, index=False)
print(f'player contract data successfully saved to {output_path}')
print("\n Data collection and export complete!")