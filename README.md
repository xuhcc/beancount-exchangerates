# Beancount Exchange Rates

Price source for [Beancount](http://furius.ca/beancount/) that loads data from http://exchangeratesapi.io/

http://exchangeratesapi.io/ uses datasets published by the European Central Bank. List of supported currencies: https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html

No API key required.

## Usage

Evaluate source string:

```
bean-price --no-cache -e 'RUB:beancount_exchangerates/USD_RUB'
```

Set price source for commodity in beancount file:

```
1970-01-01 commodity USD
    price: "RUB:beancount_exchangerates/USD_RUB"
```
