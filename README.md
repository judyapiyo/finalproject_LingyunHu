# finalproject_LingyunHu

## 📊 Project Overview

This project explores the relationship between **cost of living**, **median income**, and **mental health** across U.S. states. Using data collected from multiple public sources via APIs and web scraping, we aim to uncover patterns and disparities in mental health outcomes associated with economic factors.

## 📁 Data Sources

1. **Cost of Living Index by State**  
   - Source: [World Population Review](https://worldpopulationreview.com/state-rankings/cost-of-living-index-by-state)  
   - Method: Web scraping  
   - File: `cost_of_living.csv`

2. **Median Income by State**  
   - Source: [Data USA](https://datausa.io/)  
   - Method: API request  
   - File: `state_income_datausa.csv`

3. **Mental Health Indicators by State**  
   - Source: [County Health Rankings & Roadmaps](https://www.countyhealthrankings.org/)  
   - Method: Manual download (cleaned from raw CSV)  
   - File: `analytic_data2024.csv`

## 🧹 Cleaning and Merging

All three datasets were cleaned using Python (see `clean_and_merge.py`). The cleaning process included:
- Removing null or redundant columns
- Normalizing state names
- Converting income and cost data to numeric
- Extracting state-level mental health scores

Final merged dataset saved as: `final_dataset.csv`

## 🧪 Analysis Goals

We will analyze:
- Correlation between cost of living and reported poor mental health
- Income-to-cost ratio and its predictive power on mental health
- Potential disparities across regions

## 🚀 How to Run

1. Clone the repo:
   ```
   git clone https://github.com/judyapiyo/finalproject_LingyunHu.git
   cd finalproject_LingyunHu
   ```

2. Install dependencies (if needed):
   ```
   pip install pandas requests beautifulsoup4
   ```

3. Run data scripts:
   ```
   python get_income_api.py
   python scrape_cost_of_living.py
   python clean_and_merge.py
   ```

## 📝 File Structure

```
├── README.md
├── get_income_api.py
├── scrape_cost_of_living.py
├── clean_and_merge.py
├── cost_of_living.csv
├── state_income_datausa.csv
├── analytic_data2024.csv
└── final_dataset.csv
```

## 👩‍💻 Author

Lingyun (Judy) Hu  
USC DSCI-510 Final Project · Spring 2025
