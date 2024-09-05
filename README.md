# allstar-prediction
Your README file should clearly explain your project's purpose, how to set it up, and how to use it. Here’s a template you can follow based on your NBA All-Star prediction project:

---

# NBA All-Star Prediction Project

## **Project Overview**
This project aims to predict NBA All-Star selections based on player performance stats from past seasons. By using historical data from Basketball Reference, we collect player statistics and All-Star selections to build a machine learning model that predicts the likelihood of a player being selected as an All-Star.

### **Key Objectives:**
- Scrape NBA player statistics using the `baskref` package.
- Scrape NBA All-Star selections using a custom web scraper.
- Clean and preprocess the data for analysis.
- Build a machine learning model to predict All-Star selections.

## **Project Structure**
```bash
.
├── data/
│   ├── raw/             # Scraped raw player stats (e.g., player_stats_2008.csv)
│   ├── processed/       # Cleaned and processed data
│   ├── manual/          # Manually scraped All-Star data (e.g., allstar_data.csv)
│   └── final/           # Final dataset combining player stats and All-Star data
├── models/              # Trained machine learning models
├── notebooks/           # Jupyter notebooks for analysis and exploration
├── scripts/
│   ├── data_collection.py    # Script to collect player stats using baskref
│   ├── allstar_scraper.py    # Script to scrape All-Star selections
│   ├── data_cleaning.py      # Script for cleaning and processing data
│   ├── merge_stats_labels.py # Script to combine stats and All-Star labels
│   ├── feature_engineering.py# Script to create features for model training
│   ├── model_training.py     # Script to train the predictive model
│   └── predict_allstars.py   # Script to predict All-Star selections for a future season
├── README.md
├── requirements.txt     # Project dependencies
└── .gitignore           # Files and directories to ignore in Git
```

## **Data Sources**
- **Player Stats**: Scraped from Basketball Reference using the `baskref` package.
- **All-Star Selections**: Scraped from Basketball Reference using a custom web scraper.

## **Requirements**
To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

### **Main Packages Used**:
- `baskref`: For scraping player statistics.
- `requests`: For making HTTP requests in the All-Star scraper.
- `beautifulsoup4`: For parsing HTML in the All-Star scraper.
- `pandas`: For data manipulation.
- `scikit-learn`: For building machine learning models.

## **Usage**

### **1. Scrape Player Stats**
You can scrape player statistics for multiple seasons by running the `data_collection.py` script. The scraped data will be saved in the `data/raw` directory.

```bash
python scripts/data_collection.py
```

### **2. Scrape All-Star Selections**
Run the `allstar_scraper.py` script to scrape All-Star selections for the seasons from 2000 to 2024.

```bash
python scripts/allstar_scraper.py
```

### **3. Clean and Process Data**
After scraping the data, run `data_cleaning.py` to clean the raw player stats.

```bash
python scripts/data_cleaning.py
```

### **4. Merge Player Stats with All-Star Data**
Use `merge_stats_labels.py` to merge the player statistics with the All-Star labels to create the final dataset.

```bash
python scripts/merge_stats_labels.py
```

### **5. Feature Engineering**
Run `feature_engineering.py` to create additional features for model training.

```bash
python scripts/feature_engineering.py
```

### **6. Train the Model**
Train a machine learning model to predict All-Star selections using the `model_training.py` script.

```bash
python scripts/model_training.py
```

### **7. Predict All-Star Selections**
After training the model, use `predict_allstars.py` to predict the likelihood of a player being selected for the All-Star game in future seasons.

```bash
python scripts/predict_allstars.py
```

## **Machine Learning Model**
The model uses historical player performance data to predict the probability of a player being selected as an All-Star. The model can be trained using algorithms such as:
- Random Forest
- Logistic Regression

The performance of the model can be evaluated using metrics such as:
- Accuracy
- Precision/Recall
- AUC-ROC

## **Contributing**
If you'd like to contribute to the project, feel free to submit a pull request or open an issue on GitHub.

---
