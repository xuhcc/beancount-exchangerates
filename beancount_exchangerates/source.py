import datetime
import json
import os
from urllib.parse import urljoin, urlencode
from urllib.request import Request, urlopen

from beancount.core.number import D

try:
    from beanprice import source
except ImportError:
    from beancount.prices import source

DEFAULT_PROVIDER = 'https://api.exchangerate.host'
EXCHANGERATE_API_URL = os.environ.get('EXCHANGERATE_API_URL', DEFAULT_PROVIDER)
DEFAULT_SOURCE = 'ecb'
SOURCE = os.environ.get('EXCHANGERATE_SOURCE', DEFAULT_SOURCE)


def to_decimal(number, precision):
    quant = D('0.' + '0' * precision)
    return D(number).quantize(quant)


class Source(source.Source):

    def _get_price(self, ticker, time=None):
        base, symbol = ticker.split(':')
        url_params = {
            'base': base,
            'symbols': symbol,
            'source': SOURCE
        }
        if time is None:
            date_str = 'latest'
        else:
            date_str = time.strftime('%Y-%m-%d')

        url = urljoin(EXCHANGERATE_API_URL, date_str) + '?' + urlencode(url_params)
        request = Request(url)
        # Requests without User-Agent header can be blocked
        request.add_header('User-Agent', 'price-fetcher')
        response = urlopen(request)
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
