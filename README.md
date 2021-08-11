# Beancount Exchange Rates

Price source for [Beancount](http://furius.ca/beancount/) that can load data from https://exchangerate.host/ or similar providers.

### exchangerate.host

This service uses datasets published by the European Central Bank.

List of supported forex currencies: https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html

No API key required.

## Installation

Install latest version with `pip`:

```
pip install https://github.com/xuhcc/beancount-exchangerates/archive/master.zip
```

## Usage

Source string format is `<quote-currency>:beancount_exchangerates/<base-currency>:<quote-currency>`.

Default API base url is https://api.exchangerate.host. It can be changed using `EXCHANGERATE_API_URL` environment variable.

Default source is ECB. It can be changed using `EXCHANGE_SOURCE` environment variable. Check https://api.exchangerate.host/sources for the complete list of sources.
### Examples

Evaluate source string with `bean-price`:

```
PYTHONPATH=.:$PYTHONPATH bean-price --no-cache -e 'RUB:beancount_exchangerates/USD:RUB'
```

Set price source for commodity in beancount file:

```
1970-01-01 commodity USD
    price: "RUB:beancount_exchangerates/USD:RUB"
```
