import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "V0LQQUH9UV5AYAU2"
STOCK_API_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_API_KEY = "7f8696c92fcf4d59bcc14c9e3d688816"
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
SMS_ACC_SID = "ACfc37337505347e37ea7a3c40fb822625"
SMS_AUTH_TOKEN = "82ec6e7076da6fe79e0ecb507b452bde"



## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}
stock_response = requests.get(url=STOCK_API_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()
data_list = [value for (key, value) in stock_data["Time Series (Daily)"].items()]

yesterday_data = data_list[0]
yesterday_price = float(yesterday_data["4. close"])

day_before_yesterday_data = data_list[1]
day_before_yesterday_price = float(day_before_yesterday_data["4. close"])
difference = yesterday_price-day_before_yesterday_price
diff = abs(difference)
diff_percent = (diff/yesterday_price)*100

if diff_percent > 1:

    ## STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    news_parameters = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
        "searchln": "title",
    }
    news_response = requests.get(url=NEWS_API_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    articles = news_response.json()["articles"][:3]




    ## STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.
    formatted_articles = [f"Headline: {article['title']}, \n Brief: {article['description']}" for article in articles]
    client = Client(SMS_ACC_SID, SMS_AUTH_TOKEN)
    if diff > 0:
        symbol = "🔼"
    else:
        symbol = "⬇"
    for article_send in formatted_articles:
        message = client.messages \
            .create(
            body=f"{symbol} {round(diff_percent)}%\n"+article_send,
            from_ = "+13465507115",
            to = '+919979231095'
        )

        print(message.status)





