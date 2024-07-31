import logging
import requests
import datetime

from cashflow.errors import GeneralError

_log = logging.getLogger(__name__)


class Api(object):

    URL = 'https://api.forexrateapi.com'

    def __init__(self, api_key, url=URL, base_currency='CHF'):
        self.url = url
        self.base_currency = base_currency
        self.headers = {
            'Accept': 'application/json',
            'X-API-KEY': api_key
        }

    def request(self, path):
        url = self.url + path
        res = requests.request('GET', url=url, headers=self.headers)
        if not res.ok:
            raise self.Error("Request '{url}' failed!")
        return res.json()

    def get_latest(self, base, currencies):
        currency_list_str = ','.join(currencies)
        path = f'/v1/latest?base={base}&currencies={currency_list_str}'
        return self.request(path)

    def update_rates(self, currencies):
        if len(currencies) == 0:
            return
        currency_list = map(lambda cur: cur.code, currencies)
        rates = self.get_latest(self.base_currency, currency_list)
        if not rates['success']:
            raise self.Error(rates['error']['info'])
        date = datetime.datetime.fromtimestamp(rates['timestamp'])
        _log.info(f"Update currencies: {', '.join(currency_list)} ({date})")
        for currency in currencies:
            try:
                currency.rate = rates['rates'][currency.code]
            except KeyError:
                continue
            currency.date = date
            _log.info(f'Update currency: {currency}')


    class Error(GeneralError):
        pass


def install_forexrate_api(config):
    _log.debug('Install ForexRate API')
    settings = config.get_settings()
    api_key = settings.get('forexrate.api_key', 'UNKNOWN')
    def forexrate_api(request):
        _log.debug('Create ForexRate API')
        return Api(api_key)
    config.add_request_method(forexrate_api, reify=True)