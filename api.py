################################################################################################################################################################################
import datetime
import pprint
import requests
import json
import decimal
import time
from dateutil.tz import gettz
import datetime as dt
from keys import *
from kusama import *
################################################################################################################################################################################



def API_key_check(api_key):
    pass






# Revisited funcs for API



# format coins
def format_coins_API(coins):
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
            return str(coins)
        else:
            return '0'
    except:
        return f'{coins}'


# format coins longer
def format_coins_longer_API(coins):
    if decimal.Decimal(coins) != 0:
        coins = str(coins)
        point = 0
        for i in coins:
            if i != '.':
                point += 1
            elif i == '.':
                break
        coins = str(coins)[:point + 8]
        return str(coins)

    else:
        return '0'



def raw_transfer_format_timestamp_API(timestamp):
    try:
        from datetime import datetime, date
        full_date = datetime.fromtimestamp(timestamp)
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
            day_message = '0'
        elif days_since == 1:
            day_message = '1'
        else:
            day_message = days_since
        return {'first_txn_full_date': first_txn_full_date, 'days_since': day_message}
    except IndexError:
        return {'first_txn_full_date': '-', 'days_since': '-'}







# SERER SETUP #######################################################################################################################################################
from json import dumps
from flask_cors import CORS
from flask import *
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})
# SERVER ###########################################################################################################################################################
# Home #############################################################################################################################################################
@app.route('/', methods=['GET'])
def home():
    USER_API_KEY = str(request.args.get('api_key'))
    API_key_check(USER_API_KEY)
    return Response(dumps({'wallety.org_server_status': 200}), mimetype='text/json')




# Chain-state #############################################################################################################################################################
@app.route('/chain-state', methods=['GET'])
def chain_state():
    USER_API_KEY = str(request.args.get('api_key'))
    API_key_check(USER_API_KEY)

    CURRENCY = str(request.args.get('currency'))
    if CURRENCY == "":
        # CURRENCY = "dollar"
        # do  later
        pass

    NETWORK = str(request.args.get('network'))
    if NETWORK == "polkadot":
        from polkadot import general_polkadot
        code_import = general_polkadot
    else:
        from kusama import general_kusama
        code_import = general_kusama
    CODE_IMPORT = code_import()['kusama_general']

    RETURN = {'coin_price': CODE_IMPORT[f'{NETWORK}_price'],
              'percentage_change_24hr': CODE_IMPORT[f'{NETWORK}_p_increase'],
              'market_cap': CODE_IMPORT[f'{NETWORK}_market_cap'],
              'transfer_count': CODE_IMPORT['recent_gas']['transfer_count'],
              'last_gas': {'coin_amount': CODE_IMPORT['recent_gas']['coin_gas_fee'], 'fiat_worth': CODE_IMPORT['recent_gas']['dollar_gas_fee']}
              }

    return Response(dumps(RETURN), mimetype='text/json')





# On chain identity #############################################################################################################################################################
@app.route('/on-chain-identity', methods=['GET'])
def on_chain_identity():
    USER_API_KEY = str(request.args.get('api_key'))
    API_key_check(USER_API_KEY)

    WALLET_ADDRESS = str(request.args.get('wallet_address'))

    NETWORK = str(request.args.get('network'))
    if NETWORK == "polkadot":
        from polkadot import polkadot_wallet_profile
        code_import = polkadot_wallet_profile
    else:
        from kusama import kusama_wallet_profile
        code_import = kusama_wallet_profile
    CODE_IMPORT = code_import(WALLET_ADDRESS)[0]['wallet_profile']['wallet_profile']

    RETURN = {"display_name": CODE_IMPORT['display_name'],
              "legal_name": CODE_IMPORT['legal_name'],
              "index": CODE_IMPORT['account_index'],
              "role": CODE_IMPORT['role'],
              "socials": {"twitter": CODE_IMPORT['twitter'], "website": CODE_IMPORT['website'], "email": CODE_IMPORT['email'], "element": CODE_IMPORT['riot']}
              }

    return Response(dumps(RETURN), mimetype='text/json')





# Balances #############################################################################################################################################################
@app.route('/balances', methods=['GET'])
def balances():
    USER_API_KEY = str(request.args.get('api_key'))
    API_key_check(USER_API_KEY)

    CURRENCY = str(request.args.get('currency'))
    if CURRENCY == "":
        # CURRENCY = "dollar"
        # do  later
        pass

    WALLET_ADDRESS = str(request.args.get('wallet_address'))

    NETWORK = str(request.args.get('network'))
    if NETWORK == "polkadot":
        from polkadot import polkadot_wallet_profile
        code_import = polkadot_wallet_profile
    else:
        from kusama import kusama_wallet_profile
        code_import = kusama_wallet_profile
    CODE_IMPORT = code_import(WALLET_ADDRESS)[0]['wallet_profile']['balances']

    RETURN = {
        "total_balance": {"coin": CODE_IMPORT['total_balance'], "fiat_worth": CODE_IMPORT['total_balance_dollars']},
        "transferable_balance": {"coin": CODE_IMPORT['transferable_balance'], "fiat_worth": CODE_IMPORT['transferable_balance_dollars']},
        "locked_balance": {"coin": CODE_IMPORT['locked_balance'], "fiat_worth": CODE_IMPORT['locked_balance_dollars']},
        "reserved_balance": {"coin": CODE_IMPORT['reserved_balance'], "fiat_worth": CODE_IMPORT['reserved_balance_dollars']}
        }

    return Response(dumps(RETURN), mimetype='text/json')




