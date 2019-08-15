import datetime
import json
from urllib.parse import urljoin, urlencode
from urllib.request import urlopen

from beancount.core.number import D
from beancount.prices import source

API_BASE_URL = 'https://api.exchangeratesapi.io/'


def to_decimal(number, precision):
    quant = D('0.' + '0' * precision)
    return D(number).quantize(quant)


class Source(source.Source):

    def _get_price(self, ticker, time=None):
        base, symbol = ticker.split('_')
        url_params = {
            'base': base,
            'symbols': symbol,
        }
        if time is None:
            date_str = 'latest'
        else:
            date_str = time.strftime('%Y-%m-%d')

        url = urljoin(API_BASE_URL, date_str) + '?' + urlencode(url_params)
        response = urlopen(url)
        result = json.loads(response.read().decode())

        price = to_decimal(result['rates'][symbol], 4)
        price_time = datetime.datetime.\
            strptime(result['date'], '%Y-%m-%d').\
            replace(tzinfo=datetime.timezone.utc)
        return source.SourcePrice(price, price_time, base)

    def get_latest_price(self, ticker):
        return self._get_price(ticker)

    def get_historical_price(self, ticker, time):
        return self._get_price(ticker, time)
