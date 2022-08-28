import pprint
import requests
import json
# API Examples

# local or server test
local = 'http://127.0.0.1:7777/'
server = 'https://api.wallety.org/'
# def pref
URL = local


# Server test
API_URL = f'{URL}?api_key=1234'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Chain state
API_URL = f'{URL}chain-state?api_key=1234&&network=polkadot&&currency=pound'
# try dollar too
API_URL = requests.get(API_URL).text
# API_URL = json.loads(API_URL)
# pprint.pp(API_URL)
print(API_URL)
print('-' * 100)

# On chain identity
API_URL = f'{URL}on-chain-identity?api_key=1234&&network=kusama&&wallet_address=J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Balances
API_URL = f'{URL}balances?api_key=1234&&network=kusama&&wallet_address=J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3&&currency=pound'
# try dollar too
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Paper diamond handed
API_URL = f'{URL}paper-diamond-handed?api_key=1234&&network=kusama&&wallet_address=J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3&&currency=pound'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Other address formats
API_URL = f'{URL}other-address-formats?api_key=1234&&wallet_address=J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Transfers
API_URL = f'{URL}transfers?api_key=1234&&network=kusama&&wallet_address=J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3&&currency=pound'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Unique wallets
API_URL = f'{URL}unique-wallets?api_key=1234&&network=kusama&&wallet_address=J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3&&currency=pound'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)








