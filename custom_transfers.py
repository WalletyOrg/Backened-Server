import datetime
import decimal
from universal_functions import decimal_number_formatter, format_coins, format_dollars, first_txn_dates, last_txn_dates



def customTransfers(all_transfers, wallet_address, custom_to, custom_from, coin_price):

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
    custom_withdrawal_failed_gas_dollars = custom_withdrawal_failed_gas_coin * decimal.Decimal(coin_price)
    custom_withdrawal_gas_dollars = custom_withdrawal_gas_coin * decimal.Decimal(coin_price)

    # deposit, withdrawal and total dollar worth
    custom_total_volume_dollars = custom_total_volume_coins * float(coin_price)
    custom_deposit_volume_dollars = custom_deposit_volume_coins * float(coin_price)
    custom_withdrawal_volume_dollars = custom_withdrawal_volume_coin * float(coin_price)

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
    custom_withdrawal_first_txn_date = first_txn_dates(custom_withdraws)
    custom_deposits_first_txn_date = first_txn_dates(custom_deposits)
    custom_total_first_txn_date = first_txn_dates(custom_transfers)
    # last txn dates
    custom_withdrawal_last_txn_date = last_txn_dates(custom_withdraws)
    custom_deposits_last_txn_date = last_txn_dates(custom_deposits)
    custom_total_last_txn_date = last_txn_dates(custom_transfers)

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

