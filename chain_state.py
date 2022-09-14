import requests
import json
import decimal
from keys import *
from universal_functions import decimal_number_formatter, format_coins_longer, format_dollars_longer, currentDates


def chainState(network, coin_price):
    gecko = requests.get('https://api.coingecko.com/api/v3/coins/kusama').text
    gecko = json.loads(gecko)
    kusama_p_increase = gecko['market_data']['market_cap_change_percentage_24h']
    point = 0
    for i in str(kusama_p_increase):
        if i == '.':
            kusama_p_increase = str(kusama_p_increase)[:point + 3]
            break
        else:
            point += 1
    kusama_p_increase = str(kusama_p_increase) + '%'
    if str(kusama_p_increase)[0] != '-':
        kusama_p_increase = '+' + kusama_p_increase
    kusama_market_cap = gecko['market_data']['market_cap']['usd']

    def recent_gas():
        headers = {'X-API-Key': subscan_api_key}
        json_data = {
            'row': 1,
            'page': 0}
        response = requests.post(f'https://{network}.api.subscan.io/api/scan/transfers', headers=headers, json=json_data)
        response = json.loads(response.text)

        transfer_count = response['data']['count']
        transfer_count = format(int(transfer_count), ",")

        fee = response['data']['transfers'][0]['fee']
        fee = decimal_number_formatter(fee)
        coin_gas_fee = format_coins_longer(fee, network)

        dollar_gas_fee = decimal.Decimal(fee) * decimal.Decimal(coin_price)
        dollar_gas_fee = format_dollars_longer(dollar_gas_fee)
        dollar_gas_fee = format_dollars_longer(dollar_gas_fee)

        return {'coin_gas_fee': coin_gas_fee, 'dollar_gas_fee': dollar_gas_fee, 'transfer_count': transfer_count}

    Return = {'kusama_general': {'currentDates': currentDates(),
                                                'kusama_price': float(coin_price),
                                                'kusama_market_cap': kusama_market_cap,
                                                'recent_gas': recent_gas(),
                                                'kusama_p_increase': kusama_p_increase}}
    return Return

