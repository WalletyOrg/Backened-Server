################################################################################################################################################################################
import datetime
import requests
import json
import decimal
import time
from dateutil.tz import gettz
import datetime as dt
from keys import *

# random functions###############################################################################################################################################################################


def current_dates():
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
            return float(formatted_number)
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






# format coins
def format_coins(coins):
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
            coins = str(coins) + ' KSM'
            return str(coins)
        else:
            return '0 KSM'
    except:
        return f'{coins} KSM'
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
def format_coins_longer(coins):
    if decimal.Decimal(coins) != 0:
        coins = str(coins)
        point = 0
        for i in coins:
            if i != '.':
                point += 1
            elif i == '.':
                break
        coins = str(coins)[:point + 8]
        coins = str(coins) + ' KSM'
        return str(coins)

    else:
        return '0 KSM'






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




# kusama price
def kusamaPrice():
    kusama_price_req = requests.get('https://api.coingecko.com/api/v3/coins/kusama').text
    kusama_price_req = json.loads(kusama_price_req)
    kusama_price_req = kusama_price_req['market_data']['current_price']['usd']
    return kusama_price_req

kusama_price = decimal.Decimal(kusamaPrice())



# first txn times
def kusama_first_txn_dates(transfers):
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
def kusama_timestamp_converter(block_timestamp):
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
def raw_transfer_format_timestamp(timestamp):
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
            day_message = '(today)'
        elif days_since == 1:
            day_message = '(1 day ago)'
        else:
            day_message = '({} days ago)'.format(days_since)
        return {'first_txn_full_date': first_txn_full_date, 'days_since': day_message}
    except IndexError:
        return {'first_txn_full_date': '-', 'days_since': '-'}
# last txn times
def kusama_last_txn_dates(transfers):
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
def kusama_wallet_short_name(address):
    short_name = '{}...{}'.format(str(address)[:7], str(address)[40:47])
    return short_name




# monthly stats###############################################################################################################################################################################


def kusama_monthly_stats(all_transfers, wallet_address):

    def timestamp_m_converter(timestamp):
        from datetime import datetime
        dt_object = datetime.fromtimestamp(timestamp)
        return {'month': int(dt_object.strftime('%m')), 'year': int(dt_object.strftime('%Y'))}

    # monthly transactions function
    def monthly_transactions(all_transfers):
        from datetime import date
        monthly_transactions = []
        current_month = str(date.today().strftime('%m'))
        current_month = int(current_month)
        current_year = str(date.today().strftime('%Y'))
        current_year = int(current_year)
        for i in all_transfers['all_transfers']:
            if int(timestamp_m_converter(i['block_timestamp'])['month']) == current_month and int(
                    timestamp_m_converter(i['block_timestamp'])['year']) == current_year:
                monthly_transactions.append(i)
        return monthly_transactions

    monthly_transfers = monthly_transactions(all_transfers)
    monthly_withdraws = []
    monthly_deposits = []

    # monthly dates title
    if len(monthly_transfers) != 0:
        first_txn = int(len(monthly_transfers)) - 1
        first_txn = monthly_transfers[first_txn]['block_timestamp']
        first_txn = kusama_timestamp_converter(first_txn)
        today = current_dates_short()
        monthly_dates_title = '(' + str(first_txn) + ' - ' + str(today) + ')'
    else:
        monthly_dates_title = '(--/--/-- - --/--/--)'

    # deposit info's
    monthly_deposit_volume_coins = 0
    # withdraw info's
    monthly_withdrawal_volume_coin = 0

    monthly_withdrawal_gas_coin = decimal.Decimal(0)
    monthly_withdrawal_failed_gas_coin = decimal.Decimal(0)
    monthly_withdrawal_failed_interactions = 0

    # organising into deposit and withdraws
    for i in monthly_transfers:
        if i['from'] == wallet_address:
            monthly_withdraws.append(i)
        else:
            monthly_deposits.append(i)

    # deposit and withdrawal interaction amounts
    monthly_deposit_interactions = len(monthly_deposits)
    monthly_withdrawal_interactions = len(monthly_withdraws)

    # getting deposit data
    for i in monthly_deposits:
        monthly_deposit_volume_coins += float(i['amount'])

    # getting withdrawal data
    for i in monthly_withdraws:
        if i['success'] == True:
            monthly_withdrawal_volume_coin += float(i['amount'])
            monthly_withdrawal_gas_coin += decimal_number_formatter(i['fee'])
        else:
            monthly_withdrawal_failed_gas_coin += decimal_number_formatter((i['fee']))
            monthly_withdrawal_failed_interactions += 1

    # total asset volume
    monthly_total_volume_coins = 0

    # getting total txn info
    for i in monthly_transfers:
        # Wallet volume
        monthly_total_volume_coins += float(i['amount'])

    # fee paid dollar worth
    monthly_withdrawal_failed_gas_dollars = monthly_withdrawal_failed_gas_coin * decimal.Decimal(kusama_price)
    monthly_withdrawal_gas_dollars = monthly_withdrawal_gas_coin * decimal.Decimal(kusama_price)
    # deposit, withdrawal and total dollar worth
    monthly_total_volume_dollars = monthly_total_volume_coins * float(kusama_price)
    monthly_deposit_volume_dollars = monthly_deposit_volume_coins * float(kusama_price)
    monthly_withdrawal_volume_dollars = monthly_withdrawal_volume_coin * float(kusama_price)

    # formatting numbers
    # total
    monthly_total_volume_coins = format_coins(monthly_total_volume_coins)
    monthly_total_volume_dollars = format_dollars(monthly_total_volume_dollars)
    # withdrawal
    monthly_withdrawal_volume_coin = format_coins(monthly_withdrawal_volume_coin)
    monthly_withdrawal_volume_dollars = format_dollars(monthly_withdrawal_volume_dollars)
    monthly_withdrawal_gas_coin = format_coins_longer(monthly_withdrawal_gas_coin)
    monthly_withdrawal_gas_dollars = format_dollars_longer(monthly_withdrawal_gas_dollars)
    monthly_withdrawal_failed_gas_coin = format_coins_longer(monthly_withdrawal_failed_gas_coin)
    monthly_withdrawal_failed_gas_dollars = format_dollars_longer(monthly_withdrawal_failed_gas_dollars)
    # deposit
    monthly_deposit_volume_coins = format_coins(monthly_deposit_volume_coins)
    monthly_deposit_volume_dollars = format_dollars(monthly_deposit_volume_dollars)

    # first txn dates
    monthly_withdrawal_first_txn_date = kusama_first_txn_dates(monthly_withdraws)
    monthly_deposits_first_txn_date = kusama_first_txn_dates(monthly_deposits)
    monthly_total_first_txn_date = kusama_first_txn_dates(monthly_transfers)
    # last txn dates
    monthly_withdrawal_last_txn_date = kusama_last_txn_dates(monthly_withdraws)
    monthly_deposits_last_txn_date = kusama_last_txn_dates(monthly_deposits)
    monthly_total_last_txn_date = kusama_last_txn_dates(monthly_transfers)

    return {'monthly_total': {'monthly_total_volume_coins': monthly_total_volume_coins,
                              'monthly_total_volume_dollars': monthly_total_volume_dollars,
                              'monthly_total_interactions': monthly_deposit_interactions + monthly_withdrawal_interactions + monthly_withdrawal_failed_interactions,
                              'monthly_total_failed_interactions': monthly_withdrawal_failed_interactions,
                              'monthly_total_gas_coin': monthly_withdrawal_gas_coin,
                              'monthly_total_gas_dollars': monthly_withdrawal_gas_dollars,
                              'monthly_total_failed_gas_coin': monthly_withdrawal_failed_gas_coin,
                              'monthly_total_failed_gas_dollars': monthly_withdrawal_failed_gas_dollars,
                              'monthly_dates_title': monthly_dates_title,
                              'monthly_total_first_txn_date': monthly_total_first_txn_date,
                              'monthly_total_last_txn_date': monthly_total_last_txn_date
                              },

            'monthly_withdrawal': {'monthly_withdrawal_volume_coin': monthly_withdrawal_volume_coin,
                                   'monthly_withdrawal_volume_dollars': monthly_withdrawal_volume_dollars,
                                   'monthly_withdrawal_interactions': monthly_withdrawal_interactions,
                                   'monthly_withdrawal_failed_interactions': monthly_withdrawal_failed_interactions,
                                   'monthly_withdrawal_gas_coin': monthly_withdrawal_gas_coin,
                                   'monthly_withdrawal_gas_dollars': monthly_withdrawal_gas_dollars,
                                   'monthly_withdrawal_failed_gas_coin': monthly_withdrawal_failed_gas_coin,
                                   'monthly_withdrawal_failed_gas_dollars': monthly_withdrawal_failed_gas_dollars,
                                   'monthly_withdrawal_first_txn_date': monthly_withdrawal_first_txn_date,
                                   'monthly_withdrawal_last_txn_date': monthly_withdrawal_last_txn_date
                                   },

            'monthly_deposit': {'monthly_deposit_volume_coins': monthly_deposit_volume_coins,
                                'monthly_deposit_volume_dollars': monthly_deposit_volume_dollars,
                                'monthly_deposit_interactions': monthly_deposit_interactions,
                                'monthly_deposits_first_txn_date': monthly_deposits_first_txn_date,
                                'monthly_deposits_last_txn_date': monthly_deposits_last_txn_date
                                }}, \
           {'monthly_withdraws': monthly_withdraws}, \
           {'monthly_deposits': monthly_deposits}, \
           {'monthly_transfers': monthly_transfers}






# paper hand diamond hand###############################################################################################################################################################################



