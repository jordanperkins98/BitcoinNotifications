
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  'symbol':'BTC',
  'convert':'GBP'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'acaa9f45-0308-4957-a6b1-8ebb532550c3',
}

session = Session()
session.headers.update(headers)
response = session.get(url, params=parameters)
data = json.loads(response.text)
print(data['data']['BTC']['quote']['GBP']['price'])
