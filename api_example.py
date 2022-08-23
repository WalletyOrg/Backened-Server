import pprint
import requests
import json
# API Examples

# Server test
API_URL = 'https://api.wallety.org/?api_key=1234'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Chain state
API_URL = 'https://api.wallety.org/chain_state?api_key=1234&&network=polkadot&&currency=dollar'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# On chain identity
API_URL = 'https://api.wallety.org/on-chain-identity?api_key=1234&&network=kusama&&wallet_address=J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Balances
API_URL = 'https://api.wallety.org/balances?api_key=1234&&network=kusama&&wallet_address=J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Paper handed
API_URL = 'https://api.wallety.org/paper-handed?api_key=1234&&network=kusama&&wallet_address=J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Diamond handed
API_URL = 'https://api.wallety.org/diamond-handed?api_key=1234&&network=kusama&&wallet_address=J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Other address formats
API_URL = 'https://api.wallety.org/other-address-formats?api_key=1234&&wallet_address=J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Transfers
API_URL = 'https://api.wallety.org/transfers?api_key=1234&&network=kusama&&wallet_address=J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Monthly transfer data
API_URL = 'https://api.wallety.org/monthly-transfers?api_key=1234&&network=kusama&&wallet_address=J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Total transfer data
API_URL = 'https://api.wallety.org/total-transfers?api_key=1234&&network=kusama&&wallet_address=J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)

# Custom transfer data
API_URL = 'https://api.wallety.org/custom-transfers?api_key=1234&&network=kusama&&wallet_address=J6hXKFgZRQRc9Go8gvAwTMAima3Xqwqznz14cfsJ81hWpV3&&from=2021-07-30&&to=2022-07-30'
API_URL = requests.get(API_URL).text
API_URL = json.loads(API_URL)
pprint.pp(API_URL)
print('-' * 100)










