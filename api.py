##############################################################################################################################################################################
from kusama import *
from key_check import *
# Revisited funcs for API ##############################################################################################################################################################################



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
        return {'first_txn_full_date': '', 'days_since': ''}








# first txn times
def first_txn_dates_API(transfers):
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
            day_message = '0'
        elif days_since == 1:
            day_message = '1'
        else:
            day_message = days_since
        return {'first_txn_full_date': first_txn_full_date, 'days_since': day_message}
    except IndexError:
        return {'first_txn_full_date': '', 'days_since': ''}




# last txn times
def last_txn_dates_API(transfers):
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
            day_message = '0'
        elif days_since == 1:
            day_message = '1'
        else:
            day_message = days_since
        return {'last_txn_full_date': last_txn_full_date, 'days_since': day_message}
    except IndexError:
        return {'last_txn_full_date': '', 'days_since': ''}






# format percentage
def percentage_format_API(percentage):
    if float(percentage) != 0:
        percentage = str(percentage)
        point = 0
        for i in percentage:
            if i != '.':
                point += 1
            elif i == '.':
                break
        percentage = str(percentage)[:point + 6]
        percentage = str(percentage)
        return percentage
    else:
        return '0'




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
    API_key_check(USER_API_KEY, 'Server Check', 401)
    return Response(dumps({'wallety.org_server_status': 200}), mimetype='text/json')




# Chain-state #############################################################################################################################################################
@app.route('/chain-state', methods=['GET'])
def chain_state():
    USER_API_KEY = str(request.args.get('api_key'))
    API_key_check(USER_API_KEY, 'Chain State', 401)

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
    WALLET_ADDRESS = str(request.args.get('wallet_address'))

    USER_API_KEY = str(request.args.get('api_key'))
    API_key_check(USER_API_KEY, 'On Chain Identity', WALLET_ADDRESS)

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
    WALLET_ADDRESS = str(request.args.get('wallet_address'))

    USER_API_KEY = str(request.args.get('api_key'))
    API_key_check(USER_API_KEY, 'Balances', WALLET_ADDRESS)

    CURRENCY = str(request.args.get('currency'))
    if CURRENCY == "":
        # CURRENCY = "dollar"
        # do  later
        pass

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




