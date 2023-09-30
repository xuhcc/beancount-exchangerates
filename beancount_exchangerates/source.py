import datetime
import json
import os
from urllib.error import HTTPError
from urllib.parse import urljoin, urlencode
from urllib.request import Request, urlopen

from beancount.core.number import D

try:
    from beanprice import source
except ImportError:
    from beancount.prices import source

DEFAULT_PROVIDER = 'https://api.frankfurter.app'
EXCHANGERATE_API_URL = os.environ.get('EXCHANGERATE_API_URL', DEFAULT_PROVIDER)
EXCHANGERATE_SOURCE = os.environ.get('EXCHANGERATE_SOURCE')
EXCHANGERATE_DEFAULTS = os.environ.get('EXCHANGERATE_DEFAULTS')


def to_decimal(number, precision=4):
    quant = D('0.' + '0' * precision)
    return D(number).quantize(quant)


def get_default(symbol):
    if EXCHANGERATE_DEFAULTS is not None:
        for pair in EXCHANGERATE_DEFAULTS.split(','):
            key, value = pair.split('=')
            if key == symbol:
                return to_decimal(value)


class Source(source.Source):

    def _get_price(self, ticker, time=None):
        base, symbol = ticker.split(':')
        url_params = {
            'base': base,
            'symbols': symbol,
        }
        if EXCHANGERATE_SOURCE is not None:
            url_params['source'] = EXCHANGERATE_SOURCE
        if time is None:
            date_str = 'latest'
        else:
            date_str = time.strftime('%Y-%m-%d')

        url = urljoin(EXCHANGERATE_API_URL, date_str) + '?' + urlencode(url_params)
        request = Request(url)
        # Requests without User-Agent header can be blocked
        request.add_header('User-Agent', 'price-fetcher')
        try:
            response = urlopen(request)
        except HTTPError:
            price = get_default(symbol)
            if not price:
                raise
            price_time = datetime.datetime.now(datetime.timezone.utc)
        else:
            result = json.loads(response.read().decode())
            price = to_decimal(result['rates'][symbol])
            price_time = datetime.datetime.\
                strptime(result['date'], '%Y-%m-%d').\
                replace(tzinfo=datetime.timezone.utc)
        return source.SourcePrice(price, price_time, base)

    def get_latest_price(self, ticker):
        return self._get_price(ticker)

    def get_historical_price(self, ticker, time):
        return self._get_price(ticker, time)
