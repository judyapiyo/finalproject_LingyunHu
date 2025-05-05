import pandas as pd

# Define paths
mental_health_path = "data/analytic_data2024.csv"
cost_path = "data/cost_of_living.csv"
income_path = "data/state_income_datausa.csv"

# Step 1: Load data
mental_df = pd.read_csv(mental_health_path, low_memory=False)
cost_df = pd.read_csv(cost_path, encoding="latin1")
income_df = pd.read_csv(income_path)

# Step 2: Clean column names
cost_df.columns = cost_df.columns.str.strip().str.replace("\xa0", " ").str.replace("\u200b", "")
income_df.columns = income_df.columns.str.strip()

# Step 3: Define state name to abbreviation map
state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
    'District of Columbia': 'DC'
}

# Step 4: Standardize state names in cost and income
cost_df["State"] = cost_df["State"].map(state_abbrev)
income_df["State"] = income_df["State"].map(state_abbrev)

# Step 5: Extract and rename columns
try:
    cost_df = cost_df[["State", "Cost of Living Index 2024"]]
except KeyError:
    real_col = [col for col in cost_df.columns if "Cost of Living Index" in col][0]
    cost_df = cost_df[["State", real_col]]
    cost_df.rename(columns={real_col: "Cost of Living Index 2024"}, inplace=True)

try:
    income_df = income_df[["State", "MedianHouseholdIncome"]]
except KeyError:
    real_income_col = [col for col in income_df.columns if "MedianHouseholdIncome" in col][0]
    income_df = income_df[["State", real_income_col]]
    income_df.rename(columns={real_income_col: "MedianHouseholdIncome"}, inplace=True)

# Step 6: Clean and group mental health data
valid_states = list(state_abbrev.values())
mental_df = mental_df[["State Abbreviation", "Frequent Mental Distress raw value"]]
mental_df = mental_df[mental_df["State Abbreviation"].isin(valid_states)]
mental_df["Frequent Mental Distress raw value"] = pd.to_numeric(
    mental_df["Frequent Mental Distress raw value"], errors="coerce"
)
mental_df = mental_df.groupby("State Abbreviation", as_index=False).mean()
mental_df.rename(columns={"State Abbreviation": "State"}, inplace=True)

# Step 7: Merge all three datasets
merged_df = mental_df.merge(cost_df, on="State", how="left")
merged_df = merged_df.merge(income_df, on="State", how="left")

# Step 8: Drop rows with missing values (optional)
merged_df.dropna(inplace=True)

# Step 9: Export result
merged_df.to_csv("output/merged_data.csv", index=False)
print("✅ 所有列都有值，州级数据合并完成，已保存为 output/merged_data.csv")
