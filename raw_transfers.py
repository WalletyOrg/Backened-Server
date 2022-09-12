import decimal
from universal_functions import wallet_short_name, decimal_number_formatter, \
    format_coins, format_dollars, format_dollars_longer, format_coins_longer
from kusama import kusama_price



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




def rawTransfers(all_deposits, all_withdrawals):
    deposit_transfers = []
    for i in all_deposits['all_deposits']:
        display_name = wallet_short_name(i['from'])
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
        display_name = wallet_short_name(i['to'])
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