# Paper handed #############################################################################################################################################################
# Diamond handed #############################################################################################################################################################




# Other address formats #############################################################################################################################################################


@app.route('/other-address-formats', methods=['GET'])
def other_address_formats():
    USER_API_KEY = str(request.args.get('api_key'))
    API_key_check(USER_API_KEY)

    WALLET_ADDRESS = str(request.args.get('wallet_address'))

    from kusama import wallet_check
    code_import = wallet_check

    polkadot_address = code_import(WALLET_ADDRESS, 'polkadot')['wallet_network']['wallet_address']
    kusama_address = code_import(WALLET_ADDRESS, 'kusama')['wallet_network']['wallet_address']

    RETURN = {"polkadot_address": polkadot_address,
              "kusama_address": kusama_address
              }

    return Response(dumps(RETURN), mimetype='text/json')















# Transfer data #############################################################################################################################################################

@app.route('/other-address-formats', methods=['GET'])

def transfers(wallet_address, network):
    # the api request function for getting transfers
    def the_transfers():
        def all_transfer_req(page):
            url = f"https://{network}.api.subscan.io/api/scan/transfers"
            payload = json.dumps({
                "address": wallet_address,
                "row": 100,
                "page": page})
            headers = {
                'Content-Type': 'application/json',
                'X-API-Key': subscan_api_key}
            response = requests.request("POST", url, headers=headers, data=payload).text
            response = json.loads(response)
            return response

        all_transfers1 = []
        req = all_transfer_req(0)
        try:
            all_transfers1.extend(req['data']['transfers'])
        except TypeError:
            all_transfers1 = []

        transfer_count = float(req['data']['count'])
        pulled_transfer_count = float(len(all_transfers1))

        revolving_page = 1
        while pulled_transfer_count != transfer_count:
            try:
                req = all_transfer_req(revolving_page)
                time.sleep(1)
                all_transfers1.extend(req['data']['transfers'])
                pulled_transfer_count += float(len(req['data']['transfers']))
                revolving_page += 1
            except TypeError:
                break
        return all_transfers1

    # all wallet transfers
    all_transfers = the_transfers()
    all_withdraws = []
    all_deposits = []

    # organising into deposit and withdraws
    for i in all_transfers:
        if i['from'] == wallet_address:
            all_withdraws.append(i)
        else:
            all_deposits.append(i)


    deposit_transfers = []
    for i in all_deposits:
        display_name = kusama_wallet_short_name(i['from'])
        try:
            if i['from_account_display']['display'] != '':
                display_name = i['from_account_display']['display']
        except:
            pass
        full_wallet_address = i['from']
        coin_amount = i['amount']
        coin_worth_dollar = float(coin_amount) * float(kusama_price)
        gas = decimal_number_formatter(i['fee'])
        gas_dollar_worth = decimal.Decimal(gas) * decimal.Decimal(kusama_price)
        txn_time = raw_transfer_format_timestamp_API(i['block_timestamp'])
        days_since = txn_time['days_since']
        txn_time = txn_time['first_txn_full_date']
        # formatting dollars
        coin_worth_dollar = format_dollars(coin_worth_dollar)
        gas_dollar_worth = format_dollars_longer(gas_dollar_worth)
        # formatting coins
        coin_amount = format_coins_API(coin_amount)
        gas = format_coins_longer_API(gas)



        deposit_transfers.append({'display_name': display_name,
                                  'wallet_address': full_wallet_address,
                                  'deposited': coin_amount,
                                  'deposited_fiat_worth': coin_worth_dollar,
                                  'txn_time': txn_time,
                                  'days_since': days_since,
                                  'gas_fee': gas,
                                  'gas_dollar_worth': gas_dollar_worth
                                  })



    withdraw_transfers = []
    for i in all_withdraws:
        display_name = kusama_wallet_short_name(i['to'])
        try:
            if i['to_account_display']['display'] != '':
                display_name = i['to_account_display']['display']
        except:
            pass
        full_wallet_address = i['to']
        coin_amount = i['amount']
        coin_worth_dollar = float(coin_amount) * float(kusama_price)
        gas = decimal_number_formatter(i['fee'])
        gas_dollar_worth = decimal.Decimal(gas) * decimal.Decimal(kusama_price)
        txn_time = raw_transfer_format_timestamp_API(i['block_timestamp'])
        days_since = txn_time['days_since']
        txn_time = txn_time['first_txn_full_date']
        # formatting dollars
        coin_worth_dollar = format_dollars(coin_worth_dollar)
        gas_dollar_worth = format_dollars_longer(gas_dollar_worth)
        # formatting coins
        coin_amount = format_coins_API(coin_amount)
        gas = format_coins_longer_API(gas)


        withdraw_transfers.append({'coin_amount': coin_amount,
                                   'coin_worth_dollar': coin_worth_dollar,
                                   'display_name': display_name,
                                   'wallet_address': full_wallet_address,
                                   'txn_time': txn_time,
                                   'days_since': days_since,
                                   'gas_fee': gas,
                                   'gas_fee_fiat': gas_dollar_worth
                                   })


    return {'deposit_transfers': deposit_transfers, 'withdraw_transfers': withdraw_transfers}





# Unique wallets #############################################################################################################################################################











# RUN SERVER ##############################################################################################################################################################
if __name__ == '__main__':
    app.run(port=7777)


