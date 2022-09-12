import json
import requests
import time
import decimal
from keys import *
from universal_functions import kusama_timestamp_converter, current_dates_short, decimal_number_formatter, format_dollars, \
    format_coins, format_dollars_longer, format_coins_longer, kusama_first_txn_dates, kusama_last_txn_dates
from kusama import kusama_price



def getTransfers(wallet_address, network):
    # the api request function for getting transfers
    def the_transfers():
        def all_transfer_req(page):
            url = f"https://{network}.api.subscan.io/api/scan/transfers"
            payload = json.dumps({"address": wallet_address, "row": 100, "page": page})
            headers = {'Content-Type': 'application/json', 'X-API-Key': subscan_api_key}
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

    # total dates title
    if len(all_transfers) != 0:
        first_txn = int(len(all_transfers)) - 1
        first_txn = all_transfers[first_txn]['block_timestamp']
        first_txn = kusama_timestamp_converter(first_txn)
        today = current_dates_short()
        total_dates_title = '(' + str(first_txn) + ' - ' + str(today) + ')'
    else:
        total_dates_title = '(--/--/-- - --/--/--)'

    # deposit info's
    total_deposit_volume_coins = 0

    # withdraw info's
    withdrawal_volume_coins = 0
    total_withdrawal_gas_coins = 0
    total_withdrawal_gas_coins_failed = 0
    total_withdrawal_interactions_failed = 0

    # organising into deposit and withdraws
    for i in all_transfers:
        if i['from'] == wallet_address:
            all_withdraws.append(i)
        else:
            all_deposits.append(i)

    # deposit and withdrawal interaction amounts
    total_deposit_interactions = len(all_deposits)
    total_withdrawal_interactions = len(all_withdraws)

    # getting deposit data
    for i in all_deposits:
        total_deposit_volume_coins += float(i['amount'])

    # getting withdrawal data
    for i in all_withdraws:
        if i['success'] == True:
            withdrawal_volume_coins += float(i['amount'])
            total_withdrawal_gas_coins += decimal_number_formatter(i['fee'])
        else:
            total_withdrawal_gas_coins_failed += decimal_number_formatter((i['fee']))
            total_withdrawal_interactions_failed += 1

    # total asset volume
    total_volume_coins = 0

    # getting total txn info
    for i in all_transfers:
        # Wallet volume
        total_volume_coins += float(i['amount'])

    # kusama price
    global kusama_price

    # fee paid dollar worth
    total_withdrawal_gas_dollars_failed = total_withdrawal_gas_coins_failed * decimal.Decimal(kusama_price)
    total_withdrawal_gas_dollars = total_withdrawal_gas_coins * decimal.Decimal(kusama_price)

    # deposit, withdrawal and total dollar worth
    total_volume_dollars = total_volume_coins * float(kusama_price)
    total_deposit_volume_dollars = total_deposit_volume_coins * float(kusama_price)
    total_withdrawal_volume_dollars = withdrawal_volume_coins * float(kusama_price)

    # formatting numbers
    # total
    total_volume_coins = format_coins(total_volume_coins)
    total_volume_dollars = format_dollars(total_volume_dollars)
    # withdrawal
    withdrawal_volume_coins = format_coins(withdrawal_volume_coins)
    total_withdrawal_volume_dollars = format_dollars(total_withdrawal_volume_dollars)
    total_withdrawal_gas_coins = format_coins_longer(total_withdrawal_gas_coins)
    total_withdrawal_gas_dollars = format_dollars_longer(total_withdrawal_gas_dollars)
    total_withdrawal_gas_coins_failed = format_coins_longer(total_withdrawal_gas_coins_failed)
    total_withdrawal_gas_dollars_failed = format_dollars_longer(total_withdrawal_gas_dollars_failed)
    # deposits
    total_deposit_volume_coins = format_coins(total_deposit_volume_coins)
    total_deposit_volume_dollars = format_dollars(total_deposit_volume_dollars)
    # first txn dates
    withdrawal_first_txn_date = kusama_first_txn_dates(all_withdraws)
    deposits_first_txn_date = kusama_first_txn_dates(all_deposits)
    total_first_txn_date = kusama_first_txn_dates(all_transfers)
    # last txn dates
    withdrawal_last_txn_date = kusama_last_txn_dates(all_withdraws)
    deposits_last_txn_date = kusama_last_txn_dates(all_deposits)
    total_last_txn_date = kusama_last_txn_dates(all_transfers)

    return {'total_transfers': {
        'total': {'total_volume_coins': total_volume_coins, 'total_volume_dollars': total_volume_dollars,
                  'total_interactions': total_deposit_interactions + total_withdrawal_interactions + total_withdrawal_interactions_failed,
                  'total_interactions_failed': total_withdrawal_interactions_failed,
                  'total_gas_coins': total_withdrawal_gas_coins,
                  'total_gas_dollars': total_withdrawal_gas_dollars,
                  'total_gas_coins_failed': total_withdrawal_gas_coins_failed,
                  'total_gas_dollars_failed': total_withdrawal_gas_dollars_failed,
                  'total_dates_title': total_dates_title,
                  'total_first_txn_date': total_first_txn_date,
                  'total_last_txn_date': total_last_txn_date
                  },

        'total_withdrawals': {'withdrawal_volume_coins': withdrawal_volume_coins,
                              'total_withdrawal_volume_dollars': total_withdrawal_volume_dollars,
                              'total_withdrawal_interactions': total_withdrawal_interactions,
                              'total_withdrawal_interactions_failed': total_withdrawal_interactions_failed,
                              'total_withdrawal_gas_coins': total_withdrawal_gas_coins,
                              'total_withdrawal_gas_dollars': total_withdrawal_gas_dollars,
                              'total_withdrawal_gas_coins_failed': total_withdrawal_gas_coins_failed,
                              'total_withdrawal_gas_dollars_failed': total_withdrawal_gas_dollars_failed,
                              'withdrawal_first_txn_date': withdrawal_first_txn_date,
                              'withdrawal_last_txn_date': withdrawal_last_txn_date
                              },

        'total_deposits': {'total_deposit_volume_coins': total_deposit_volume_coins,
                           'total_deposit_volume_dollars': total_deposit_volume_dollars,
                           'total_deposit_interactions': total_deposit_interactions,
                           'deposits_first_txn_date': deposits_first_txn_date,
                           'deposits_last_txn_date': deposits_last_txn_date
                           }}}, \
           {'all_transfers': all_transfers}, \
           {'all_withdraws': all_withdraws}, \
           {'all_deposits': all_deposits}