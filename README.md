# Beancount Exchange Rates

Price source for [Beancount](http://furius.ca/beancount/) that can load data from https://exchangerate.host/ or similar providers.

### exchangerate.host

List of supported forex currencies: https://api.exchangerate.host/symbols

No API key required.

## Installation

Install latest version with `pip`:

```
pip install https://github.com/xuhcc/beancount-exchangerates/archive/master.zip
```

## Usage

Source string format is `<quote-currency>:beancount_exchangerates/<base-currency>:<quote-currency>`.

Default API base url is `https://api.frankfurter.dev/v1/`. It can be changed using `EXCHANGERATE_API_URL` environment variable (which should end with slash) to any service that implements Fixer API.

Use `EXCHANGERATE_ACCESS_KEY` to specify the `?access_key=` (if any; e.g. Frankfurter.dev does not, but e.g. ExchangeRatesAPI.io does).

Data source can be changed using `EXCHANGERATE_SOURCE` environment variable.

Check https://api.exchangerate.host/sources for the complete list of sources.

### Examples

Evaluate source string with `bean-price`:

```
PYTHONPATH=.:$PYTHONPATH bean-price --no-cache -e 'CHF:beancount_exchangerates/USD:CHF'
```

Set price source for commodity in beancount file:

```
1970-01-01 commodity USD
    price: "CHF:beancount_exchangerates/USD:CHF"
```
