import pandas as pd
import os

def clean_player_stats(input_dir="data/raw/", output_dir="data/processed/"):
    """
    Clean and process raw player stats data.
    """
    # List all raw player stats files
    raw_files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]
    
    for file in raw_files:
        print(f"Processing {file}...")
        file_path = os.path.join(input_dir, file)
        df = pd.read_csv(file_path)

        # Example cleaning process: remove rows with missing player IDs
        df_cleaned = df.dropna(subset=['player_id'])
        
        # You can add more cleaning steps as necessary, e.g., converting types, normalizing data

        # Save the cleaned data
        output_file_path = os.path.join(output_dir, file)
        df_cleaned.to_csv(output_file_path, index=False)
        print(f"Cleaned data saved to {output_file_path}")

if __name__ == "__main__":
    clean_player_stats()
