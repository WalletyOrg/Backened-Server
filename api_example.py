import pprint
import requests
import json
# API Examples

# local or server test
local = 'http://127.0.0.1:7777/'
main_server = 'https://api.wallety.org/'
# def pref
URL = local
wallet_address = 'J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3'
network = 'kusama'
currency = 'dollar'
api_key = '1234'


# Server test
API_URL = f'{URL}?api_key={api_key}'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Chain state
API_URL = f'{URL}chain-state?api_key={api_key}&&network={network}&&currency={currency}'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# On chain identity
API_URL = f'{URL}on-chain-identity?api_key={api_key}&&network={network}&&wallet_address={wallet_address}'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Balances
API_URL = f'{URL}balances?api_key={api_key}&&network={network}&&wallet_address={wallet_address}&&currency={currency}'
# try dollar too
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Paper diamond handed
API_URL = f'{URL}paper-diamond-handed?api_key={api_key}&&network={network}&&wallet_address={wallet_address}&&currency={currency}'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Other address formats
API_URL = f'{URL}other-address-formats?api_key={api_key}&&wallet_address={wallet_address}'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Transfers
API_URL = f'{URL}transfers?api_key={api_key}&&network={network}&&wallet_address={wallet_address}&&currency={currency}'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
print(API_URL)
print('-' * 100)

# Unique wallets
API_URL = f'{URL}unique-wallets?api_key={api_key}&&network={currency}&&wallet_address={wallet_address}&&currency={currency}'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
print(API_URL)
print('-' * 100)