def kusama_paper_diamond_handed(all_withdrawals, diamond_handed_coins):
    # paper handed
    paper_handed_coins = 0

    for i in all_withdrawals['all_withdraws']:
        paper_handed_coins += float(i['amount'])

    # paperhanded dollar amounts and formatting numbers
    paper_handed_coins_dollars = float(kusama_price) * float(paper_handed_coins)

    # formatting numbers
    paper_handed_coins = format_coins(paper_handed_coins)
    paper_handed_coins_dollars = format_dollars(paper_handed_coins_dollars)

    # diamond handed
    diamond_handed_coins = diamond_handed_coins['diamond_handed_coins']
    diamond_handed_coins_dollars = float(kusama_price) * float(diamond_handed_coins)
    diamond_handed_coins = format_coins(diamond_handed_coins)
    diamond_handed_coins_dollars = format_dollars(diamond_handed_coins_dollars)

    return {'handed': {'paper_handed': {'paper_handed_coins': paper_handed_coins,
                                        'paper_handed_coins_dollars': paper_handed_coins_dollars},

                       'diamond_handed': {'diamond_handed_coins': diamond_handed_coins,
                                          'diamond_handed_coins_dollars': diamond_handed_coins_dollars}
                       }
            }


# raw transfers###############################################################################################################################################################################


def kusama_raw_transfers(all_deposits, all_withdrawals):
    deposit_transfers = []
    for i in all_deposits['all_deposits']:
        display_name = kusama_wallet_short_name(i['from'])
        if i['from_account_display']['display'] != '':
            display_name = i['from_account_display']['display']
        full_wallet_address = i['from']
        coin_amount = i['amount']
        coin_worth_dollar = float(coin_amount) * float(kusama_price)
        gas = decimal_number_formatter(i['fee'])
        gas_dollar_worth = decimal.Decimal(gas) * decimal.Decimal(kusama_price)
        txn_time = raw_transfer_format_timestamp(i['block_timestamp'])
        days_since = txn_time['days_since']
        txn_time = txn_time['first_txn_full_date']
        # formatting dollars
        coin_worth_dollar = format_dollars(coin_worth_dollar)
        gas_dollar_worth = format_dollars_longer(gas_dollar_worth)
        # formatting coins
        coin_amount = format_coins(coin_amount)
        gas = format_coins_longer(gas)

        deposit_transfers.append([f'{display_name} ({full_wallet_address}) deposited {coin_amount} (',
                                  coin_worth_dollar,
                                  f') on {txn_time} {days_since} with a fee of {gas} (',
                                  gas_dollar_worth,
                                  ')'])

    if deposit_transfers == []:
        deposit_transfers.append('-')


    withdraw_transfers = []
    for i in all_withdrawals['all_withdraws']:
        withdraw_withdrew = 'withdrew'
        if i['success'] != True:
            withdraw_withdrew = 'TRIED to withdraw'
        display_name = kusama_wallet_short_name(i['to'])
        if i['to_account_display']['display'] != '':
            display_name = i['to_account_display']['display']
        full_wallet_address = i['to']
        coin_amount = i['amount']
        coin_worth_dollar = float(coin_amount) * float(kusama_price)
        gas = decimal_number_formatter(i['fee'])
        gas_dollar_worth = decimal.Decimal(gas) * decimal.Decimal(kusama_price)
        txn_time = raw_transfer_format_timestamp(i['block_timestamp'])
        days_since = txn_time['days_since']
        txn_time = txn_time['first_txn_full_date']
        # formatting dollars
        coin_worth_dollar = format_dollars(coin_worth_dollar)
        gas_dollar_worth = format_dollars_longer(gas_dollar_worth)
        # formatting coins
        coin_amount = format_coins(coin_amount)
        gas = format_coins_longer(gas)

        withdraw_transfers.append([f'You {withdraw_withdrew} {coin_amount} (',
                                   coin_worth_dollar,
                                   f') to {display_name} ({full_wallet_address}) on {txn_time} {days_since} with a fee of {gas} (',
                                   gas_dollar_worth,
                                   ')'])

    if withdraw_transfers == []:
        withdraw_transfers.append('-')

    return dict({'raw_transfers': {'deposit_transfers': deposit_transfers,
                                   'withdraw_transfers': withdraw_transfers}})





# unique accounts###############################################################################################################################################################################