# Paper diamond handed #############################################################################################################################################################
@app.route('/paper-diamond-handed', methods=['GET'])
def paper_diamond_handed():
    WALLET_ADDRESS = str(request.args.get('wallet_address'))

    USER_API_KEY = str(request.args.get('api_key'))
    API_key_check(USER_API_KEY, 'Paper Diamond Handed', WALLET_ADDRESS)

    NETWORK = str(request.args.get('network'))

    # the api request function for getting transfers
    def the_transfers():
        def all_transfer_req(page):
            url = f"https://{NETWORK}.api.subscan.io/api/scan/transfers"
            payload = json.dumps({
                "address": WALLET_ADDRESS,
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
        if i['from'] == WALLET_ADDRESS:
            all_withdraws.append(i)
        else:
            all_deposits.append(i)



    paper_handed_coins = 0
    for i in all_withdraws:
        paper_handed_coins += float(i['amount'])

    # paperhanded dollar amounts and formatting numbers
    paper_handed_coins_dollars = float(kusama_price) * float(paper_handed_coins)

    # formatting numbers
    paper_handed_coins = format_coins_API(paper_handed_coins)
    paper_handed_coins_dollars = format_dollars(paper_handed_coins_dollars)


    # diamond handed
    url = "https://kusama.api.subscan.io/api/v2/scan/search"
    payload = json.dumps({"key": WALLET_ADDRESS})
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': subscan_api_key}
    response = requests.request("POST", url, headers=headers, data=payload).text
    response = json.loads(response)

    # balances
    total_balance = response['data']['account']['balance']
    locked_balance = response['data']['account']['balance_lock']
    reserved_balance = response['data']['account']['reserved']
    reserved_balance = decimal_number_formatter(reserved_balance)
    transferable_balance = (float(total_balance) - float(locked_balance)) - float(reserved_balance)

    # balances for handed coins later on
    diamond_handed_coins = float(transferable_balance) + float(locked_balance)
    diamond_handed_coins_dollars = float(kusama_price) * float(diamond_handed_coins)
    diamond_handed_coins = format_coins_API(diamond_handed_coins)
    diamond_handed_coins_dollars = format_dollars(diamond_handed_coins_dollars)

    return {'paper_handed': {'paper_handed_coins': paper_handed_coins,
                             'paper_handed_coins_fiat_worth': paper_handed_coins_dollars},

            'diamond_handed': {'diamond_handed_coins': diamond_handed_coins,
                               'diamond_handed_coins_fiat_worth': diamond_handed_coins_dollars}
            }





# Other address formats #############################################################################################################################################################


@app.route('/other-address-formats', methods=['GET'])
def other_address_formats():
    WALLET_ADDRESS = str(request.args.get('wallet_address'))

    USER_API_KEY = str(request.args.get('api_key'))
    API_key_check(USER_API_KEY, 'Other Address Formats', WALLET_ADDRESS)

    from kusama import wallet_check
    code_import = wallet_check

    polkadot_address = code_import(WALLET_ADDRESS, 'polkadot')['wallet_network']['wallet_address']
    kusama_address = code_import(WALLET_ADDRESS, 'kusama')['wallet_network']['wallet_address']

    RETURN = {"polkadot_address": polkadot_address,
              "kusama_address": kusama_address
              }

    return Response(dumps(RETURN), mimetype='text/json')






# Transfer data #############################################################################################################################################################

@app.route('/transfers', methods=['GET'])
def transfers():
    WALLET_ADDRESS = str(request.args.get('wallet_address'))

    USER_API_KEY = str(request.args.get('api_key'))
    API_key_check(USER_API_KEY, 'Transfers', WALLET_ADDRESS)

    CURRENCY = str(request.args.get('currency'))
    if CURRENCY == "":
        # CURRENCY = "dollar"
        # do  later
        pass

    NETWORK = str(request.args.get('network'))


    # the api request function for getting transfers
    def the_transfers():
        def all_transfer_req(page):
            url = f"https://{NETWORK}.api.subscan.io/api/scan/transfers"
            payload = json.dumps({
                "address": WALLET_ADDRESS,
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
        if i['from'] == WALLET_ADDRESS:
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




@app.route('/unique-wallets', methods=['GET'])
def unique_wallets():

    WALLET_ADDRESS = str(request.args.get('wallet_address'))

    USER_API_KEY = str(request.args.get('api_key'))
    API_key_check(USER_API_KEY, 'Unique Wallets', WALLET_ADDRESS)

    CURRENCY = str(request.args.get('currency'))
    if CURRENCY == "":
        # CURRENCY = "dollar"
        # do  later
        pass

    NETWORK = str(request.args.get('network'))


    # the api request function for getting transfers
    def the_transfers():
        def all_transfer_req(page):
            url = f"https://{NETWORK}.api.subscan.io/api/scan/transfers"
            payload = json.dumps({
                "address": WALLET_ADDRESS,
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
        if i['from'] == WALLET_ADDRESS:
            all_withdraws.append(i)
        else:
            all_deposits.append(i)



    def top_accounts(wallet_address, transfers, withdraw_or_deposit):

        w_d_indicator = withdraw_or_deposit
        if withdraw_or_deposit == "withdraw":
            withdraw_or_deposit = 'to'
            account_display = 'to_account_display'
        else:
            withdraw_or_deposit = 'from'
            account_display = 'from_account_display'

        # unique wallet data
        coin_amount = {}
        fees_coin = {}
        fees_dollars = {}
        interacted_times = {}
        wallet_names = {}
        failed_interacted_times = {}

        rawFLtxns = {}

        for index, i in enumerate(transfers):
            if i[withdraw_or_deposit] != wallet_address:
                # first time add
                if i[withdraw_or_deposit] not in coin_amount:
                    # only adds coins and dollars if true but gas was paid so its added
                    if i['success'] == True:
                        coin_amount[i[withdraw_or_deposit]] = float(i['amount'])
                        failed_interacted_times[i[withdraw_or_deposit]] = 0
                    else:
                        coin_amount[i[withdraw_or_deposit]] = float(0)
                        failed_interacted_times[i[withdraw_or_deposit]] = 1

                    fees_coin[i[withdraw_or_deposit]] = decimal_number_formatter(i['fee'])
                    fees_dollars[i[withdraw_or_deposit]] = decimal_number_formatter(i['fee']) * decimal.Decimal(kusama_price)
                    interacted_times[i[withdraw_or_deposit]] = 1

                    try:
                        if i[account_display]['identity']:
                            wallet_names[i[withdraw_or_deposit]] = i[account_display]['display']
                        else:
                            wallet_names[i[withdraw_or_deposit]] = kusama_wallet_short_name(i[withdraw_or_deposit])
                    except:
                        wallet_names[i[withdraw_or_deposit]] = kusama_wallet_short_name(i[withdraw_or_deposit])

                # adding onto original value
                else:
                    if i['success'] == True:
                        coin_amount[i[withdraw_or_deposit]] = float(float(coin_amount[i[withdraw_or_deposit]]) + float(i['amount']))
                        interacted_times[i[withdraw_or_deposit]] += 1
                    else:
                        failed_interacted_times[i[withdraw_or_deposit]] += 1
                        interacted_times[i[withdraw_or_deposit]] += 1

                    fees_coin[i[withdraw_or_deposit]] = fees_coin[i[withdraw_or_deposit]] + decimal_number_formatter(i['fee'])
                    fees_dollars[i[withdraw_or_deposit]] = decimal.Decimal(fees_coin[i[withdraw_or_deposit]]) * decimal.Decimal(kusama_price)

                if i[withdraw_or_deposit] not in rawFLtxns:
                    rawFLtxns[i[withdraw_or_deposit]] = [i]
                else:
                    rawFLtxns[i[withdraw_or_deposit]].append(i)

        # unique txn info
        total_coin_volume = 0
        for i in coin_amount.items():
            total_coin_volume += float(i[1])

        coin_pi_chart_percentage = {}

        for i in coin_amount.items():
            coin_pi_chart_percentage[i[0]] = (format_coins_machine(i[1]) / total_coin_volume) * 100

        # making the lists
        data = {}
        # unformatted data
        for address, coin_amount1 in coin_amount.items():
            i = {f'{w_d_indicator}_address': address,
                 f'{w_d_indicator}_coin_amount': coin_amount1,
                 f'{w_d_indicator}_pi_chart_percent': coin_pi_chart_percentage[address],
                 f'{w_d_indicator}_coin_fee': fees_coin[address],
                 f'{w_d_indicator}_coin_fee_dollars': fees_dollars[address],
                 f'{w_d_indicator}_interaction_times': interacted_times[address],
                 f'{w_d_indicator}_failed_interaction_times': failed_interacted_times[address],
                 f'{w_d_indicator}_display_name': wallet_names[address],
                 'XXX_coin_volume': total_coin_volume
                 }
            # unformatted data
            data[address] = i
        unformatted_data = data

        # formatted data
        data = {}
        for address, coin_amount in coin_amount.items():
            i = {f'{w_d_indicator}_address': address,
                 f'{w_d_indicator}_coin_amount': coin_amount,
                 f'{w_d_indicator}_pi_chart_percent': coin_pi_chart_percentage[address],
                 f'{w_d_indicator}_coin_fee': fees_coin[address],
                 f'{w_d_indicator}_coin_fee_dollars': fees_dollars[address],
                 f'{w_d_indicator}_interaction_times': interacted_times[address],
                 f'{w_d_indicator}_failed_interaction_times': failed_interacted_times[address],
                 f'{w_d_indicator}_display_name': wallet_names[address]
                 }
            # formatted data
            data[address] = i

        return {'data': data}, {f'{w_d_indicator}_unformatted_data': unformatted_data}, {'rawFLtxns': rawFLtxns}



    # some data
    # ALL total deposits
    deposits_data = top_accounts(WALLET_ADDRESS, all_deposits, 'deposit')
    deposits = deposits_data[0]
    deposits_rawFLtxns = deposits_data[2]
    # ALL total withdrawals
    withdrawals_data = top_accounts(WALLET_ADDRESS, all_withdraws, 'withdraw')
    withdrawals = withdrawals_data[0]
    withdrawals_rawFLtxns = withdrawals_data[2]




    # formatting total deposits data
    deposits_formatted = []
    for i in deposits['data'].items():
        tier = i[1]
        deposit_display_name = tier['deposit_display_name']
        deposit_address = tier['deposit_address']
        deposit_dollar_amount = format_dollars(format_coins_machine(tier['deposit_coin_amount']) * float(kusama_price))
        deposit_coin_amount = format_coins_API(tier['deposit_coin_amount'])
        deposit_pi_chart_percent = percentage_format_API(tier['deposit_pi_chart_percent'])
        deposit_coin_fee = format_coins_longer_API(tier['deposit_coin_fee'])
        deposit_coin_fee_dollars = format_dollars_longer(tier['deposit_coin_fee_dollars'])
        deposit_interaction_times = tier['deposit_interaction_times']
        deposit_failed_interaction_times = tier['deposit_failed_interaction_times']
        deposit_first_txn = first_txn_dates_API(deposits_rawFLtxns['rawFLtxns'][tier['deposit_address']])
        first_txn = deposit_first_txn['first_txn_full_date']
        first_days_since = deposit_first_txn['days_since']
        deposit_last_txn = last_txn_dates_API(deposits_rawFLtxns['rawFLtxns'][tier['deposit_address']])
        last_txn = deposit_last_txn['last_txn_full_date']
        last_days_since = deposit_last_txn['days_since']


        deposits_formatted.append({'display_name': deposit_display_name,
                                   'wallet_address': deposit_address,
                                   'coin_amount': deposit_coin_amount,
                                   'coin_amount_fiat_worth': deposit_dollar_amount,
                                   'percentage_account': deposit_pi_chart_percent,
                                   'gas_fee': deposit_coin_fee,
                                   'gas_fee_dollars': deposit_coin_fee_dollars,
                                   'interaction_times': deposit_interaction_times,
                                   'failed_interaction_times': deposit_failed_interaction_times,
                                   'first_txn': first_txn,
                                   'first_txn_days_since': first_days_since,
                                   'last_txn': last_txn,
                                   'last_txn_days_since': last_days_since
                                   })


    # formatting total withdrawals data
    withdrawals_formatted = []
    for i in withdrawals['data'].items():
        tier = i[1]
        withdraw_display_name = tier['withdraw_display_name']
        withdraw_address = tier['withdraw_address']
        withdraw_dollar_amount = format_dollars(format_coins_machine(tier['withdraw_coin_amount']) * float(kusama_price))
        withdraw_coin_amount = format_coins_API(tier['withdraw_coin_amount'])
        withdraw_pi_chart_percent = percentage_format_API(tier['withdraw_pi_chart_percent'])
        withdraw_coin_fee = format_coins_longer_API(tier['withdraw_coin_fee'])
        withdraw_coin_fee_dollars = format_dollars_longer(tier['withdraw_coin_fee_dollars'])
        withdraw_interaction_times = tier['withdraw_interaction_times']
        withdraw_failed_interaction_times = tier['withdraw_failed_interaction_times']
        withdraw_first_txn = first_txn_dates_API(withdrawals_rawFLtxns['rawFLtxns'][tier['withdraw_address']])
        first_txn = withdraw_first_txn['first_txn_full_date']
        first_days_since = withdraw_first_txn['days_since']
        withdraw_last_txn = last_txn_dates_API(withdrawals_rawFLtxns['rawFLtxns'][tier['withdraw_address']])
        last_txn = withdraw_last_txn['last_txn_full_date']
        last_days_since = withdraw_last_txn['days_since']


        withdrawals_formatted.append({'display_name': withdraw_display_name,
                                      'wallet_address': withdraw_address,
                                      'coin_amount': withdraw_coin_amount,
                                      'coin_amount_fiat_worth': withdraw_dollar_amount,
                                      'percentage_account': withdraw_pi_chart_percent,
                                      'gas_fee': withdraw_coin_fee,
                                      'gas_fee_dollars': withdraw_coin_fee_dollars,
                                      'interaction_times': withdraw_interaction_times,
                                      'failed_interaction_times': withdraw_failed_interaction_times,
                                      'first_txn': first_txn,
                                      'first_txn_days_since': first_days_since,
                                      'last_txn': last_txn,
                                      'last_txn_days_since': last_days_since
                                      })



    return {'all_deposits': deposits_formatted,
            'all_withdrawals': withdrawals_formatted}







# RUN SERVER ##############################################################################################################################################################
if __name__ == '__main__':
    app.run(port=7777)


