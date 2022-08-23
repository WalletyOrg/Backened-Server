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


# on-chain identity ###############################################################################################################################################################################

from kusama import wallet_check






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
    return Response(dumps({'wallety_org_server_status': 200}), mimetype='text/json')

# On chain identity #####################################################################################################################################################
@app.route('/walletcheck/', methods=['GET'])
def wallet_check_page():
    try:
        wallet_address = str(request.args.get('wallet_address'))
        specified_network = str(request.args.get('specified_network'))

        json_dump = json.dumps(wallet_check(wallet_address, specified_network))
        return json_dump
    except:
        return {'wallety_org_wallet_check_server_status': 500, 'response': 'internal server error, please try again later'}


# RUN SERVER ##############################################################################################################################################################
if __name__ == '__main__':
    app.run(port=7777)


