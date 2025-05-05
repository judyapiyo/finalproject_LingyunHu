import pandas as pd

# === Load raw CSVs ===
income_df = pd.read_csv("/Users/judyhu/Desktop/state_income_datausa.csv")
cost_df = pd.read_csv("/Users/judyhu/Desktop/cost_of_living.csv")
mental_df = pd.read_csv("/Users/judyhu/Desktop/analytic_data2024.csv")

# === Clean column names ===
cost_df.columns = [col.strip().replace('\x86', '').replace('\x93', '') for col in cost_df.columns]

# === Keep only relevant columns ===
income_df = income_df[["State", "Year", "MedianHouseholdIncome"]]
cost_df = cost_df[["State", "Cost of Living Index 2024"]]
mental_df = mental_df.rename(columns={"State": "State", "v060_rawvalue": "PoorMentalHealthDays"})

# === Group mental_df to state-level average mental health ===
mental_state_df = mental_df.groupby("State", as_index=False)["PoorMentalHealthDays"].mean()

# === Merge all data ===
merged = income_df.merge(cost_df, on="State")
merged = merged.merge(mental_state_df, on="State")

# === Save cleaned and merged CSV ===
merged.to_csv("/Users/judyhu/Desktop/final_cleaned_data.csv", index=False)
print("✅ 清洗完成，已保存为 final_cleaned_data.csv")
