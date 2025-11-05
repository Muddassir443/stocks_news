import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv("data.env")

STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("from_")
TWILIO_TO = os.getenv("to")

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

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

data_list = [value for (key, value) in data["Time Series (Daily)"].items()]
yesterday_data = data_list[0]
day_before_yesterday_data = data_list[1]

yesterday_closing_price = float(yesterday_data['4. close'])
day_before_yesterday_closing_price = float(day_before_yesterday_data['4. close'])

difference = abs(yesterday_closing_price - day_before_yesterday_closing_price)
diff_percent = (difference / yesterday_closing_price) * 100
print(f"{STOCK_NAME} moved {diff_percent:.2f}%")

if diff_percent > 5:
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

    formatted_articles = [
        f"Headline: {a['title']}\nBrief: {a['description']}\nURL: {a['url']}"
        for a in articles
    ]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=TWILIO_FROM,
            to=TWILIO_TO
        )
        print(f"✅ Sent: {message.sid}")
else:
    print("Change below threshold. No news sent.")
