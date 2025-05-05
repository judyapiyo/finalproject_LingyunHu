import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import sys

def scrape_data(limit=None):
    url = "https://worldpopulationreview.com/state-rankings/cost-of-living-index-by-state"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    headers = [th.text.strip() for th in table.find_all("th")]

    data = []
    for idx, row in enumerate(table.find_all("tr")[1:]):
        if limit is not None and idx >= limit:
            break
        cols = row.find_all("td")
        if len(cols) == len(headers):
            data.append([col.text.strip() for col in cols])

    df = pd.DataFrame(data, columns=headers)
    return df

def main():
    parser = argparse.ArgumentParser(description="Scrape cost of living index by U.S. state.")
    parser.add_argument("--scrape", type=int, help="Scrape the first N entries.")
    parser.add_argument("--save", type=str, help="Save the full scraped data to a CSV file.")
    args = parser.parse_args()

    if args.scrape is not None:
        df = scrape_data(limit=args.scrape)
        print(df.to_csv(index=False))
    elif args.save is not None:
        df = scrape_data()
        df.to_csv(args.save, index=False)
        print(f"✅ Data saved to {args.save}")
    else:
        df = scrape_data()
        print(df.to_csv(index=False))

if __name__ == "__main__":
    main()
