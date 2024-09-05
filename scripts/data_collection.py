import os
import subprocess
import time

def scrape_player_stats(season_year, output_dir="data/raw", delay=3):
    """
    Scrape player stats for a given NBA season using baskref.
    
    Args:
    - season_year (int): The ending year of the season (e.g., 2023 for the 2022-23 season).
    - output_dir (str): Directory where the CSV will be saved.
    - delay (int): Delay between requests in seconds.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the output CSV file path
    output_file = os.path.join(output_dir, f"player_stats_{season_year}.csv")
    
    # Build the baskref command
    command = [
        "baskref",
        "-t", "gspl",  # Scrape player stats for the whole season
        "-y", str(season_year),  # Specify the season year
        "-fp", output_file  # File path where the data will be saved
    ]
    
    # Run the baskref command
    try:
        subprocess.run(command, check=True)
        print(f"Successfully scraped player stats for the {season_year} season.")
    except subprocess.CalledProcessError as e:
        print(f"Error scraping data for {season_year}: {e}")
    
    # Add a delay between requests to avoid rate-limiting
    time.sleep(delay)

if __name__ == "__main__":
    # Scrape player stats for seasons from 2000 to 2024
    for year in range(2000, 2025):
        scrape_player_stats(year)
