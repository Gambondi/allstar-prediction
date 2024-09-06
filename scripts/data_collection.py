from baskref.data_collection.baskref_data_scraper import BaskRefDataScraper
from baskref.data_collection.baskref_url_scraper import BaskRefUrlScraper
from baskref.data_saving.file_saver import save_file_from_list
import time
import os

def scrape_player_stats_for_season(year, batch_size=20):
    """
    Scrape player stats for the entire season (regular season + playoffs) and save to CSV in batches.
    
    Args:
    - year (int): The year for the NBA season (e.g., 2008 for the 2007-2008 season).
    - batch_size (int): Number of games to scrape before saving data.
    """
    url_scraper = BaskRefUrlScraper()
    data_scraper = BaskRefDataScraper()
    
    # Get all game URLs for the season
    game_urls = url_scraper.get_game_urls_year(year)
    print(f"Scraping player stats for {year} season. Found {len(game_urls)} games.")
    
    all_player_stats = []
    output_file = f'data/raw/player_stats_{year}.csv'
    
    # If the file exists, load its data to avoid duplicating work
    if os.path.exists(output_file):
        print(f"{output_file} already exists. Loading existing data to continue.")
        existing_df = pd.read_csv(output_file)
        all_player_stats = existing_df.to_dict('records')
    
    for i, url in enumerate(game_urls):
        try:
            # Scrape player stats for each game
            player_stats = data_scraper.get_player_stats_data([url])
            all_player_stats.extend(player_stats)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        
        # Periodically save data in batches
        if (i + 1) % batch_size == 0:
            save_file_from_list(all_player_stats, output_file)
            print(f"Saved batch {i+1}/{len(game_urls)} to {output_file}")
        
        # Add delay between requests to stay within the rate limit
        time.sleep(4)  # 4 seconds to stay below 20 requests/minute
    
    # Final save after all scraping
    save_file_from_list(all_player_stats, output_file)
    print(f"Player stats for {year} season saved to {output_file}")

if __name__ == "__main__":
    scrape_player_stats_for_season(2000)
