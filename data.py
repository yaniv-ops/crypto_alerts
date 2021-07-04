import requests
from time import sleep
from twilio.rest import Client

answer = {}

with open('config.txt', 'r') as data:



    for line in data:
        k, v = line.split()
        answer[k] = v



CURRENCIES_API = answer['CURRENCIES_API']
CURRENCIES_KEY = answer['CURRENCIES_KEY']
NEWS_API_KEY = answer['NEWS_API_KEY']
NEWS_END_POINT = answer['NEWS_END_POINT']
PHONE_NUMBER = answer['PHONE_NUMBER']
TWILIO_SID = answer['TWILIO_SID']
TWILIO_AUTH_TOKEN = answer['TWILIO_AUTH_TOKEN']
ids_coins = answer['ids_coins']
phone_to_send = answer['phone_to_send']

currecies_parameters = {
    "key": CURRENCIES_KEY,
    "ids": ids_coins,
}



market_is_on = True

while market_is_on:
    response = requests.get(CURRENCIES_API, params=currecies_parameters)
    currency_data = response.json()
    currency_change_sliced = currency_data[:]

    for coin in currency_change_sliced:



        currency_price = float(coin['price'])

        currency_change = float(coin['1d']['price_change'])

        price_change = (currency_price + currency_change) * 0.10

        if currency_change > 0:
            change = "😁"

        else:
            change = "😞"


        if abs(currency_change) >= price_change:


            news_parameters = {
            'apiKey': NEWS_API_KEY,
            'qinTitle': coin['name'],

            }

            response_news = requests.get(NEWS_END_POINT, params=news_parameters)
            news_data = response_news.json()['articles']


            coin_shout = [f"{coin['name']}: {currency_change/(currency_price + currency_change)*100}% {change}\n Headline: {article['title']}.\nBrief: {article['description']}" for article in news_data]

            client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
            for article in coin_shout:
                message = client.messages \
                    .create(
                    body=article,
                    from_=PHONE_NUMBER,
                    to=phone_to_send
                )

                print(message.sid)




    sleep(600)










