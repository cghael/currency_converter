import requests
import json


class CurrencyConverter:
    def __init__(self):
        self._amount = 0.00
        self._available_currency = None
        self._currency_cache = {}
        self._url = None

    def run(self):
        self._available_currency = self._input_currency()
        self._add_to_cashe()
        while True:
            exchange_currency = input().lower()
            if not exchange_currency:
                break
            self._amount = self._input_amount()
            self._checking_cashe(exchange_currency)
            receive = round(self._amount /
                            self._currency_cache[exchange_currency], 2)
            print(f"You received {receive} {exchange_currency.upper()}.")

    def _input_currency(self):
        while True:
            currency = input().lower()
            if len(currency) != 3:
                continue
            return currency

    def _input_amount(self):
        while True:
            try:
                amount = float(input())
                if amount < 0:
                    raise ValueError
                return amount
            except ValueError:
                continue

    def _add_to_cashe(self):
        rates = self._get_currency_rates()
        if self._available_currency != "usd":
            self._currency_cache["usd"] = rates["usd"]["inverseRate"]
        if self._available_currency != "eur":
            self._currency_cache["eur"] = rates["eur"]["inverseRate"]

    def _checking_cashe(self, exchange_currency):
        print("Checking the cache...")
        if exchange_currency not in self._currency_cache:
            print("Sorry, but it is not in the cache!")
            rate = self._get_currency_rates()
            self._currency_cache[exchange_currency] = \
                rate[exchange_currency]["inverseRate"]
        else:
            print("Oh! It is in the cache!")

    def _get_currency_rates(self):
        url = f"http://www.floatrates.com/daily/{self._available_currency}.json"
        try:
            response = json.loads(requests.get(url).content)
            if not response:
                raise ConnectionError
            return response
        except ConnectionError as err:
            print(err)


def main():
    converter = CurrencyConverter()
    converter.run()


if __name__ == "__main__":
    main()
