import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_allstar_voting_data(start_year, end_year, output_file="data/manual/allstar_data.csv"):
    """
    Scrapes NBA All-Star voting selections from Basketball Reference and saves the data to a CSV.
    
    Args:
    - start_year (int): The first season year to scrape (e.g., 2000).
    - end_year (int): The last season year to scrape (e.g., 2023).
    - output_file (str): Path to save the All-Star voting data.
    """
    allstar_data = []

    # Define the possible positions and conferences
    sections = {
        "Frontcourt Eastern Conference": "frontcourt-eastern-conference",
        "Backcourt Eastern Conference": "backcourt-eastern-conference",
        "Frontcourt Western Conference": "frontcourt-western-conference",
        "Backcourt Western Conference": "backcourt-western-conference"
    }

    request_count = 0  # Track the number of requests
    for year in range(start_year, end_year + 1):
        for section_name, section_slug in sections.items():
            url = f'https://www.basketball-reference.com/allstar/NBA_{year}_voting-{section_slug}.html'
            print(f"Scraping {url}...")

            try:
                # If we've made 20 requests, wait for a minute
                if request_count >= 20:
                    print("Rate limit reached. Waiting for a minute...")
                    time.sleep(60)  # Sleep for 60 seconds
                    request_count = 0  # Reset the count

                response = requests.get(url)
                request_count += 1

                if response.status_code == 404:
                    print(f"Could not access {url}. Status code: {response.status_code}")
                    continue  # Skip to the next URL if the page doesn't exist
                elif response.status_code == 429:
                    print(f"Rate limited at {url}. Status code: 429")
                    print("Waiting for an hour due to rate limiting...")
                    time.sleep(3600)  # Wait for 1 hour if rate-limited
                    continue

                soup = BeautifulSoup(response.content, 'html.parser')

                # Find the table containing player data
                table = soup.find('table')
                if table:
                    rows = table.find('tbody').find_all('tr')
                    print(f"Found {len(rows)} rows in {section_name} for year {year}.")
                    
                    for row in rows:
                        player_name_td = row.find('td', {'data-stat': 'player_name'})
                        if player_name_td:
                            player_name = player_name_td.text.strip()

                            # Extract other statistics
                            fan_votes_td = row.find('td', {'data-stat': 'fan_votes'})
                            player_votes_td = row.find('td', {'data-stat': 'player_votes'})
                            media_votes_td = row.find('td', {'data-stat': 'media_votes'})
                            fan_votes = fan_votes_td.text.strip() if fan_votes_td else None
                            player_votes = player_votes_td.text.strip() if player_votes_td else None
                            media_votes = media_votes_td.text.strip() if media_votes_td else None

                            # Append player info and votes to the list
                            allstar_data.append({
                                'year': year,
                                'player_name': player_name,
                                'fan_votes': fan_votes,
                                'player_votes': player_votes,
                                'media_votes': media_votes,
                                'section': section_name,  # Keep track of backcourt/frontcourt and conference
                                'is_allstar': 1  # Mark as All-Star
                            })
                else:
                    print(f"Table not found for {section_name} in year {year}.")
            except Exception as e:
                print(f"Error occurred while scraping {url}: {e}")
            
            # Add a delay of 3 seconds between requests to avoid rate limiting
            time.sleep(3)

    # Convert list of All-Star data to a DataFrame
    allstar_df = pd.DataFrame(allstar_data)

    # Print DataFrame to verify if it's populated
    print(allstar_df)

    # Save the data to a CSV file
    allstar_df.to_csv(output_file, index=False)
    print(f"All-Star voting data saved to {output_file}")

if __name__ == "__main__":
    scrape_allstar_voting_data(2000, 2023)
