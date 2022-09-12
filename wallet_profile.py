import requests
import json
from keys import *
from kusama import kusama_wallet_short_name, format_coins, format_dollars, kusama_price, decimal_number_formatter
from universal_functions import report_analytic


def wallet_profile(wallet_address, network):
    url = f"https://{network}.api.subscan.io/api/v2/scan/search"
    payload = json.dumps({"key": wallet_address})
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': subscan_api_key}
    response = requests.request("POST", url, headers=headers, data=payload).text
    response = json.loads(response)

    # identity
    try:
        identity = response['data']['account']['account_display']['identity']
        if identity != False:
            identity = True
        else:
            identity = False
    except:
        identity = False
    # display name
    try:
        display_name = response['data']['account']['account_display']['display']
        if display_name == '':
            display_name = kusama_wallet_short_name(wallet_address)
    except:
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
    try:
        if str(response['data']['account']['judgements']) == str(None):
            judgements = False
        else:
            judgements = True
    except:
        judgements = False
    # checking if sub account
    try:
        if response['data']['account']['account_display']['parent'] == None:
            sub = False
        else:
            sub = True
    except:
        sub = False
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
        response = requests.post(f'https://{network}.api.subscan.io/api/scan/staking/nominator', headers=headers, json=json_data).text
        response = json.loads(response)
        if response['data'] == None:
            response = None
        else:
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
        headers = {'X-API-Key': subscan_api_key}
        json_data = {}
        response = requests.post(f'https://{network}.api.subscan.io/api/scan/staking/validators', headers=headers, json=json_data).text
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



    # network addresses
    def all_wallet_formats(wallet_address):
        def network_check(network, wallet_address):
            url = f"https://{network}.api.subscan.io/api/v2/scan/search"
            payload = json.dumps({"key": wallet_address})
            headers = {
                'Content-Type': 'application/json',
                'X-API-Key': subscan_api_key}
            response = requests.request("POST", url, headers=headers, data=payload).text
            response = json.loads(response)

            network_response = False
            if response['message'] == 'Record Not Found':
                network_response = False

            elif response['data']['account']['address'] == wallet_address:
                network_response = network
            try:
                wallet_address = response['data']['account']['address']
            except KeyError:
                wallet_address = False
            network_data = {'network_response': network_response, 'wallet_address': wallet_address}
            return network_data

        networks = {'kusama': '', 'polkadot': ''}
        polkadot_check = network_check('polkadot', wallet_address)
        networks['polkadot'] = polkadot_check['wallet_address']
        kusama_check = network_check('kusama', wallet_address)
        networks['kusama'] = kusama_check['wallet_address']

        return {'wallet_networks': networks}

    network_addresses = all_wallet_formats(wallet_address)
    polkadot_address = network_addresses['wallet_networks']['polkadot']
    kusama_address = network_addresses['wallet_networks']['kusama']


    # Report analytic
    report_analytic(network, wallet_address, display_name)

    return {'wallet_profile': {
        'wallet_profile': {'display_name': display_name, 'legal_name': legal_name, 'account_index': account_index,
                           'role': role,
                           'email': email, 'twitter': twitter, 'website': website, 'riot': riot, 'identity': identity,
                           'judgements': judgements, 'sub': sub,
                           'kusama_address': kusama_address, 'polkadot_address': polkadot_address},

        'balances': {'total_balance': total_balance, 'total_balance_dollars': total_balance_dollars,
                     'transferable_balance': transferable_balance,
                     'transferable_balance_dollars': transferable_balance_dollars, 'locked_balance': locked_balance,
                     'locked_balance_dollars': locked_balance_dollars,
                     'reserved_balance': reserved_balance, 'reserved_balance_dollars': reserved_balance_dollars}}}, \
           {'diamond_handed_coins': diamond_handed_coins}


