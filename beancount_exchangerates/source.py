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

DEFAULT_PROVIDER = 'https://api.frankfurter.dev/v1/'
EXCHANGERATE_API_URL = os.environ.get('EXCHANGERATE_API_URL', DEFAULT_PROVIDER)
EXCHANGERATE_ACCESS_KEY = os.environ.get('EXCHANGERATE_ACCESS_KEY')
EXCHANGERATE_SOURCE = os.environ.get('EXCHANGERATE_SOURCE')
EXCHANGERATE_DEFAULTS = os.environ.get('EXCHANGERATE_DEFAULTS')


# TODO Should really use the precision set on a commodity in Beancount instead of hard-coding something...
# NB: The hard-coded precision of 12 is chosen because that's what Fixer.io & exchangeratesapi.io use for BTC.
def to_decimal(number, precision=12):
    quant = D('0.' + '0' * precision)
    return D(number).quantize(quant)


def get_default_price(ticker):
    """
    Will be used if provider doesn't support given currency
    """
    if EXCHANGERATE_DEFAULTS is not None:
        for pair in EXCHANGERATE_DEFAULTS.split(','):
            key, value = pair.split('=')
            if key == ticker:
                return to_decimal(value)


class Source(source.Source):

    def _get_price(self, ticker, time=None):
        base, symbol = ticker.split(':')
        url_params = {
            'base': base,
            'symbols': symbol,
        }
        if EXCHANGERATE_ACCESS_KEY is not None:
            url_params['access_key'] = EXCHANGERATE_ACCESS_KEY
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
        except HTTPError as err:
            price = get_default_price(ticker)
            if not price:
                message = f"HTTP Error: {err.code} for URL: {err.url}"
                raise RuntimeError(message) from err
            price_time = datetime.datetime.now(datetime.timezone.utc)
        else:
            result = json.loads(response.read().decode())
            try:
                price = to_decimal(result['rates'][symbol])
            except KeyError as err:
                message = f"Missing key {str(err)}: {str(result)}"
                raise RuntimeError(message) from err
            price_time = datetime.datetime.\
                strptime(result['date'], '%Y-%m-%d').\
                replace(tzinfo=datetime.timezone.utc)
        return source.SourcePrice(price, price_time, base)

    def get_latest_price(self, ticker):
        return self._get_price(ticker)

    def get_historical_price(self, ticker, time):
        return self._get_price(ticker, time)
