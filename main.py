import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv("data.env")

STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Fetch stock data
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()

if "Time Series (Daily)" not in data:
    print("⚠️ Error fetching stock data. Response:", data)
    exit()

# Extract recent closing prices
data_list = [value for (key, value) in data["Time Series (Daily)"].items()]
yesterday_data = data_list[0]
day_before_yesterday_data = data_list[1]

yesterday_closing_price = float(yesterday_data['4. close'])
day_before_yesterday_closing_price = float(day_before_yesterday_data['4. close'])

# Calculate movement
difference = yesterday_closing_price - day_before_yesterday_closing_price
diff_percent = (difference / day_before_yesterday_closing_price) * 100

direction = "🔺 UP" if difference > 0 else "🔻 DOWN"
print(f"{STOCK_NAME} moved {direction} by {abs(diff_percent):.2f}%")

# If movement is significant, fetch news
if abs(diff_percent) > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
        "language": "en",
        "pageSize": 3
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json().get("articles", [])

    if not articles:
        print("No news articles found.")
        exit()

    print("\n📰 Top News Headlines:")
    for a in articles:
        print(f"\nHeadline: {a['title']}\nBrief: {a['description']}\nURL: {a['url']}")
else:
    print("Change below threshold. No news fetched.")
