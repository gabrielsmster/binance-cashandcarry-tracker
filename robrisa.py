import json
import requests
import telebot
from datetime import datetime

class RobrisaContangoReader:

    def __init__(self, pair_code=None, target=None):

        self.binance_secret = 'binance_api'
        self.telegram_secret = 'telegram_api'
        self.pair_code = pair_code
        self.target = target

    def connect_to_client(self, client):

        if client == 'binance':

            secret = session.client(service_name='secretsmanager', region_name='us-east-1'
                                    ).get_secret_value(SecretId=self.binance_secret)
            self.conn = Client(
                json.loads(secret['SecretString'])['API_KEY'],
                json.loads(secret['SecretString'])['SECRET_KEY']
            )

        elif client == 'telegram':

            secret = session.client(service_name='secretsmanager').get_secret_value(
                SecretId=self.telegram_secret
            )
            self.conn = telebot.TeleBot(json.loads(secret['SecretString'])['API_TOKEN_CONTANGO'])

    def check_premium(self):

        prices = self.get_prices()

        futuresInfo = []

        for contract in prices:
            if contract['symbol'][-4:] != 'PERP':
                future = {
                    'symbol': contract['symbol'],
                    'price': float(contract['markPrice']),
                    'premium': float(contract['markPrice']) / float(contract['indexPrice']) - 1,
                    'annual_premium': get_annual_premium(float(contract['markPrice']),
                                                         float(contract['indexPrice']),
                                                         get_days_maturity(contract['symbol'])),
                    'days': get_days_maturity(contract['symbol'])
                }

                if future['annual_premium'] > self.target or future['annual_premium'] < 0.1:
                    futuresInfo.append(future)

        return futuresInfo

    def get_prices(self):

        endpoint = 'https://dapi.binance.com'
        url = '/dapi/v1/premiumIndex?pair=' + self.pair_code

        avg_price = requests.get(endpoint + url)

        return avg_price.json()

    def notify_telegram_group(self, info):

        notification = 'Opportunity detected for {}: \n {}% at price {}'.format(
            info['symbol'], round(info['annual_premium'] * 100, 2), round(info['price'], 2))

        self.conn.send_message(-415473302, notification)


def get_days_maturity(symbol):
    year = '20' + symbol[-6:-4]
    month = symbol[-4:-2]
    day = symbol[-2:]

    maturity = datetime(int(year), int(month), int(day))
    days = abs((maturity - datetime.today()).days)

    return (days)


def get_annual_premium(mark, index, days):
    premium = mark / index - 1
    annual = premium * 360 / days

    return annual