def kusama_top_accounts_withdraw_deposit(wallet_address, all_transactions, all_deposits, all_withdrawals, monthly_deposits,
                                         monthly_withdrawals, monthly_transactions):
    def kusama_top_accounts(wallet_address, transfers, withdraw_or_deposit):

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

                    if i[account_display]['identity']:
                        wallet_names[i[withdraw_or_deposit]] = i[account_display]['display']
                    else:
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

    # total top accounts
    def total_top_transfer_accounts(total_deposits, total_withdrawals, monthly_deposits, monthly_withdrawals):
        # all_total_transfers
        total_deposits = total_deposits['deposit_unformatted_data']
        try:
            first_address = list(total_deposits)[0]
            depositVolume = total_deposits[first_address]['XXX_coin_volume']
        except IndexError:
            depositVolume = 0
        total_withdrawals = total_withdrawals['withdraw_unformatted_data']
        try:
            first_address = list(total_withdrawals)[0]
            withdrawalsVolume = total_withdrawals[first_address]['XXX_coin_volume']
        except IndexError:
            withdrawalsVolume = 0

        total_XX = depositVolume + withdrawalsVolume

        all_total_transfers = {}

        for i in total_deposits.items():
            all_total_transfers[i[0]] = {'total_address': i[0],
                                         'total_coin_amount': float(i[1]['deposit_coin_amount']),
                                         'total_coin_fee': decimal.Decimal(i[1]['deposit_coin_fee']),
                                         'total_coin_fee_dollars': decimal.Decimal(i[1]['deposit_coin_fee_dollars']),
                                         'total_display_name': i[1]['deposit_display_name'],
                                         'total_interaction_times': i[1]['deposit_interaction_times'],
                                         'total_failed_interaction_times': i[1]['deposit_failed_interaction_times'],
                                         'total_pi_chart_percent': i[1]['deposit_pi_chart_percent']
                                         }

        for i in total_withdrawals.items():
            if i[0] in all_total_transfers:
                dict_transfers = dict(all_total_transfers[i[0]])
                all_total_transfers[i[0]] = {'total_address': i[0],
                                             'total_coin_amount': float(i[1]['withdraw_coin_amount']) + dict_transfers['total_coin_amount'],
                                             'total_coin_fee': decimal.Decimal(i[1]['withdraw_coin_fee']) + dict_transfers['total_coin_fee'],
                                             'total_coin_fee_dollars': decimal.Decimal(i[1]['withdraw_coin_fee_dollars']) + dict_transfers['total_coin_fee_dollars'],
                                             'total_display_name': i[1]['withdraw_display_name'],
                                             'total_interaction_times': i[1]['withdraw_interaction_times'] + dict_transfers['total_interaction_times'],
                                             'total_failed_interaction_times': i[1]['withdraw_failed_interaction_times'] + dict_transfers['total_failed_interaction_times'],
                                             }
            else:
                all_total_transfers[i[0]] = {'total_address': i[0],
                                             'total_coin_amount': i[1]['withdraw_coin_amount'],
                                             'total_coin_fee': i[1]['withdraw_coin_fee'],
                                             'total_coin_fee_dollars': i[1]['withdraw_coin_fee_dollars'],
                                             'total_display_name': i[1]['withdraw_display_name'],
                                             'total_interaction_times': i[1]['withdraw_interaction_times'],
                                             'total_failed_interaction_times': i[1]['withdraw_failed_interaction_times'],
                                             'total_pi_chart_percent': i[1]['withdraw_pi_chart_percent']
                                             }

        # monthly_total_transfers
        monthly_total_deposits = monthly_deposits['deposit_unformatted_data']
        try:
            first_address = list(monthly_total_deposits)[0]
            monthlyDepositVolume = monthly_total_deposits[first_address]['XXX_coin_volume']
        except IndexError:
            monthlyDepositVolume = 0
        monthly_total_withdrawals = monthly_withdrawals['withdraw_unformatted_data']
        try:
            first_address = list(monthly_total_withdrawals)[0]
            monthlyWithdrawalsVolume = monthly_total_withdrawals[first_address]['XXX_coin_volume']
        except IndexError:
            monthlyWithdrawalsVolume = 0

        monthly_XX = monthlyDepositVolume + monthlyWithdrawalsVolume

        monthly_total_transfers = {}

        for i in monthly_total_deposits.items():
            monthly_total_transfers[i[0]] = {'monthly_total_address': i[0],
                                             'monthly_total_coin_amount': i[1]['deposit_coin_amount'],
                                             'monthly_total_coin_fee': i[1]['deposit_coin_fee'],
                                             'monthly_total_coin_fee_dollars': i[1]['deposit_coin_fee_dollars'],
                                             'monthly_total_display_name': i[1]['deposit_display_name'],
                                             'monthly_total_interaction_times': i[1]['deposit_interaction_times'],
                                             'monthly_total_failed_interaction_times': i[1]['deposit_failed_interaction_times'],
                                             'monthly_total_pi_chart_percent': i[1]['deposit_pi_chart_percent']
                                             }

        for i in monthly_total_withdrawals.items():
            if i[0] in monthly_total_transfers:
                dict_transfers = dict(monthly_total_transfers[i[0]])
                monthly_total_transfers[i[0]] = {'monthly_total_address': i[0],
                                                 'monthly_total_coin_amount': float(i[1]['withdraw_coin_amount']) + float(dict_transfers['monthly_total_coin_amount']),
                                                 'monthly_total_coin_fee': decimal.Decimal(i[1]['withdraw_coin_fee']) + decimal.Decimal(dict_transfers['monthly_total_coin_fee']),
                                                 'monthly_total_coin_fee_dollars': decimal.Decimal(i[1]['withdraw_coin_fee_dollars']) + decimal.Decimal(dict_transfers['monthly_total_coin_fee_dollars']),
                                                 'monthly_total_display_name': i[1]['withdraw_display_name'],
                                                 'monthly_total_interaction_times': i[1]['withdraw_interaction_times'] + dict_transfers['monthly_total_interaction_times'],
                                                 'monthly_total_failed_interaction_times': i[1]['withdraw_failed_interaction_times'] + dict_transfers['monthly_total_failed_interaction_times'],
                                                 }
            else:
                monthly_total_transfers[i[0]] = {'monthly_total_address': i[0],
                                                 'monthly_total_coin_amount': i[1]['withdraw_coin_amount'],
                                                 'monthly_total_coin_fee': i[1]['withdraw_coin_fee'],
                                                 'monthly_total_coin_fee_dollars': i[1]['withdraw_coin_fee_dollars'],
                                                 'monthly_total_display_name': i[1]['withdraw_display_name'],
                                                 'monthly_total_interaction_times': i[1]['withdraw_interaction_times'],
                                                 'monthly_total_failed_interaction_times': i[1]['withdraw_failed_interaction_times'],
                                                 'monthly_total_pi_chart_percent': i[1]['withdraw_pi_chart_percent']
                                                 }

        return {'all_total_transfers': all_total_transfers, 'monthly_total_transfers': monthly_total_transfers, 'total_XX': total_XX, 'monthly_XX': monthly_XX}


    # some data
    # ALL total deposits
    deposits_data = kusama_top_accounts(wallet_address, all_deposits, 'deposit')
    deposits = deposits_data[0]
    unformatted_deposits = deposits_data[1]
    deposits_rawFLtxns = deposits_data[2]
    # ALL total withdrawals
    withdrawals_data = kusama_top_accounts(wallet_address, all_withdrawals, 'withdraw')
    withdrawals = withdrawals_data[0]
    unformatted_withdrawals = withdrawals_data[1]
    withdrawals_rawFLtxns = withdrawals_data[2]
    # monthly deposits
    deposits_monthly_data = kusama_top_accounts(wallet_address, monthly_deposits, 'deposit')
    deposits_monthly = deposits_monthly_data[0]
    monthly_unformatted_deposits = deposits_monthly_data[1]
    monthly_deposits_rawFLtxns = deposits_monthly_data[2]
    # monthly withdrawals
    withdrawals_monthly_data = kusama_top_accounts(wallet_address, monthly_withdrawals, 'withdraw')
    withdrawals_monthly = withdrawals_monthly_data[0]
    monthly_unformatted_withdrawals = withdrawals_monthly_data[1]
    monthly_withdrawals_rawFLtxns = withdrawals_monthly_data[2]

    # total data
    total_data = total_top_transfer_accounts(unformatted_deposits, unformatted_withdrawals,
                                             monthly_unformatted_deposits, monthly_unformatted_withdrawals)

    # total total
    total = total_data['all_total_transfers']
    total_XX = total_data['total_XX']
    # total flx
    total_rawFLtxns = {}
    for i in all_transactions:
        if i['from'] != wallet_address:
            unique_wd = 'from'
        else:
            unique_wd = 'to'
        if i[unique_wd] not in total_rawFLtxns:
            total_rawFLtxns[i[unique_wd]] = [i]
        else:
            total_rawFLtxns[i[unique_wd]].append(i)
    total_rawFLtxns = {'total_rawFLtxns': total_rawFLtxns}


    # monthly total
    monthly_total = total_data['monthly_total_transfers']
    monthly_XX = total_data['monthly_XX']
    # monthly flx
    monthly_rawFLtxns = {}
    for i in monthly_transactions:
        if i['from'] != wallet_address:
            unique_wd = 'from'
        else:
            unique_wd = 'to'
        if i[unique_wd] not in monthly_rawFLtxns:
            monthly_rawFLtxns[i[unique_wd]] = [i]
        else:
            monthly_rawFLtxns[i[unique_wd]].append(i)
    monthly_rawFLtxns = {'monthly_rawFLtxns': monthly_rawFLtxns}


    # times time function
    def time_times(possible):
        if int(possible) == 1:
            return 'time'
        else:
            return 'times'


    # formatting total deposits data
    deposits_formatted = []
    for i in deposits['data'].items():
        tier = i[1]
        deposit_display_name = tier['deposit_display_name']
        deposit_address = tier['deposit_address']
        deposit_dollar_amount = format_dollars(format_coins_machine(tier['deposit_coin_amount']) * float(kusama_price))
        deposit_coin_amount = format_coins(tier['deposit_coin_amount'])
        deposit_pi_chart_percent = percentage_format(tier['deposit_pi_chart_percent'])
        deposit_coin_fee = format_coins_longer(tier['deposit_coin_fee'])
        deposit_coin_fee_dollars = format_dollars_longer(tier['deposit_coin_fee_dollars'])
        deposit_interaction_times = tier['deposit_interaction_times']
        deposit_interaction_times_times = time_times(tier['deposit_interaction_times'])
        deposit_failed_interaction_times = tier['deposit_failed_interaction_times']
        deposit_failed_interaction_times_times = time_times(tier['deposit_failed_interaction_times'])
        deposit_first_txn = kusama_first_txn_dates(deposits_rawFLtxns['rawFLtxns'][tier['deposit_address']])
        first_txn = deposit_first_txn['first_txn_full_date']
        first_days_since = deposit_first_txn['days_since']
        deposit_last_txn = kusama_last_txn_dates(deposits_rawFLtxns['rawFLtxns'][tier['deposit_address']])
        last_txn = deposit_last_txn['last_txn_full_date']
        last_days_since = deposit_last_txn['days_since']

        deposits_formatted.append([f'{deposit_display_name} ({deposit_address}) has deposited a total of {deposit_coin_amount} (',
                                   deposit_dollar_amount,
                                   f') which accounts for {deposit_pi_chart_percent} of your total deposits. They have spent {deposit_coin_fee} (',
                                   deposit_coin_fee_dollars,
                                   f') on gas with you and deposited {deposit_interaction_times} {deposit_interaction_times_times} in total, '
                                   f'in which {deposit_failed_interaction_times} {deposit_failed_interaction_times_times} they failed. '
                                   f'Your first transaction with them was {first_txn} {first_days_since} and your last transaction with them was {last_txn} {last_days_since}.'])
    if deposits_formatted == []:
        deposits_formatted.append('-')


    # formatting total withdrawals data
    withdrawals_formatted = []
    for i in withdrawals['data'].items():
        tier = i[1]
        withdraw_display_name = tier['withdraw_display_name']
        withdraw_address = tier['withdraw_address']
        withdraw_dollar_amount = format_dollars(format_coins_machine(tier['withdraw_coin_amount']) * float(kusama_price))
        withdraw_coin_amount = format_coins(tier['withdraw_coin_amount'])
        withdraw_pi_chart_percent = percentage_format(tier['withdraw_pi_chart_percent'])
        withdraw_coin_fee = format_coins_longer(tier['withdraw_coin_fee'])
        withdraw_coin_fee_dollars = format_dollars_longer(tier['withdraw_coin_fee_dollars'])
        withdraw_interaction_times = tier['withdraw_interaction_times']
        withdraw_interaction_times_times = time_times(tier['withdraw_interaction_times'])
        withdraw_failed_interaction_times = tier['withdraw_failed_interaction_times']
        withdraw_failed_interaction_times_times = time_times(tier['withdraw_failed_interaction_times'])
        withdraw_first_txn = kusama_first_txn_dates(withdrawals_rawFLtxns['rawFLtxns'][tier['withdraw_address']])
        first_txn = withdraw_first_txn['first_txn_full_date']
        first_days_since = withdraw_first_txn['days_since']
        withdraw_last_txn = kusama_last_txn_dates(withdrawals_rawFLtxns['rawFLtxns'][tier['withdraw_address']])
        last_txn = withdraw_last_txn['last_txn_full_date']
        last_days_since = withdraw_last_txn['days_since']

        withdrawals_formatted.append([f'You have withdrawn to {withdraw_display_name} ({withdraw_address}) a total of {withdraw_coin_amount} (',
                                      withdraw_dollar_amount,
                                      f') which accounts for {withdraw_pi_chart_percent} of your total withdrawals. You have spent {withdraw_coin_fee} (',
                                      withdraw_coin_fee_dollars,
                                      f') on gas doing this and withdrawn {withdraw_interaction_times} {withdraw_interaction_times_times} in total, '
                                      f'in which {withdraw_failed_interaction_times} {withdraw_failed_interaction_times_times} they failed. '
                                      f'Your first transaction with them was {first_txn} {first_days_since} and your last transaction with them was {last_txn} {last_days_since}.'])
    if withdrawals_formatted == []:
        withdrawals_formatted.append('-')


    # formatting total total data
    total_formatted = []
    for i in total.items():
        tier = i[1]
        total_display_name = tier['total_display_name']
        total_address = tier['total_address']
        total_dollar_amount = format_dollars(format_coins_machine(tier['total_coin_amount']) * float(kusama_price))
        total_coin_amount = format_coins(tier['total_coin_amount'])
        total_pi_chart_percent = percentage_format((float(tier['total_coin_amount']) / float(total_XX)) * 100)
        total_coin_fee = format_coins_longer(tier['total_coin_fee'])
        total_coin_fee_dollars = format_dollars_longer(tier['total_coin_fee_dollars'])
        total_interaction_times = tier['total_interaction_times']
        total_interaction_times_times = time_times(tier['total_interaction_times'])
        total_failed_interaction_times = tier['total_failed_interaction_times']
        total_failed_interaction_times_times = time_times(tier['total_failed_interaction_times'])
        total_first_txn = kusama_first_txn_dates(total_rawFLtxns['total_rawFLtxns'][tier['total_address']])
        first_txn = total_first_txn['first_txn_full_date']
        first_days_since = total_first_txn['days_since']
        total_last_txn = kusama_last_txn_dates(total_rawFLtxns['total_rawFLtxns'][tier['total_address']])
        last_txn = total_last_txn['last_txn_full_date']
        last_days_since = total_last_txn['days_since']

        total_formatted.append([f'You and {total_display_name} ({total_address}) have had a total volume of {total_coin_amount} (',
                                total_dollar_amount,
                                f') which accounts for {total_pi_chart_percent} of your total volume. Between you both have spent {total_coin_fee} (',
                                total_coin_fee_dollars,
                                f') on gas and interacted {total_interaction_times} {total_interaction_times_times} in total, '
                                f'in which {total_failed_interaction_times} {total_failed_interaction_times_times} they failed. '
                                f'Your first transaction with them was {first_txn} {first_days_since} and your last transaction with them was {last_txn} {last_days_since}.'])
    if total_formatted == []:
        total_formatted.append('-')


    # formatting monthly deposits data
    monthly_deposits_formatted = []
    for i in deposits_monthly['data'].items():
        tier = i[1]
        deposit_display_name = tier['deposit_display_name']
        deposit_address = tier['deposit_address']
        deposit_dollar_amount = format_dollars(format_coins_machine(tier['deposit_coin_amount']) * float(kusama_price))
        deposit_coin_amount = format_coins(tier['deposit_coin_amount'])
        deposit_pi_chart_percent = percentage_format(tier['deposit_pi_chart_percent'])
        deposit_coin_fee = format_coins_longer(tier['deposit_coin_fee'])
        deposit_coin_fee_dollars = format_dollars_longer(tier['deposit_coin_fee_dollars'])
        deposit_interaction_times = tier['deposit_interaction_times']
        deposit_interaction_times_times = time_times(tier['deposit_interaction_times'])
        deposit_failed_interaction_times = tier['deposit_failed_interaction_times']
        deposit_failed_interaction_times_times = time_times(tier['deposit_failed_interaction_times'])
        deposit_first_txn = kusama_first_txn_dates(monthly_deposits_rawFLtxns['rawFLtxns'][tier['deposit_address']])
        first_txn = deposit_first_txn['first_txn_full_date']
        first_days_since = deposit_first_txn['days_since']
        deposit_last_txn = kusama_last_txn_dates(monthly_deposits_rawFLtxns['rawFLtxns'][tier['deposit_address']])
        last_txn = deposit_last_txn['last_txn_full_date']
        last_days_since = deposit_last_txn['days_since']

        monthly_deposits_formatted.append([f'{deposit_display_name} ({deposit_address}) has deposited a total of {deposit_coin_amount} (',
                                           deposit_dollar_amount,
                                           f') which accounts for {deposit_pi_chart_percent} of your monthly deposits. They have spent {deposit_coin_fee} (',
                                           deposit_coin_fee_dollars,
                                           f') on gas with you and deposited {deposit_interaction_times} {deposit_interaction_times_times} this month, '
                                           f'in which {deposit_failed_interaction_times} {deposit_failed_interaction_times_times} they failed. '
                                           f'Your first transaction with them this month was {first_txn} {first_days_since} and your last transaction with them this month was {last_txn} {last_days_since}.'])
    if monthly_deposits_formatted == []:
        monthly_deposits_formatted.append('-')


    # formatting monthly withdrawals data
    monthly_withdrawals_formatted = []
    for i in withdrawals_monthly['data'].items():
        tier = i[1]
        withdraw_display_name = tier['withdraw_display_name']
        withdraw_address = tier['withdraw_address']
        withdraw_dollar_amount = format_dollars(format_coins_machine(tier['withdraw_coin_amount']) * float(kusama_price))
        withdraw_coin_amount = format_coins(tier['withdraw_coin_amount'])
        withdraw_pi_chart_percent = percentage_format(tier['withdraw_pi_chart_percent'])
        withdraw_coin_fee = format_coins_longer(tier['withdraw_coin_fee'])
        withdraw_coin_fee_dollars = format_dollars_longer(tier['withdraw_coin_fee_dollars'])
        withdraw_interaction_times = tier['withdraw_interaction_times']
        withdraw_interaction_times_times = time_times(tier['withdraw_interaction_times'])
        withdraw_failed_interaction_times = tier['withdraw_failed_interaction_times']
        withdraw_failed_interaction_times_times = time_times(tier['withdraw_failed_interaction_times'])
        withdraw_first_txn = kusama_first_txn_dates(monthly_withdrawals_rawFLtxns['rawFLtxns'][tier['withdraw_address']])
        first_txn = withdraw_first_txn['first_txn_full_date']
        first_days_since = withdraw_first_txn['days_since']
        withdraw_last_txn = kusama_last_txn_dates(monthly_withdrawals_rawFLtxns['rawFLtxns'][tier['withdraw_address']])
        last_txn = withdraw_last_txn['last_txn_full_date']
        last_days_since = withdraw_last_txn['days_since']

        monthly_withdrawals_formatted.append([f'You have withdrawn to {withdraw_display_name} ({withdraw_address}) a total of {withdraw_coin_amount} (',
                                              withdraw_dollar_amount,
                                              f') which accounts for {withdraw_pi_chart_percent} of your monthly withdrawals. You have spent {withdraw_coin_fee} (',
                                              withdraw_coin_fee_dollars,
                                              f') on gas doing this and withdrawn {withdraw_interaction_times} {withdraw_interaction_times_times} to them this month, '
                                              f'in which {withdraw_failed_interaction_times} {withdraw_failed_interaction_times_times} they failed. '
                                              f'Your first transaction with them this month was {first_txn} {first_days_since} and your last transaction with them this month was {last_txn} {last_days_since}.'])
    if monthly_withdrawals_formatted == []:
        monthly_withdrawals_formatted.append('-')


    # formatting monthly total data
    monthly_total_formatted = []
    for i in monthly_total.items():
        tier = i[1]
        total_display_name = tier['monthly_total_display_name']
        total_address = tier['monthly_total_address']
        total_dollar_amount = format_dollars(format_coins_machine(tier['monthly_total_coin_amount']) * float(kusama_price))
        total_coin_amount = format_coins(tier['monthly_total_coin_amount'])
        total_pi_chart_percent = percentage_format((float(tier['monthly_total_coin_amount']) / float(monthly_XX)) * 100)
        total_coin_fee = format_coins_longer(tier['monthly_total_coin_fee'])
        total_coin_fee_dollars = format_dollars_longer(tier['monthly_total_coin_fee_dollars'])
        total_interaction_times = tier['monthly_total_interaction_times']
        total_interaction_times_times = time_times(tier['monthly_total_interaction_times'])
        total_failed_interaction_times = tier['monthly_total_failed_interaction_times']
        total_failed_interaction_times_times = time_times(tier['monthly_total_failed_interaction_times'])
        total_first_txn = kusama_first_txn_dates(monthly_rawFLtxns['monthly_rawFLtxns'][tier['monthly_total_address']])
        first_txn = total_first_txn['first_txn_full_date']
        first_days_since = total_first_txn['days_since']
        total_last_txn = kusama_last_txn_dates(monthly_rawFLtxns['monthly_rawFLtxns'][tier['monthly_total_address']])
        last_txn = total_last_txn['last_txn_full_date']
        last_days_since = total_last_txn['days_since']

        monthly_total_formatted.append([f'You and {total_display_name} ({total_address}) have had a monthly volume of {total_coin_amount} (',
                                        total_dollar_amount,
                                        f') which accounts for {total_pi_chart_percent} of your monthly volume. Between you both have spent {total_coin_fee} (',
                                        total_coin_fee_dollars,
                                        f') on gas and interacted {total_interaction_times} {total_interaction_times_times} this month, '
                                        f'in which {total_failed_interaction_times} {total_failed_interaction_times_times} they failed. '
                                        f'Your first transaction with them this month was {first_txn} {first_days_since} and your last transaction with them this month was {last_txn} {last_days_since}.'])
    if monthly_total_formatted == []:
        monthly_total_formatted.append('-')

    return {'all_top_accounts': {'all_deposits': deposits_formatted, 'all_withdrawals': withdrawals_formatted,
                                 'all_total': total_formatted},
            'monthly_top_accounts': {'monthly_deposits': monthly_deposits_formatted,
                                     'monthly_withdrawals': monthly_withdrawals_formatted,
                                     'monthly_total': monthly_total_formatted}}


