# Beancount Exchange Rates

Price source for [Beancount](http://furius.ca/beancount/) that can load data from <https://frankfurter.dev> or other providers with similar APIs, such as <https://fixer.io> or <https://exchangeratesapi.io> (both support more symbols than Frankfurter, but only support EUR as `base` currency, at least on their free plans).

## Providers

### frankfurter.dev

List of supported currencies: https://api.frankfurter.dev/v1/currencies

No API key required.

## Installation

Install latest version with `pip`:

```
pip install https://github.com/xuhcc/beancount-exchangerates/archive/master.zip
```

## Usage

Source string format is `<quote-currency>:beancount_exchangerates/<base-currency>:<quote-currency>`.

Default API base url is `https://api.frankfurter.dev/v1/`. It can be changed using `EXCHANGERATE_API_URL` environment variable (which should end with slash) to any service that implements Fixer API.

Use `EXCHANGERATE_ACCESS_KEY` to specify the `access_key` query parameter (not required by frankfurter.dev).

Data source can be changed using `EXCHANGERATE_SOURCE` environment variable.

### Examples

Evaluate source string with `bean-price`:

```
PYTHONPATH=.:$PYTHONPATH bean-price --no-cache -e 'CHF:beancount_exchangerates/USD:CHF'

EXCHANGERATE_API_URL=https://api.exchangeratesapi.io/v1/ EXCHANGERATE_ACCESS_KEY=... bean-price --no-cache -e 'EUR:beancount_exchangerates/EUR:XAU'
```

Set price source for commodity in beancount file:

```
1970-01-01 commodity USD
    price: "CHF:beancount_exchangerates/USD:CHF"
```

