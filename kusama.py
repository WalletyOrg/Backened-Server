################################################################################################################################################################################
import requests
import json
import decimal
from keys import *
from universal_functions import current_dates
# random functions###############################################################################################################################################################################


# kusama price
def kusamaPrice():
    kusama_price_req = requests.get('https://api.coingecko.com/api/v3/coins/kusama').text
    kusama_price_req = json.loads(kusama_price_req)
    kusama_price_req = kusama_price_req['market_data']['current_price']['usd']
    return kusama_price_req

kusama_price = decimal.Decimal(kusamaPrice())


# monthly stats###############################################################################################################################################################################
from monthly_stats import monthlyStats

# paper hand diamond hand###############################################################################################################################################################################
from paper_diamond_handed import paper_diamond_handed

# raw transfers###############################################################################################################################################################################
from raw_transfers import rawTransfers

# unique accounts###############################################################################################################################################################################
from unique_wallets import uniqueWallets

# wallet profile###############################################################################################################################################################################
from wallet_profile import wallet_profile

# transfers###############################################################################################################################################################################
from transfers import getTransfers

# custom transfers ###############################################################################################################################################################################
from custom_transfers import customTransfers

# custom unique wallets ###############################################################################################################################################################################
from custom_unique_wallets import customUniqueWallets

# general###############################################################################################################################################################################
from chain_state import chainState

# user feed ###############################################################################################################################################################################
from user_feed import joinForm, suggestion, apiApply

# wallet check###############################################################################################################################################################################
from universal_functions import walletCheck





# data ###############################################################################################################################################################################
def kusama_data(kusama_wallet_address, kusama_wallet_profile, current_dates, kusama_paper_diamond_handed,
                kusama_raw_transfers, general_kusama):

    current_dates = current_dates()
    general_kusama = general_kusama()
    kusama_wallet_profile = kusama_wallet_profile(kusama_wallet_address, 'kusama')
    kusama_transfers_data = getTransfers(kusama_wallet_address, 'kusama')
    kusama_monthly_transfers = monthlyStats(kusama_transfers_data[1], kusama_wallet_address)
    kusama_paper_diamond_handed = kusama_paper_diamond_handed(kusama_transfers_data[2], kusama_wallet_profile[1])

    kusama_top_deposit_withdraws = uniqueWallets(kusama_wallet_address,
                                                 kusama_transfers_data[1]['all_transfers'],
                                                 kusama_transfers_data[3]['all_deposits'],
                                                 kusama_transfers_data[2]['all_withdraws'],
                                                 kusama_monthly_transfers[2]['monthly_deposits'],
                                                 kusama_monthly_transfers[1]['monthly_withdraws'],
                                                 kusama_monthly_transfers[3]['monthly_transfers'])

    kusama_raw_transfers = kusama_raw_transfers(kusama_transfers_data[3], kusama_transfers_data[2])
    data = {'wallety_org_kusama_server_status': 200,
            'kusama_wallet_address': kusama_wallet_address,
            'wallet_profile': kusama_wallet_profile[0],
            'kusama_transfers_data': kusama_transfers_data[0],
            'kusama_monthly_transfers': kusama_monthly_transfers[0],
            'paper_diamond_handed': kusama_paper_diamond_handed,
            'current_dates': current_dates,
            'kusama_top_deposit_withdraws': kusama_top_deposit_withdraws,
            'rawTransfers': kusama_raw_transfers,
            'chainState': general_kusama}

    return data



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
        return Response(dumps({'wallety_org_server_status': 200}), mimetype='text/json')
    except:
        return Response(dumps({'wallety_org_server_status': 400}), mimetype='text/json')
# Wallet check #####################################################################################################################################################
@app.route('/walletcheck/', methods=['GET'])
def wallet_check_page():
    try:
        wallet_address = str(request.args.get('wallet_address'))
        specified_network = str(request.args.get('specified_network'))
        json_dump = json.dumps(walletCheck(wallet_address, specified_network))
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
        joinForm(form_name, form_role, form_email, form_project, form_website, form_net, form_comments)
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
@app.route('/apiApply/', methods=['GET'])
def apiApply():
    try:
        name = str(request.args.get('name'))
        email = str(request.args.get('email'))
        comments = str(request.args.get('comments'))
        apiApply(name, email, comments)
        return {'wallety_org_api_apply_server_status': 200, 'response': True}
    except:
        return {'wallety_org_api_apply_server_status': 500, 'response': 'internal server error, please try again later'}
# KUSAMA ###############################################################################################################################################################
# kusama data ##########################################################################################################################################################
@app.route('/kusama/', methods=['GET']) # http://127.0.0.1:7777/kusama/?wallet_address=
def kusama_request_page():
    try:
        wallet_address = str(request.args.get('wallet_address'))
        json_data = json.dumps(kusama_data(wallet_address, wallet_profile, current_dates, paper_diamond_handed, rawTransfers, chainState))
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
        all_transfers_custom = getTransfers(wallet_address, 'kusama')[1]
        custom_data = customTransfers(all_transfers_custom, wallet_address, custom_to, custom_from)
        custom_top_accounts = customUniqueWallets(wallet_address, custom_data[2], custom_data[1], custom_data[3])
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
        json_dump = json.dumps(chainState())
        return json_dump
    except:
        return {'wallety_org_kusama_general_server_status': 500, 'response': 'internal server error, please try again later'}
# Server test message ##########################################################################################################################################################
@app.route('/test/', methods=['GET'])
def test():
    return '1234', 200
# RUN SERVER ##############################################################################################################################################################
if __name__ == '__main__':
    app.run(port=7777)


