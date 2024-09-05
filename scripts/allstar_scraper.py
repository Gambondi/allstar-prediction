import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_allstar_data(start_year, end_year, output_file="data/manual/allstar_data.csv"):
    """
    Scrapes NBA All-Star stats from Basketball Reference from 2000 to 2024.
    
    Args:
    - start_year (int): The first season year to scrape (e.g., 2000).
    - end_year (int): The last season year to scrape (e.g., 2024).
    - output_file (str): Path to save the All-Star data as CSV.
    """
    allstar_data = []
    request_count = 0  # Track number of requests

    for year in range(start_year, end_year + 1):
        url = f'https://www.basketball-reference.com/allstar/NBA_{year}.html'
        print(f"Scraping {url}...")

        # Rate limiting: Pause after every 20 requests
        if request_count >= 20:
            print("Rate limit reached. Pausing for 1 minute...")
            time.sleep(60)  # Sleep for 60 seconds
            request_count = 0  # Reset the request count

        response = requests.get(url)
        request_count += 1

        if response.status_code == 404:
            print(f"Could not access {url}. Status code: 404")
            continue
        elif response.status_code == 429:
            print(f"Rate limited. Status code: 429. Waiting for an hour...")
            time.sleep(3600)  # Wait 1 hour if rate-limited
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        # Determine which table IDs to use based on the year
        if 2018 <= year < 2024:
            if year == 2018:
                teams = ['Team LeBron', 'Team Stephen']
            elif year in [2019, 2020, 2023]:
                teams = ['Team LeBron', 'Team Giannis']
            elif year in [2021, 2022]:
                teams = ['Team LeBron', 'Team Durant']
        else:
            teams = ['East', 'West']  # For years before 2018 and for 2024 (back to East vs. West)

        # Scrape the table data
        for team in teams:
            # Use the team name directly without removing spaces
            table = soup.find('table', {'id': team})  
            if table:
                tbody = table.find('tbody')  # Access <tbody>
                rows = tbody.find_all('tr')  # Get all rows
                print(f"Found {len(rows)} rows for {team} in year {year}.")

                for row in rows:
                    # Access player name from <th> tag using the 'csk' attribute
                    player_name_th = row.find('th', {'data-stat': 'player'})
                    if player_name_th:
                        player_name = player_name_th.get('csk', '').strip()  # Extract from csk

                        # Extract other statistics (team, points, etc.)
                        team_td = row.find('td', {'data-stat': 'team_id'})
                        team_name = team_td.text.strip() if team_td else team
                        points_td = row.find('td', {'data-stat': 'pts'})
                        points = points_td.text.strip() if points_td else None

                        # Append data to the list with binary All-Star indicator
                        allstar_data.append({
                            'year': year,
                            'team': team_name,
                            'player_name': player_name,
                            'points': points,
                            'is_allstar': 1  # Automatically set to 1 as this is an All-Star player
                        })
            else:
                print(f"No table found for {team} in year {year}.")

        # Add a delay of 3 seconds between each request to avoid rate-limiting
        time.sleep(3)

    # Convert data to a DataFrame and save as CSV
    allstar_df = pd.DataFrame(allstar_data)
    allstar_df.to_csv(output_file, index=False)
    print(f"All-Star data saved to {output_file}")

if __name__ == "__main__":
    scrape_allstar_data(2000, 2024)