# wallet profile###############################################################################################################################################################################



def kusama_wallet_profile(wallet_address):
    url = "https://kusama.api.subscan.io/api/v2/scan/search"
    payload = json.dumps({"key": wallet_address})
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': subscan_api_key}
    response = requests.request("POST", url, headers=headers, data=payload).text
    response = json.loads(response)
    # identity
    identity = response['data']['account']['account_display']['identity']
    if identity != False:
        identity = True
    else:
        identity = False
    # display name
    display_name = response['data']['account']['account_display']['display']
    if display_name == '':
        display_name = kusama_wallet_short_name(wallet_address)
    # legal name
    try:
        legal_name = response['data']['account']['legal']
    except KeyError:
        legal_name = '-'
    if legal_name == '':
        legal_name = '-'
    # account index
    try:
        account_index = response['data']['account']['account_display']['account_index']
    except KeyError:
        account_index = '-'
    if account_index == '':
        account_index = '-'
    # socials
    def url_check(url, social):
        social = str(social)
        url = str(url)
        url_len = len(url)
        if social == '':
            return ''
        if social[:url_len] == url:
            return social
        else:
            social = url + social
            return social
    # matrix
    try:
        riot = response['data']['account']['riot']
        riot = url_check('https://matrix.to/#/', riot)
    except KeyError:
        riot = ''
    # twitter
    try:
        twitter = response['data']['account']['twitter']
        twitter = url_check('https://www.twitter.com/', twitter)
    except KeyError:
        twitter = ''
    # website
    try:
        website = response['data']['account']['web']
        website = url_check('https://', website)
    except KeyError:
        website = ''
    # email
    try:
        email = response['data']['account']['email']
        email = url_check('mailto:', email)
    except KeyError:
        email = ''
    # judgements
    if response['data']['account']['account_display']['judgements'] == None:
        judgements = False
    else:
        judgements = True
    # checking if sub account
    if response['data']['account']['account_display']['parent'] == None:
        sub = False
    else:
        sub = True
    if sub == True:
        display_name = response['data']['account']['account_display']['parent']['display']

    # balances
    total_balance = response['data']['account']['balance']
    locked_balance = response['data']['account']['balance_lock']
    reserved_balance = response['data']['account']['reserved']
    reserved_balance = decimal_number_formatter(reserved_balance)
    transferable_balance = (float(total_balance) - float(locked_balance)) - float(reserved_balance)

    # balances for handed coins later on
    diamond_handed_coins = float(transferable_balance) + float(locked_balance)

    # Users role
    def nominator_check(wallet_address):
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': subscan_api_key}
        json_data = {
            'row': 1,
            'page': 0,
            'address': wallet_address}
        response = requests.post('https://kusama.api.subscan.io/api/scan/staking/nominator', headers=headers, json=json_data).text
        response = json.loads(response)
        response = response['data']['staking_info']
        if response != None:
            role = 'Nominator'
        else:
            role = 'Chain User'
        return role

    role = nominator_check(wallet_address)
    if role == '':
        role = 'Chain User'

    def nominator_role_check(address, current_role):
        headers = {
            'X-API-Key': subscan_api_key}
        json_data = {}
        response = requests.post('https://kusama.api.subscan.io/api/scan/staking/validators', headers=headers, json=json_data).text
        response = json.loads(response)
        response = response['data']['list']

        current_validators = []

        for i in response:
            validator_address = i['controller_account_display']['address']
            current_validators.append(validator_address)
            stash_address = i['stash_account_display']['address']
            current_validators.append(stash_address)
        if address in current_validators:
            return 'Validator'
        else:
            return current_role

    role = nominator_role_check(wallet_address, role)

    if response['data']['account']['is_registrar']:
        role = 'Registrar'
    if response['data']['account']['is_techcomm_member']:
        role = 'Technical Committee Member'
    if response['data']['account']['is_council_member']:
        role = 'Councillor'

    # dollar balances
    total_balance_dollars = float(total_balance) * float(kusama_price)
    locked_balance_dollars = float(locked_balance) * float(kusama_price)
    reserved_balance_dollars = float(reserved_balance) * float(kusama_price)
    transferable_balance_dollars = float(transferable_balance) * float(kusama_price)

    # formatting numbers
    total_balance = format_coins(total_balance)
    total_balance_dollars = format_dollars(total_balance_dollars)
    transferable_balance = format_coins(transferable_balance)
    transferable_balance_dollars = format_dollars(transferable_balance_dollars)
    locked_balance = format_coins(locked_balance)
    locked_balance_dollars = format_dollars(locked_balance_dollars)
    reserved_balance = format_coins(reserved_balance)
    reserved_balance_dollars = format_dollars(reserved_balance_dollars)

    # Report analytic
    report_analytic('Kusama', wallet_address, display_name)

    return {'wallet_profile': {
        'wallet_profile': {'display_name': display_name, 'legal_name': legal_name, 'account_index': account_index,
                           'role': role,
                           'email': email, 'twitter': twitter, 'website': website, 'riot': riot, 'identity': identity,
                           'judgements': judgements, 'sub': sub},
        'balances': {'total_balance': total_balance, 'total_balance_dollars': total_balance_dollars,
                     'transferable_balance': transferable_balance,
                     'transferable_balance_dollars': transferable_balance_dollars, 'locked_balance': locked_balance,
                     'locked_balance_dollars': locked_balance_dollars,
                     'reserved_balance': reserved_balance, 'reserved_balance_dollars': reserved_balance_dollars}}}, \
           {'diamond_handed_coins': diamond_handed_coins}



