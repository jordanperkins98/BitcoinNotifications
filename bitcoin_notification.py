from requests import Request, Session
import json
import time
from datetime import datetime

BITCOIN_PRICE_THRESHOLD = 105
BITCOIN_API_URL ='https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/jOM9YJKcNZ01TBEKU0h0-VveSjP4E95_Nr7_IV-Mdsu'


def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string: '24.02.2018 15:09'
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        # <b> (bold) tag creates bolded text
        # 24.02.2018 15:09: $<b>10123.4</b>
        row = f'{date}: £<b>{price:.2f}</b>'
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    # Join the rows delimited by <br> tag: row1<br>row2<br>row3
    return '<br>'.join(rows)


def get_latest_bitcoin_price():
    
    parameters = {
    'symbol':'ETH',
    'convert':'GBP'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'acaa9f45-0308-4957-a6b1-8ebb532550c3',
    }

    session = Session()
    session.headers.update(headers)
    response = session.get(BITCOIN_API_URL, params=parameters)
    data = json.loads(response.text)

    return(data['data']['ETH']['quote']['GBP']['price'])
    
def post_ifttt_webhook(event,value):
    session = Session()
    data = {'value1': value}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    session.post(ifttt_event_url, json=data)

def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

          # Send an emergency notification
        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency',price)
        
        # Send a Telegram notification
        # Once we have 5 items in our bitcoin_history send an update
        if len(bitcoin_history) == 5:
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
            # Reset the history
            bitcoin_history = []
        # Sleep for 5 minutes
        time.sleep(5 * 60)

if __name__ == '__main__':
    main()



