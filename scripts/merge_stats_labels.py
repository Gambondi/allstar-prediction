import pandas as pd
import os

def merge_player_stats_with_allstar(player_stats_dir="data/processed/", allstar_file="data/manual/allstar_data.csv", output_file="data/final/merged_data.csv"):
    """
    Merges player stats with All-Star selections to create a final dataset.
    """
    # Load All-Star data
    allstar_df = pd.read_csv(allstar_file)
    
    # Initialize an empty DataFrame to store the merged results
    merged_data = pd.DataFrame()

    # List all player stats files
    player_files = [f for f in os.listdir(player_stats_dir) if f.endswith(".csv")]
    
    for file in player_files:
        year = int(file.split('_')[-1].split('.')[0])  # Extract year from file name
        print(f"Merging data for {year} season...")
        
        # Load player stats
        player_stats = pd.read_csv(os.path.join(player_stats_dir, file))
        
        # Filter All-Star data for the current year
        allstar_for_year = allstar_df[allstar_df['year'] == year]
        
        # Merge player stats with All-Star data (left join on player_name)
        merged_df = pd.merge(player_stats, allstar_for_year[['player_name', 'is_allstar']], on='player_name', how='left')
        
        # Fill NaN values in is_allstar with 0 (for players who were not All-Stars)
        merged_df['is_allstar'].fillna(0, inplace=True)
        
        # Append to the final dataset
        merged_data = pd.concat([merged_data, merged_df])
    
    # Save the merged dataset
    merged_data.to_csv(output_file, index=False)
    print(f"Merged data saved to {output_file}")

if __name__ == "__main__":
    merge_player_stats_with_allstar()