# transfers###############################################################################################################################################################################


def kusama_transfers(wallet_address):
    # the api request function for getting transfers
    def the_transfers():
        def all_transfer_req(page):
            url = "https://kusama.api.subscan.io/api/scan/transfers"
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




# general###############################################################################################################################################################################


def general_kusama():
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
        response = requests.post('https://kusama.api.subscan.io/api/scan/transfers', headers=headers, json=json_data)
        response = json.loads(response.text)

        transfer_count = response['data']['count']
        transfer_count = format(int(transfer_count), ",")

        fee = response['data']['transfers'][0]['fee']
        fee = decimal_number_formatter(fee)
        coin_gas_fee = format_coins_longer(fee)

        dollar_gas_fee = decimal.Decimal(fee) * decimal.Decimal(kusama_price)
        dollar_gas_fee = format_dollars_longer(dollar_gas_fee)
        dollar_gas_fee = format_dollars_longer(dollar_gas_fee)

        return {'coin_gas_fee': coin_gas_fee, 'dollar_gas_fee': dollar_gas_fee, 'transfer_count': transfer_count}

    kusama_general_return = {'kusama_general': {'current_dates': current_dates(),
                                         'kusama_price': float(kusama_price),
                                         'kusama_market_cap': kusama_market_cap,
                                         'recent_gas': recent_gas(),
                                         'kusama_p_increase': kusama_p_increase}}
    return kusama_general_return






# form data###############################################################################################################################################################################


def join_w_form_app(form_name, form_role, form_email, form_project, form_website, form_net, form_comments):

    def submit_form_telegram(form_name, form_role, form_email, form_project, form_website, form_net, form_comments):
        message = f'** NEW PROJECT SUBMISSION **\n\nTeam Name: {form_project}\nWebsite: {form_website}\nNet: {form_net}\n' \
                  f'Name: {form_name}\nRole: {form_role}\nEmail: {form_email}\nComments: {form_comments}'
        requests.get(f'https://api.telegram.org/bot{telegram_api_key}/sendMessage?chat_id={telegram_chat_id_core}&text={message}')
        return None
    submit_form_telegram(form_name, form_role, form_email, form_project, form_website, form_net, form_comments)

    def submit_form_email(form_name, form_email, form_project):
        try:
            body = f'\nHello {form_name} !\n\n' \
                   f'Thank you very much for being interested in {form_project} joining Wallety.org, if we are ' \
                   f'interested in going further we will email you back ASAP with a time to meet.\n' \
                   f'\nWe hope you have a great day and thanks again, \nWallety.org Auto Reply'
            subject = f'Wallety.org | {form_project}'
            import smtplib
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(email_user, email_pass)
            header = 'To:' + form_email + '\n' + 'From: ' + email_user + '\n' + f'Subject:{subject} \n'
            msg = header + f'{body}'
            smtpserver.sendmail(email_user, form_email, msg)
            smtpserver.quit()
            return None
        except:
            return None
            pass
    submit_form_email(form_name, form_email, form_project)




# suggestion###############################################################################################################################################################################





def suggestion(message, network, email, suggest_type):
    user_message = message
    message = f'** NEW {suggest_type} **\n\nNetwork: {network}\n' \
              f'Type: {suggest_type}\n' \
              f'Email: {email}\n' \
              f'Suggestion: {message}'
    requests.get(f'https://api.telegram.org/bot{telegram_api_key}/sendMessage?chat_id={telegram_chat_id_core}&text={message}')

    def suggest_email(email, suggest_type, user_message):
        try:
            body = f'\nHey there !\n\n' \
                   f'Thank you very much for reporting the {suggest_type}:\n\n' \
                   f'\"{user_message}\"\n\n' \
                   f'We have been notified and will look into it.\n' \
                   f'\nWe hope you have a great day and thanks again, \nWallety.org Auto Reply'
            subject = f'Wallety.org | {suggest_type}'
            import smtplib
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(email_user, email_pass)
            header = 'To:' + email + '\n' + 'From: ' + email_user + '\n' + f'Subject:{subject} \n'
            msg = header + f'{body}'
            smtpserver.sendmail(email_user, email, msg)
            smtpserver.quit()
            return None
        except:
            return None
            pass

    if email != False:
        suggest_email(email, suggest_type, user_message)
    return None





# API apply ###############################################################################################################################################################################



def api_apply(name, email, comments):
    message = {'name': name, 'email': email, 'comments': comments}
    requests.get(f'https://api.telegram.org/bot{telegram_api_key}/sendMessage?chat_id={telegram_chat_id_api}&text={message}')

    def api_email(name, email):
        try:
            body = f'\nHey {name} !\n\n' \
                   f'Thank you very much for applying for our API, we will let you know once it is live !\n' \
                   f'\nWe hope you have a great day and thanks again, \nWallety.org Auto Reply'
            subject = 'Wallety.org | API'
            import smtplib
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(email_user, email_pass)
            header = 'To:' + email + '\n' + 'From: ' + email_user + '\n' + f'Subject:{subject} \n'
            msg = header + f'{body}'
            smtpserver.sendmail(email_user, email, msg)
            smtpserver.quit()
            return None
        except:
            return None
            pass

    api_email(name, email)







