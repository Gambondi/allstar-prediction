from baskref.data_collection.baskref_data_scraper import BaskRefDataScraper
from baskref.data_collection.baskref_url_scraper import BaskRefUrlScraper
from baskref.data_saving.file_saver import save_file_from_list
import time

def scrape_player_stats_for_season(year):
    """
    Scrape player stats for the entire season (regular season + playoffs) and save to CSV.
    
    Args:
    - year (int): The year for the NBA season (e.g., 2008 for the 2007-2008 season).
    """
    url_scraper = BaskRefUrlScraper()
    data_scraper = BaskRefDataScraper()
    
    # Get all game URLs for the season
    game_urls = url_scraper.get_game_urls_year(year)
    print(f"Scraping player stats for {year} season. Found {len(game_urls)} games.")
    
    all_player_stats = []
    
    for i, url in enumerate(game_urls):
        try:
            # Scrape player stats for each game
            player_stats = data_scraper.get_player_stats_data([url])
            all_player_stats.extend(player_stats)
            print(f"Successfully scraped {url} ({i+1}/{len(game_urls)}).")
            
        except Exception as e:
            if '429' in str(e):
                # Handle rate limiting: if a TooManyRequests error occurs, wait for 1 hour
                print("Rate limit hit. Waiting for 1 hour...")
                time.sleep(3600)  # Wait for 1 hour
                continue  # Retry the failed request after waiting
            else:
                print(f"Error scraping {url}: {e}")
        
        # Add delay between requests to stay within the rate limit
        time.sleep(10)  # 10 seconds to avoid rate limiting
    
    # Save scraped data to CSV
    save_file_from_list(all_player_stats, f'data/raw/player_stats_{year}.csv')
    print(f"Player stats for {year} season saved to data/raw/player_stats_{year}.csv")

if __name__ == "__main__":
    for year in range(2000, 2025):
        scrape_player_stats_for_season(year)
        # Add a delay between seasons
        time.sleep(60)  # 1-minute pause between seasons to reset any potential rate limits
