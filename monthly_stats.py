import decimal
from universal_functions import decimal_number_formatter, format_dollars, format_coins, kusama_timestamp_converter, \
    format_dollars_longer, format_coins_longer, kusama_first_txn_dates, kusama_last_txn_dates, current_dates_short
from kusama import kusama_price


def monthlyStats(all_transfers, wallet_address):

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