# analytics report###############################################################################################################################################################################



def report_analytic(network, wallet_address, display_name):
    try:
        message = {'new_wallet_request': {'hashing_key_start': hashing_key, 'display_name': display_name, 'wallet_address': wallet_address,
                                          'network': network, 'date': current_dates(), 'hashing_key_end': hashing_key}}
        requests.get(f'https://api.telegram.org/bot{telegram_api_key}/sendMessage?chat_id={telegram_chat_id_report}&text={message}')
        clean_message = f'{display_name}\n{network}\n{wallet_address}'
        requests.get(f'https://api.telegram.org/bot{telegram_api_key}/sendMessage?chat_id={telegram_chat_id_report_clean}&text={clean_message}')
        return None
    except:
        return None






# data###############################################################################################################################################################################


def kusama_data(kusama_wallet_address, kusama_wallet_profile, current_dates, kusama_paper_diamond_handed,
                kusama_raw_transfers, general_kusama):

    current_dates = current_dates()
    general_kusama = general_kusama()
    kusama_wallet_profile = kusama_wallet_profile(kusama_wallet_address)
    kusama_transfers_data = kusama_transfers(kusama_wallet_address)
    kusama_monthly_transfers = kusama_monthly_stats(kusama_transfers_data[1], kusama_wallet_address)
    kusama_paper_diamond_handed = kusama_paper_diamond_handed(kusama_transfers_data[2], kusama_wallet_profile[1])

    kusama_top_deposit_withdraws = kusama_top_accounts_withdraw_deposit(kusama_wallet_address,
                                                                        kusama_transfers_data[1]['all_transfers'],
                                                                        kusama_transfers_data[3]['all_deposits'],
                                                                        kusama_transfers_data[2]['all_withdraws'],
                                                                        kusama_monthly_transfers[2]['monthly_deposits'],
                                                                        kusama_monthly_transfers[1]['monthly_withdraws'],
                                                                        kusama_monthly_transfers[3]['monthly_transfers'])

    kusama_raw_transfers = kusama_raw_transfers(kusama_transfers_data[3], kusama_transfers_data[2])
    data = {'wallety_org_kusama_server_status': 200,
            'kusama_wallet_address': kusama_wallet_address,
            'kusama_wallet_profile': kusama_wallet_profile[0],
            'kusama_transfers_data': kusama_transfers_data[0],
            'kusama_monthly_transfers': kusama_monthly_transfers[0],
            'kusama_paper_diamond_handed': kusama_paper_diamond_handed,
            'current_dates': current_dates,
            'kusama_top_deposit_withdraws': kusama_top_deposit_withdraws,
            'kusama_raw_transfers': kusama_raw_transfers,
            'general_kusama': general_kusama}

    return data



# custom data###############################################################################################################################################################################




def custom_kusama_data(all_transfers, wallet_address, custom_to, custom_from):

    def timestamp_c_converter(timestamp):
        from datetime import datetime
        dt_object = datetime.fromtimestamp(timestamp)
        year = dt_object.strftime('%Y')
        year = int(year)
        month = dt_object.strftime('%m')
        month = int(month)
        day = dt_object.strftime('%d')
        day = int(day)
        return [year, month, day]

    def zeroCheck(number):
        if str(number)[0] == 0:
            return int(str(number)[1])
        else:
            return int(number)

    # custom from
    custom_from = str(custom_from)
    from_year = int(custom_from[:4])
    from_month = zeroCheck(custom_from[5:7])
    from_day = zeroCheck(custom_from[8:10])
    custom_from = datetime.date(from_year, from_month, from_day)

    # custom to
    custom_to = str(custom_to)
    to_year = int(custom_to[:4])
    to_month = zeroCheck(custom_to[5:7])
    to_day = zeroCheck(custom_to[8:10])
    custom_to = datetime.date(to_year, to_month, to_day)


    def inToFrom(startTime, endTime, x):
        if startTime <= endTime:
            return startTime <= x <= endTime
        else:
            return startTime <= x or x <= endTime


    # getting custom transactions
    def custom_transactions(all_transfers):
        custom_transactions = []
        for i in all_transfers['all_transfers']:
            block_timestamp = timestamp_c_converter(i['block_timestamp'])
            checking = inToFrom(custom_from, custom_to, datetime.date(block_timestamp[0], block_timestamp[1], block_timestamp[2]))
            if checking == True:
                custom_transactions.append(i)
        return custom_transactions


    custom_transfers = custom_transactions(all_transfers)
    custom_withdraws = []
    custom_deposits = []

    # custom dates title
    title_from = f'{from_day}/{from_month}/{from_year}'
    title_to = f'{to_day}/{to_month}/{to_year}'
    custom_dates_title = '(' + str(title_from) + ' - ' + str(title_to) + ')'

    # custom deposit info's
    custom_deposit_volume_coins = 0

    # custom withdraw info's
    custom_withdrawal_volume_coin = 0
    custom_withdrawal_gas_coin = decimal.Decimal(0)
    custom_withdrawal_failed_gas_coin = decimal.Decimal(0)
    custom_withdrawal_failed_interactions = 0

    # organising into deposit and withdraws
    for i in custom_transfers:
        if i['from'] == wallet_address:
            custom_withdraws.append(i)
        else:
            custom_deposits.append(i)

    # deposit and withdrawal interaction amounts
    custom_deposit_interactions = len(custom_withdraws)
    custom_withdrawal_interactions = len(custom_deposits)

    # getting deposit data
    for i in custom_deposits:
        custom_deposit_volume_coins += float(i['amount'])

    # getting withdrawal data
    for i in custom_withdraws:
        if i['success'] == True:
            custom_withdrawal_volume_coin += float(i['amount'])
            custom_withdrawal_gas_coin += decimal_number_formatter(i['fee'])
        else:
            custom_withdrawal_failed_gas_coin += decimal_number_formatter((i['fee']))
            custom_withdrawal_failed_interactions += 1

    # total asset volume
    custom_total_volume_coins = 0

    # getting total txn info
    for i in custom_transfers:
        # Wallet volume
        custom_total_volume_coins += float(i['amount'])

    # fee paid dollar worth
    custom_withdrawal_failed_gas_dollars = custom_withdrawal_failed_gas_coin * decimal.Decimal(kusama_price)
    custom_withdrawal_gas_dollars = custom_withdrawal_gas_coin * decimal.Decimal(kusama_price)

    # deposit, withdrawal and total dollar worth
    custom_total_volume_dollars = custom_total_volume_coins * float(kusama_price)
    custom_deposit_volume_dollars = custom_deposit_volume_coins * float(kusama_price)
    custom_withdrawal_volume_dollars = custom_withdrawal_volume_coin * float(kusama_price)

    # formatting numbers
    # total
    custom_total_volume_coins = format_coins(custom_total_volume_coins)
    custom_total_volume_dollars = format_dollars(custom_total_volume_dollars)
    # withdrawal
    custom_withdrawal_volume_coin = format_coins(custom_withdrawal_volume_coin)
    custom_withdrawal_volume_dollars = format_dollars(custom_withdrawal_volume_dollars)
    custom_withdrawal_gas_coin = format_coins(custom_withdrawal_gas_coin)
    custom_withdrawal_gas_dollars = format_dollars(custom_withdrawal_gas_dollars)
    custom_withdrawal_failed_gas_coin = format_coins(custom_withdrawal_failed_gas_coin)
    custom_withdrawal_failed_gas_dollars = format_dollars(custom_withdrawal_failed_gas_dollars)
    # deposit
    custom_deposit_volume_coins = format_coins(custom_deposit_volume_coins)
    custom_deposit_volume_dollars = format_dollars(custom_deposit_volume_dollars)
    # first txn dates
    custom_withdrawal_first_txn_date = kusama_first_txn_dates(custom_withdraws)
    custom_deposits_first_txn_date = kusama_first_txn_dates(custom_deposits)
    custom_total_first_txn_date = kusama_first_txn_dates(custom_transfers)
    # last txn dates
    custom_withdrawal_last_txn_date = kusama_last_txn_dates(custom_withdraws)
    custom_deposits_last_txn_date = kusama_last_txn_dates(custom_deposits)
    custom_total_last_txn_date = kusama_last_txn_dates(custom_transfers)

    return {'custom_total': {'custom_total_volume_coins': custom_total_volume_coins,
                             'custom_total_volume_dollars': custom_total_volume_dollars,
                             'custom_total_interactions': custom_deposit_interactions + custom_withdrawal_interactions + custom_withdrawal_failed_interactions,
                             'custom_total_gas_coin': custom_withdrawal_gas_coin,
                             'custom_total_gas_dollars': custom_withdrawal_gas_dollars,
                             'custom_total_failed_gas_coin': custom_withdrawal_failed_gas_coin,
                             'custom_total_failed_gas_dollars': custom_withdrawal_failed_gas_dollars,
                             'custom_dates_title': custom_dates_title,
                             'custom_total_first_txn_date': custom_total_first_txn_date,
                             'custom_total_last_txn_date': custom_total_last_txn_date
                             },
            'custom_withdrawal': {'custom_withdrawal_volume_coin': custom_withdrawal_volume_coin,
                                  'custom_withdrawal_volume_dollars': custom_withdrawal_volume_dollars,
                                  'custom_withdrawal_interactions': custom_withdrawal_interactions,
                                  'custom_withdrawal_failed_interactions': custom_withdrawal_failed_interactions,
                                  'custom_withdrawal_gas_coin': custom_withdrawal_gas_coin,
                                  'custom_withdrawal_gas_dollars': custom_withdrawal_gas_dollars,
                                  'custom_withdrawal_failed_gas_coin': custom_withdrawal_failed_gas_coin,
                                  'custom_withdrawal_failed_gas_dollars': custom_withdrawal_failed_gas_dollars,
                                  'custom_withdrawal_first_txn_date': custom_withdrawal_first_txn_date,
                                  'custom_withdrawal_last_txn_date': custom_withdrawal_last_txn_date
                                  },
            'custom_deposit': {'custom_deposit_volume_coins': custom_deposit_volume_coins,
                               'custom_deposit_volume_dollars': custom_deposit_volume_dollars,
                               'custom_deposit_interactions': custom_deposit_interactions,
                               'custom_deposits_first_txn_date': custom_deposits_first_txn_date,
                               'custom_deposits_last_txn_date': custom_deposits_last_txn_date
                               }}, \
           {'custom_withdraws': custom_withdraws}, \
           {'custom_deposits': custom_deposits}, \
           {'custom_transfers': custom_transfers}





