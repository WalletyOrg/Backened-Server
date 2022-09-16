import datetime
import pprint
import requests
import json
import decimal
import time
from dateutil.tz import gettz
import datetime as dt
from keys import *
################################################################################################################################################################################




def report_analytic(network, wallet_address, display_name):
    try:
        from keys import kusama_test_addresss, polkadot_test_addresss
        clean_message = f'Site hit from: {display_name}\n' \
                        f'Calling: {network}\n' \
                        f'https://wallety.org/kusama?wallet_address={wallet_address}'
        if wallet_address not in kusama_test_addresss or polkadot_test_addresss:
            requests.get(f'https://api.telegram.org/bot{telegram_api_key}/sendMessage?chat_id={telegram_chat_id_report_clean}&text={clean_message}')
        return None
    except:
        return None




def currentDates():
    now = dt.datetime.now(gettz("Europe/London"))
    date = now.strftime('%A %d %B %Y')
    time = now.strftime('%I:%M:%S %p')
    time = str(time) + ' (BST)'
    date = date + ' ' + time
    short_date = now.strftime('%d-%m-%Y')
    return {'date': date, 'short_date': short_date}
def current_dates_short():
    now = dt.datetime.now(gettz("Europe/London"))
    date = now.strftime('%d/%m/%Y')
    return date





def decimal_number_formatter(number):
    if decimal.Decimal(number) != 0:
        coin_length = 12
        balance = str(number)
        balance_len = int(len(balance))
        if coin_length < balance_len:
            # full number
            extra_length = balance_len - coin_length
            whole_number = balance[:extra_length]
            decimal_number = balance[extra_length:]
            formatted_number = str(whole_number) + '.' + str(decimal_number)
            return decimal.Decimal(formatted_number)
        else:
            # decimal
            zeros = '0.000000000000'
            amount_need_to_add = int(coin_length - balance_len)
            formatted_number = str(zeros[:amount_need_to_add + 2]) + str(balance)
            return decimal.Decimal(formatted_number)
    else:
        return 0




# format new dollars
def format_dollars(dollars):
    if decimal.Decimal(dollars) != 0:
        dollars = str(dollars)
        point = 0
        for i in dollars:
            if i != '.':
                point += 1
            elif i == '.':
                break
        dollars = str(dollars)[:point + 3]
        return str(dollars)
    else:
        return 0
# format new dollars longer
def format_dollars_longer(dollars):
    if decimal.Decimal(dollars) != 0:
        dollars = str(dollars)
        point = 0
        for i in dollars:
            if i != '.':
                point += 1
            elif i == '.':
                break
        dollars = str(dollars[:9])
        return str(dollars)
    else:
        return 0



# get ticker
def getTicker(network):
    ticker = {'kusama': 'KSM', 'polkadot': 'DOT', 'acala': 'ACA', 'moonbeam': 'GLMR', 'astar': 'ASTR'}
    return ticker[network]





# format coins
def format_coins(coins, network):
    ticker = getTicker(network)
    try:
        if decimal.Decimal(coins) != 0 and decimal.Decimal(coins) >= decimal.Decimal(0.0001):
            coins = str(coins)
            point = 0
            for i in coins:
                if i != '.':
                    point += 1
                elif i == '.':
                    break
            coins = coins[:point + 5]
            coins = format(float(coins), ",")
            coins = str(coins) + f' {ticker}'
            return str(coins)
        else:
            return f'0 {ticker}'
    except:
        return f'{coins} {ticker}'
# formatting machine coins
def format_coins_machine(coins):
    try:
        if decimal.Decimal(coins) != 0 and decimal.Decimal(coins) >= decimal.Decimal(0.0001):
            coins = str(coins)
            point = 0
            for i in coins:
                if i != '.':
                    point += 1
                elif i == '.':
                    break
            coins = coins[:point + 5]
            return float(coins)
        else:
            return 0
    except:
        return float(coins)
# format coins longer
def format_coins_longer(coins, network):
    ticker = getTicker(network)
    if decimal.Decimal(coins) != 0:
        coins = str(coins)
        point = 0
        for i in coins:
            if i != '.':
                point += 1
            elif i == '.':
                break
        coins = str(coins)[:point + 8]
        coins = str(coins) + f' {ticker}'
        return str(coins)

    else:
        return f'0 {ticker}'






# format percentage
def percentage_format(percentage):
    if float(percentage) != 0:
        percentage = str(percentage)
        point = 0
        for i in percentage:
            if i != '.':
                point += 1
            elif i == '.':
                break
        percentage = str(percentage)[:point + 6]
        percentage = str(percentage) + '%'
        return percentage
    else:
        return '0.00%'





