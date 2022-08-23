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
################################################################################################################################################################################



def API_key_check(api_key):
    pass




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

# Transfer data #############################################################################################################################################################

# Unique wallets #############################################################################################################################################################











# RUN SERVER ##############################################################################################################################################################
if __name__ == '__main__':
    app.run(port=7777)