# custom top accounts###############################################################################################################################################################################





def custom_top_accounts_withdraw_deposit(wallet_address, custom_deposits, custom_withdrawals, custom_transactions):

    # formatting input data
    custom_deposits = custom_deposits['custom_deposits']
    custom_withdrawals = custom_withdrawals['custom_withdraws']
    custom_transactions = custom_transactions['custom_transfers']

    def custom_top_accounts(wallet_address, customTransfers, withdraw_or_deposit):

        w_d_indicator = withdraw_or_deposit
        if withdraw_or_deposit == "withdraw":
            withdraw_or_deposit = 'to'
            account_display = 'to_account_display'
        else:
            withdraw_or_deposit = 'from'
            account_display = 'from_account_display'

        # pi chart data
        coin_amount = {}
        fees_coin = {}
        fees_dollars = {}
        interacted_times = {}
        wallet_names = {}
        failed_interacted_times = {}
        rawFLtxns = {}

        for index, i in enumerate(customTransfers):
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

                    if i[account_display]['identity']:
                        wallet_names[i[withdraw_or_deposit]] = i[account_display]['display']
                    else:
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

        # pi chart info
        total_coin_volume = 0
        for i in coin_amount.items():
            total_coin_volume += float(i[1])

        coin_pi_chart_percentage = {}
        for i in coin_amount.items():
            coin_pi_chart_percentage[i[0]] = (float(i[1]) / total_coin_volume) * 100

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
            data[address] = i

        return {'data': data}, {f'{w_d_indicator}_unformatted_data': unformatted_data}, {'rawFLtxns': rawFLtxns}

    # total top accounts
    def total_top_transfer_accounts(total_deposits, total_withdrawals):

        # all_total_transfers
        total_deposits = total_deposits['deposit_unformatted_data']
        try:
            first_address = list(total_deposits)[0]
            depositVolume = total_deposits[first_address]['XXX_coin_volume']
        except IndexError:
            depositVolume = 0
        total_withdrawals = total_withdrawals['withdraw_unformatted_data']
        try:
            first_address = list(total_withdrawals)[0]
            withdrawalsVolume = total_withdrawals[first_address]['XXX_coin_volume']
        except IndexError:
            withdrawalsVolume = 0

        total_XX = depositVolume + withdrawalsVolume

        all_total_transfers = {}

        for i in total_deposits.items():
            all_total_transfers[i[0]] = {'total_address': i[0],
                                         'total_coin_amount': float(i[1]['deposit_coin_amount']),
                                         'total_coin_fee': decimal.Decimal(i[1]['deposit_coin_fee']),
                                         'total_coin_fee_dollars': decimal.Decimal(i[1]['deposit_coin_fee_dollars']),
                                         'total_display_name': i[1]['deposit_display_name'],
                                         'total_interaction_times': i[1]['deposit_interaction_times'],
                                         'total_failed_interaction_times': i[1]['deposit_failed_interaction_times'],
                                         'total_pi_chart_percent': i[1]['deposit_pi_chart_percent']
                                         }

        for i in total_withdrawals.items():
            if i[0] in all_total_transfers:
                dict_transfers = dict(all_total_transfers[i[0]])
                all_total_transfers[i[0]] = {'total_address': i[0],
                                             'total_coin_amount': float(i[1]['withdraw_coin_amount']) + dict_transfers['total_coin_amount'],
                                             'total_coin_fee': decimal.Decimal(i[1]['withdraw_coin_fee']) + dict_transfers['total_coin_fee'],
                                             'total_coin_fee_dollars': decimal.Decimal(i[1]['withdraw_coin_fee_dollars']) + dict_transfers['total_coin_fee_dollars'],
                                             'total_display_name': i[1]['withdraw_display_name'],
                                             'total_interaction_times': i[1]['withdraw_interaction_times'] + dict_transfers['total_interaction_times'],
                                             'total_failed_interaction_times': i[1]['withdraw_failed_interaction_times'] + dict_transfers['total_failed_interaction_times'],
                                             }
            else:
                all_total_transfers[i[0]] = {'total_address': i[0],
                                             'total_coin_amount': i[1]['withdraw_coin_amount'],
                                             'total_coin_fee': i[1]['withdraw_coin_fee'],
                                             'total_coin_fee_dollars': i[1]['withdraw_coin_fee_dollars'],
                                             'total_display_name': i[1]['withdraw_display_name'],
                                             'total_interaction_times': i[1]['withdraw_interaction_times'],
                                             'total_failed_interaction_times': i[1]['withdraw_failed_interaction_times'],
                                             'total_pi_chart_percent': i[1]['withdraw_pi_chart_percent']
                                             }



        return {'all_total_transfers': all_total_transfers, 'total_XX': total_XX}


    # some data
    # total deposits
    deposits_data = custom_top_accounts(wallet_address, custom_deposits, 'deposit')
    deposits = deposits_data[0]
    unformatted_deposits = deposits_data[1]
    deposits_rawFLtxns = deposits_data[2]
    # total withdrawals
    withdrawals_data = custom_top_accounts(wallet_address, custom_withdrawals, 'withdraw')
    withdrawals = withdrawals_data[0]
    unformatted_withdrawals = withdrawals_data[1]
    withdrawals_rawFLtxns = withdrawals_data[2]

    # total data
    total_data = total_top_transfer_accounts(unformatted_deposits, unformatted_withdrawals)
    # total total
    total = total_data['all_total_transfers']
    total_XX = total_data['total_XX']
    # total flx
    total_rawFLtxns = {}
    for i in custom_transactions:
        if i['from'] != wallet_address:
            unique_wd = 'from'
        else:
            unique_wd = 'to'
        if i[unique_wd] not in total_rawFLtxns:
            total_rawFLtxns[i[unique_wd]] = [i]
        else:
            total_rawFLtxns[i[unique_wd]].append(i)

    total_rawFLtxns = {'total_rawFLtxns': total_rawFLtxns}

    # times time function
    def time_times(possible):
        if int(possible) == 1:
            return 'time'
        else:
            return 'times'

    # formatting total deposits data
    deposits_formatted = []
    for i in deposits['data'].items():
        tier = i[1]
        deposit_display_name = tier['deposit_display_name']
        deposit_address = tier['deposit_address']
        deposit_dollar_amount = format_dollars(format_coins_machine(tier['deposit_coin_amount']) * float(kusama_price))
        deposit_coin_amount = format_coins(tier['deposit_coin_amount'])
        deposit_pi_chart_percent = percentage_format(tier['deposit_pi_chart_percent'])
        deposit_coin_fee = format_coins_longer(tier['deposit_coin_fee'])
        deposit_coin_fee_dollars = format_dollars_longer(tier['deposit_coin_fee_dollars'])
        deposit_interaction_times = tier['deposit_interaction_times']
        deposit_interaction_times_times = time_times(tier['deposit_interaction_times'])
        deposit_failed_interaction_times = tier['deposit_failed_interaction_times']
        deposit_failed_interaction_times_times = time_times(tier['deposit_failed_interaction_times'])
        deposit_first_txn = kusama_first_txn_dates(deposits_rawFLtxns['rawFLtxns'][tier['deposit_address']])
        first_txn = deposit_first_txn['first_txn_full_date']
        first_days_since = deposit_first_txn['days_since']
        deposit_last_txn = kusama_last_txn_dates(deposits_rawFLtxns['rawFLtxns'][tier['deposit_address']])
        last_txn = deposit_last_txn['last_txn_full_date']
        last_days_since = deposit_last_txn['days_since']

        deposits_formatted.append([f'{deposit_display_name} ({deposit_address}) has deposited a total of {deposit_coin_amount} (',
                                   deposit_dollar_amount,
                                   f') which accounts for {deposit_pi_chart_percent} of your total deposits. They have spent {deposit_coin_fee} (',
                                   deposit_coin_fee_dollars,
                                   f') on gas with you and deposited {deposit_interaction_times} {deposit_interaction_times_times} in total, '
                                   f'in which {deposit_failed_interaction_times} {deposit_failed_interaction_times_times} they failed. '
                                   f'Your first transaction with them was {first_txn} {first_days_since} and your last transaction with them was {last_txn} {last_days_since}.'])
    if deposits_formatted == []:
        deposits_formatted.append('-')


    # formatting total withdrawals data
    withdrawals_formatted = []
    for i in withdrawals['data'].items():
        tier = i[1]
        withdraw_display_name = tier['withdraw_display_name']
        withdraw_address = tier['withdraw_address']
        withdraw_dollar_amount = format_dollars(format_coins_machine(tier['withdraw_coin_amount']) * float(kusama_price))
        withdraw_coin_amount = format_coins(tier['withdraw_coin_amount'])
        withdraw_pi_chart_percent = percentage_format(tier['withdraw_pi_chart_percent'])
        withdraw_coin_fee = format_coins_longer(tier['withdraw_coin_fee'])
        withdraw_coin_fee_dollars = format_dollars_longer(tier['withdraw_coin_fee_dollars'])
        withdraw_interaction_times = tier['withdraw_interaction_times']
        withdraw_interaction_times_times = time_times(tier['withdraw_interaction_times'])
        withdraw_failed_interaction_times = tier['withdraw_failed_interaction_times']
        withdraw_failed_interaction_times_times = time_times(tier['withdraw_failed_interaction_times'])
        withdraw_first_txn = kusama_first_txn_dates(withdrawals_rawFLtxns['rawFLtxns'][tier['withdraw_address']])
        first_txn = withdraw_first_txn['first_txn_full_date']
        first_days_since = withdraw_first_txn['days_since']
        withdraw_last_txn = kusama_last_txn_dates(withdrawals_rawFLtxns['rawFLtxns'][tier['withdraw_address']])
        last_txn = withdraw_last_txn['last_txn_full_date']
        last_days_since = withdraw_last_txn['days_since']

        withdrawals_formatted.append([f'You have withdrawn to {withdraw_display_name} ({withdraw_address}) a total of {withdraw_coin_amount} (',
                                      withdraw_dollar_amount,
                                      f') which accounts for {withdraw_pi_chart_percent} of your total withdrawals. You have spent {withdraw_coin_fee} (',
                                      withdraw_coin_fee_dollars,
                                      f') on gas doing this and withdrawn {withdraw_interaction_times} {withdraw_interaction_times_times} in total, '
                                      f'in which {withdraw_failed_interaction_times} {withdraw_failed_interaction_times_times} they failed. '
                                      f'Your first transaction with them was {first_txn} {first_days_since} and your last transaction with them was {last_txn} {last_days_since}.'])
    if withdrawals_formatted == []:
        withdrawals_formatted.append('-')


    # formatting total total data
    total_formatted = []
    for i in total.items():
        tier = i[1]
        total_display_name = tier['total_display_name']
        total_address = tier['total_address']
        total_dollar_amount = format_dollars(format_coins_machine(tier['total_coin_amount']) * float(kusama_price))
        total_coin_amount = format_coins(tier['total_coin_amount'])
        total_pi_chart_percent = percentage_format((float(tier['total_coin_amount']) / float(total_XX)) * 100)
        total_coin_fee = format_coins_longer(tier['total_coin_fee'])
        total_coin_fee_dollars = format_dollars_longer(tier['total_coin_fee_dollars'])
        total_interaction_times = tier['total_interaction_times']
        total_interaction_times_times = time_times(tier['total_interaction_times'])
        total_failed_interaction_times = tier['total_failed_interaction_times']
        total_failed_interaction_times_times = time_times(tier['total_failed_interaction_times'])
        total_first_txn = kusama_first_txn_dates(total_rawFLtxns['total_rawFLtxns'][tier['total_address']])
        first_txn = total_first_txn['first_txn_full_date']
        first_days_since = total_first_txn['days_since']
        total_last_txn = kusama_last_txn_dates(total_rawFLtxns['total_rawFLtxns'][tier['total_address']])
        last_txn = total_last_txn['last_txn_full_date']
        last_days_since = total_last_txn['days_since']

        total_formatted.append([f'You and {total_display_name} ({total_address}) have had a total volume of {total_coin_amount} (',
                                total_dollar_amount,
                                f') which accounts for {total_pi_chart_percent} of your total volume. Between you both have spent {total_coin_fee} (',
                                total_coin_fee_dollars,
                                f') on gas and interacted {total_interaction_times} {total_interaction_times_times} in total, '
                                f'in which {total_failed_interaction_times} {total_failed_interaction_times_times} they failed. '
                                f'Your first transaction with them was {first_txn} {first_days_since} and your last transaction with them was {last_txn} {last_days_since}.'])
    if total_formatted == []:
        total_formatted.append('-')


    return {'all_top_accounts': {'all_deposits': deposits_formatted, 'all_withdrawals': withdrawals_formatted,
                                 'all_total': total_formatted}}




