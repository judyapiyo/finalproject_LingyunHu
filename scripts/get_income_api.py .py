import requests
import pandas as pd

# Data USA API endpoint
url = "https://datausa.io/api/data?drilldowns=State&measures=Median%20Household%20Income&year=latest"

print("📥 正在从 Data USA 获取数据...")
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    try:
        df = pd.DataFrame(data["data"])
        df = df[["State", "Year", "Median Household Income"]]
        df.columns = ["State", "Year", "MedianHouseholdIncome"]
        df.to_csv("state_income_datausa.csv", index=False)
        print("✅ 成功生成 state_income_datausa.csv")
    except KeyError:
        print("❌ 错误：API 返回不包含预期字段。")
else:
    print(f"❌ 请求失败，状态码：{response.status_code}")