# first txn times
def first_txn_dates(transfers):
    try:
        from datetime import datetime, date
        # first txn time
        last_txn = len(transfers) - 1
        first_txn_stamp = transfers[last_txn]['block_timestamp']
        full_date = datetime.fromtimestamp(first_txn_stamp)
        first_txn_full_date = full_date.strftime("%d/%m/%Y %I:%M:%S %p")
        first_txn_full_date = str(first_txn_full_date) + ' BST'
        # calculating days since
        date_format = "%m/%d/%Y"
        # today
        today = date.today()
        today = today.strftime("%m/%d/%Y")
        today = datetime.strptime(today, date_format)
        # first txn
        first_txn_date = full_date.strftime("%m/%d/%Y")
        first_txn_date = datetime.strptime(first_txn_date, date_format)
        # calculating days_since since
        delta = today - first_txn_date
        days_since = delta.days

        if days_since == 0:
            day_message = '(today)'
        elif days_since == 1:
            day_message = '(1 day ago)'
        else:
            day_message = '({} days ago)'.format(days_since)
        return {'first_txn_full_date': first_txn_full_date, 'days_since': day_message}
    except IndexError:
        return {'first_txn_full_date': '-', 'days_since': '-'}
# timestamp converter
def timestamp_converter(block_timestamp):
    from datetime import datetime
    full_date = datetime.fromtimestamp(block_timestamp)
    date = full_date.strftime("%d/%m/%Y")
    return date
# timestamp seconds converter
def timestamp_converter_seconds(block_timestamp):
    from datetime import datetime
    full_date = datetime.fromtimestamp(block_timestamp)
    date = full_date.strftime("%d/%m/%Y %I:%M:%S %p")
    date = str(date) + ' (BST)'
    return date

# last txn times
def last_txn_dates(transfers):
    try:
        from datetime import datetime, date
        # first txn time
        last_txn_stamp = transfers[0]['block_timestamp']
        full_date = datetime.fromtimestamp(last_txn_stamp)
        last_txn_full_date = full_date.strftime("%d/%m/%Y %I:%M:%S %p")
        last_txn_full_date = str(last_txn_full_date) + ' BST'
        # calculating days since
        date_format = "%m/%d/%Y"
        # today
        today = date.today()
        today = today.strftime("%m/%d/%Y")
        today = datetime.strptime(today, date_format)
        # first txn
        last_txn_date = full_date.strftime("%m/%d/%Y")
        last_txn_date = datetime.strptime(last_txn_date, date_format)
        # calculating days_since since
        delta = today - last_txn_date
        days_since = delta.days
        if days_since == 0:
            day_message = '(today)'
        elif days_since == 1:
            day_message = '(1 day ago)'
        else:
            day_message = '({} days ago)'.format(days_since)
        return {'last_txn_full_date': last_txn_full_date, 'days_since': day_message}
    except IndexError:
        return {'last_txn_full_date': '-', 'days_since': '-'}




# short wallet name
def wallet_short_name(address):
    short_name = '{}...{}'.format(str(address)[:7], str(address)[40:47])
    return short_name





def walletCheck(wallet_address, specified_network):
    def network_check(network, wallet_address):
        url = f"https://{network}.api.subscan.io/api/v2/scan/search"
        payload = json.dumps({"key": wallet_address})
        headers = {'Content-Type': 'application/json', 'X-API-Key': subscan_api_key}
        response = requests.request("POST", url, headers=headers, data=payload).text
        response = json.loads(response)
        network_response = False
        if response['message'] == 'Record Not Found':
            network_response = False
        elif response['data']['account']['address'] == wallet_address:
            network_response = network
        elif response['message'] != 'Record Not Found' and specified_network != 'all':
            network_response = specified_network
        elif response['message'] != 'Record Not Found' and specified_network == 'all':
            network_response = 'polkadot' # default to Polkadot
        try:
            wallet_address = response['data']['account']['address']
        except KeyError:
            wallet_address = False
        network_data = {'network_response': network_response, 'wallet_address': wallet_address}
        return network_data
    network = {'network': False, 'wallet_address': False}
    polkadot_check = network_check('polkadot', wallet_address)
    if polkadot_check['network_response'] == 'polkadot':
        network = {'network': 'polkadot', 'wallet_address': polkadot_check['wallet_address']}
    else:
        kusama_check = network_check('kusama', wallet_address)
        if kusama_check['network_response'] == 'kusama':
            network = {'network': 'kusama', 'wallet_address': kusama_check['wallet_address']}
    return {'wallet_network': network}






# coin price
def coinPrice(network):
    price_req = requests.get(f'https://api.coingecko.com/api/v3/coins/{network}').text
    price_req = json.loads(price_req)
    price_req = price_req['market_data']['current_price']['usd']
    return price_req