# wallet check###############################################################################################################################################################################



def wallet_check(wallet_address):
    def network_check(network, wallet_address):
        url = f"https://{network}.api.subscan.io/api/v2/scan/search"
        payload = json.dumps({"key": wallet_address})
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': subscan_api_key}
        response = requests.request("POST", url, headers=headers, data=payload).text
        response = json.loads(response)
        if response['message'] == 'Record Not Found':
            return False
        elif response['data']['account']['address'] == wallet_address:
            return network
    network = False
    polkadot_check = network_check('polkadot', wallet_address)
    if polkadot_check == 'polkadot':
        network = 'polkadot'
    else:
        kusama_check = network_check('kusama', wallet_address)
        if kusama_check == 'kusama':
            network = 'kusama'
    return {'wallet_network': network}


# DEV TEST PRINTING #######################################################################################################################################################


# json_data = json.dumps(kusama_data(test_wallet_address_kusama, kusama_wallet_profile, current_dates, kusama_paper_diamond_handed, kusama_raw_transfers, general_kusama))
# # import pprint
# # pprint.pp(json_data)
# print(json_data)



# SERER SETUP #######################################################################################################################################################
# The whole server
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
    try:
        requests.get(f'https://api.telegram.org/bot{telegram_api_key}/sendMessage?chat_id={telegram_chat_id_website_hits}&text=Hit')
    except:
        pass
    return Response(dumps({'wallety_org_server_status': 200}), mimetype='text/json')
# Wallet check #####################################################################################################################################################
@app.route('/walletcheck/', methods=['GET'])
def wallet_check_page():
    try:
        wallet_address = str(request.args.get('wallet_address'))
        json_dump = json.dumps(wallet_check(wallet_address))
        return json_dump
    except:
        return {'wallety_org_wallet_check_server_status': 500, 'response': 'internal server error, please try again later'}
# Join wallety form ##################################################################################################################################################
@app.route('/joinwalletyform/', methods=['GET'])
def join_w_form():
    try:
        form_name = str(request.args.get('form_name'))
        form_role = str(request.args.get('form_role'))
        form_email = str(request.args.get('form_email'))
        form_project = str(request.args.get('form_project'))
        form_website = str(request.args.get('form_website'))
        form_net = str(request.args.get('form_net'))
        form_comments = str(request.args.get('form_comments'))
        join_w_form_app(form_name, form_role, form_email, form_project, form_website, form_net, form_comments)
        return {'wallety_org_join_wallety_server_status': 200, 'response': True}
    except:
        return {'wallety_org_join_wallety_server_status': 500, 'response': 'internal server error, please try again later'}
# Suggest/bug report ##################################################################################################################################################
@app.route('/suggestion/', methods=['GET'])
def suggestion_form():
    try:
        message = str(request.args.get('suggestion'))
        network = str(request.args.get('network'))
        email = str(request.args.get('suggest_email'))
        suggest_type = str(request.args.get('suggest_type'))
        suggestion(message, network, email, suggest_type)
        return {'wallety_org_suggest_bug_server_status': 200, 'response': True}
    except:
        return {'wallety_org_suggest_bug_server_status': 500, 'response': 'internal server error, please try again later'}
# API wait list ##################################################################################################################################################
@app.route('/api_apply/', methods=['GET'])
def apiApply():
    try:
        name = str(request.args.get('name'))
        email = str(request.args.get('email'))
        comments = str(request.args.get('comments'))
        api_apply(name, email, comments)
        return {'wallety_org_api_apply_server_status': 200, 'response': True}
    except:
        return {'wallety_org_api_apply_server_status': 500, 'response': 'internal server error, please try again later'}
# KUSAMA ###############################################################################################################################################################
# kusama data ##########################################################################################################################################################
@app.route('/kusama/', methods=['GET']) # http://127.0.0.1:7777/kusama/?wallet_address=
def kusama_request_page():
    try:
        wallet_address = str(request.args.get('wallet_address'))
        json_data = json.dumps(kusama_data(wallet_address, kusama_wallet_profile, current_dates, kusama_paper_diamond_handed, kusama_raw_transfers, general_kusama))
        return json_data
    except:
        return {'wallety_org_kusama_server_status': 500, 'response': 'internal server error, please try again later'}
# custom kusama data ####################################################################################################################################################
@app.route('/kusama/customdata/', methods=['GET'])
def kusama_custom_data():
    try:
        wallet_address = str(request.args.get('wallet_address'))
        custom_to = str(request.args.get('to'))
        custom_from = str(request.args.get('from'))
        all_transfers_custom = kusama_transfers(wallet_address)[1]
        custom_data = custom_kusama_data(all_transfers_custom, wallet_address, custom_to, custom_from)
        custom_top_accounts = custom_top_accounts_withdraw_deposit(wallet_address, custom_data[2], custom_data[1], custom_data[3])
        return_custom = {'custom_data_total': custom_data[0]['custom_total'],
                         'custom_data_withdrawals': custom_data[0]['custom_withdrawal'],
                         'custom_data_deposits': custom_data[0]['custom_deposit'],
                         'custom_top_accounts': custom_top_accounts
                         }
        json_data = json.dumps(return_custom)
        return json_data
    except:
        return {'wallety_org_custom_data_server_status': 500, 'response': 'internal server error, please try again later'}
# kusama general ##########################################################################################################################################################
@app.route('/kusama/general/', methods=['GET']) # http://127.0.0.1:5000/kusama/general/
def kusama_general():
    try:
        json_dump = json.dumps(general_kusama())
        return json_dump
    except:
        return {'wallety_org_kusama_general_server_status': 500, 'response': 'internal server error, please try again later'}
# RUN SERVER ##############################################################################################################################################################
if __name__ == '__main__':
    app.run(port=7777)
