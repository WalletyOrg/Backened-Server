import decimal
from kusama import kusama_wallet_short_name, decimal_number_formatter, kusama_price, raw_transfer_format_timestamp, \
    format_coins, format_dollars, format_dollars_longer, format_coins_longer



def rawTransfers(all_deposits, all_withdrawals):
    deposit_transfers = []
    for i in all_deposits['all_deposits']:
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




