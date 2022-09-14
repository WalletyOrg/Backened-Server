import decimal
from universal_functions import decimal_number_formatter, wallet_short_name, format_dollars, format_coins, \
    format_coins_machine, format_dollars_longer, format_coins_longer, percentage_format, first_txn_dates, last_txn_dates




def uniqueWallets(wallet_address, all_transactions, all_deposits, all_withdrawals, monthly_deposits,
                  monthly_withdrawals, monthly_transactions, coin_price, network):

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
                    fees_dollars[i[withdraw_or_deposit]] = decimal_number_formatter(i['fee']) * decimal.Decimal(coin_price)
                    interacted_times[i[withdraw_or_deposit]] = 1

                    try:
                        if i[account_display]['identity']:
                            wallet_names[i[withdraw_or_deposit]] = i[account_display]['display']
                        else:
                            wallet_names[i[withdraw_or_deposit]] = wallet_short_name(i[withdraw_or_deposit])
                    except:
                        wallet_names[i[withdraw_or_deposit]] = wallet_short_name(i[withdraw_or_deposit])

                # adding onto original value
                else:
                    if i['success'] == True:
                        coin_amount[i[withdraw_or_deposit]] = float(float(coin_amount[i[withdraw_or_deposit]]) + float(i['amount']))
                        interacted_times[i[withdraw_or_deposit]] += 1
                    else:
                        failed_interacted_times[i[withdraw_or_deposit]] += 1
                        interacted_times[i[withdraw_or_deposit]] += 1

                    fees_coin[i[withdraw_or_deposit]] = fees_coin[i[withdraw_or_deposit]] + decimal_number_formatter(i['fee'])
                    fees_dollars[i[withdraw_or_deposit]] = decimal.Decimal(fees_coin[i[withdraw_or_deposit]]) * decimal.Decimal(coin_price)

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
    deposits_data = top_accounts(wallet_address, all_deposits, 'deposit')
    deposits = deposits_data[0]
    unformatted_deposits = deposits_data[1]
    deposits_rawFLtxns = deposits_data[2]
    # ALL total withdrawals
    withdrawals_data = top_accounts(wallet_address, all_withdrawals, 'withdraw')
    withdrawals = withdrawals_data[0]
    unformatted_withdrawals = withdrawals_data[1]
    withdrawals_rawFLtxns = withdrawals_data[2]
    # monthly deposits
    deposits_monthly_data = top_accounts(wallet_address, monthly_deposits, 'deposit')
    deposits_monthly = deposits_monthly_data[0]
    monthly_unformatted_deposits = deposits_monthly_data[1]
    monthly_deposits_rawFLtxns = deposits_monthly_data[2]
    # monthly withdrawals
    withdrawals_monthly_data = top_accounts(wallet_address, monthly_withdrawals, 'withdraw')
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
        deposit_dollar_amount = format_dollars(format_coins_machine(tier['deposit_coin_amount']) * float(coin_price))
        deposit_coin_amount = format_coins(tier['deposit_coin_amount'], network)
        deposit_pi_chart_percent = percentage_format(tier['deposit_pi_chart_percent'])
        deposit_coin_fee = format_coins_longer(tier['deposit_coin_fee'], network)
        deposit_coin_fee_dollars = format_dollars_longer(tier['deposit_coin_fee_dollars'])
        deposit_interaction_times = tier['deposit_interaction_times']
        deposit_interaction_times_times = time_times(tier['deposit_interaction_times'])
        deposit_failed_interaction_times = tier['deposit_failed_interaction_times']
        deposit_failed_interaction_times_times = time_times(tier['deposit_failed_interaction_times'])
        deposit_first_txn = first_txn_dates(deposits_rawFLtxns['rawFLtxns'][tier['deposit_address']])
        first_txn = deposit_first_txn['first_txn_full_date']
        first_days_since = deposit_first_txn['days_since']
        deposit_last_txn = last_txn_dates(deposits_rawFLtxns['rawFLtxns'][tier['deposit_address']])
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
        withdraw_dollar_amount = format_dollars(format_coins_machine(tier['withdraw_coin_amount']) * float(coin_price))
        withdraw_coin_amount = format_coins(tier['withdraw_coin_amount'], network)
        withdraw_pi_chart_percent = percentage_format(tier['withdraw_pi_chart_percent'])
        withdraw_coin_fee = format_coins_longer(tier['withdraw_coin_fee'], network)
        withdraw_coin_fee_dollars = format_dollars_longer(tier['withdraw_coin_fee_dollars'])
        withdraw_interaction_times = tier['withdraw_interaction_times']
        withdraw_interaction_times_times = time_times(tier['withdraw_interaction_times'])
        withdraw_failed_interaction_times = tier['withdraw_failed_interaction_times']
        withdraw_failed_interaction_times_times = time_times(tier['withdraw_failed_interaction_times'])
        withdraw_first_txn = first_txn_dates(withdrawals_rawFLtxns['rawFLtxns'][tier['withdraw_address']])
        first_txn = withdraw_first_txn['first_txn_full_date']
        first_days_since = withdraw_first_txn['days_since']
        withdraw_last_txn = last_txn_dates(withdrawals_rawFLtxns['rawFLtxns'][tier['withdraw_address']])
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
        total_dollar_amount = format_dollars(format_coins_machine(tier['total_coin_amount']) * float(coin_price))
        total_coin_amount = format_coins(tier['total_coin_amount'], network)
        total_pi_chart_percent = percentage_format((float(tier['total_coin_amount']) / float(total_XX)) * 100)
        total_coin_fee = format_coins_longer(tier['total_coin_fee'], network)
        total_coin_fee_dollars = format_dollars_longer(tier['total_coin_fee_dollars'])
        total_interaction_times = tier['total_interaction_times']
        total_interaction_times_times = time_times(tier['total_interaction_times'])
        total_failed_interaction_times = tier['total_failed_interaction_times']
        total_failed_interaction_times_times = time_times(tier['total_failed_interaction_times'])
        total_first_txn = first_txn_dates(total_rawFLtxns['total_rawFLtxns'][tier['total_address']])
        first_txn = total_first_txn['first_txn_full_date']
        first_days_since = total_first_txn['days_since']
        total_last_txn = last_txn_dates(total_rawFLtxns['total_rawFLtxns'][tier['total_address']])
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
        deposit_dollar_amount = format_dollars(format_coins_machine(tier['deposit_coin_amount']) * float(coin_price))
        deposit_coin_amount = format_coins(tier['deposit_coin_amount'], network)
        deposit_pi_chart_percent = percentage_format(tier['deposit_pi_chart_percent'])
        deposit_coin_fee = format_coins_longer(tier['deposit_coin_fee'], network)
        deposit_coin_fee_dollars = format_dollars_longer(tier['deposit_coin_fee_dollars'])
        deposit_interaction_times = tier['deposit_interaction_times']
        deposit_interaction_times_times = time_times(tier['deposit_interaction_times'])
        deposit_failed_interaction_times = tier['deposit_failed_interaction_times']
        deposit_failed_interaction_times_times = time_times(tier['deposit_failed_interaction_times'])
        deposit_first_txn = first_txn_dates(monthly_deposits_rawFLtxns['rawFLtxns'][tier['deposit_address']])
        first_txn = deposit_first_txn['first_txn_full_date']
        first_days_since = deposit_first_txn['days_since']
        deposit_last_txn = last_txn_dates(monthly_deposits_rawFLtxns['rawFLtxns'][tier['deposit_address']])
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
        withdraw_dollar_amount = format_dollars(format_coins_machine(tier['withdraw_coin_amount']) * float(coin_price))
        withdraw_coin_amount = format_coins(tier['withdraw_coin_amount'], network)
        withdraw_pi_chart_percent = percentage_format(tier['withdraw_pi_chart_percent'])
        withdraw_coin_fee = format_coins_longer(tier['withdraw_coin_fee'], network)
        withdraw_coin_fee_dollars = format_dollars_longer(tier['withdraw_coin_fee_dollars'])
        withdraw_interaction_times = tier['withdraw_interaction_times']
        withdraw_interaction_times_times = time_times(tier['withdraw_interaction_times'])
        withdraw_failed_interaction_times = tier['withdraw_failed_interaction_times']
        withdraw_failed_interaction_times_times = time_times(tier['withdraw_failed_interaction_times'])
        withdraw_first_txn = first_txn_dates(monthly_withdrawals_rawFLtxns['rawFLtxns'][tier['withdraw_address']])
        first_txn = withdraw_first_txn['first_txn_full_date']
        first_days_since = withdraw_first_txn['days_since']
        withdraw_last_txn = last_txn_dates(monthly_withdrawals_rawFLtxns['rawFLtxns'][tier['withdraw_address']])
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
        total_dollar_amount = format_dollars(format_coins_machine(tier['monthly_total_coin_amount']) * float(coin_price))
        total_coin_amount = format_coins(tier['monthly_total_coin_amount'], network)
        total_pi_chart_percent = percentage_format((float(tier['monthly_total_coin_amount']) / float(monthly_XX)) * 100)
        total_coin_fee = format_coins_longer(tier['monthly_total_coin_fee'], network)
        total_coin_fee_dollars = format_dollars_longer(tier['monthly_total_coin_fee_dollars'])
        total_interaction_times = tier['monthly_total_interaction_times']
        total_interaction_times_times = time_times(tier['monthly_total_interaction_times'])
        total_failed_interaction_times = tier['monthly_total_failed_interaction_times']
        total_failed_interaction_times_times = time_times(tier['monthly_total_failed_interaction_times'])
        total_first_txn = first_txn_dates(monthly_rawFLtxns['monthly_rawFLtxns'][tier['monthly_total_address']])
        first_txn = total_first_txn['first_txn_full_date']
        first_days_since = total_first_txn['days_since']
        total_last_txn = last_txn_dates(monthly_rawFLtxns['monthly_rawFLtxns'][tier['monthly_total_address']])
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
