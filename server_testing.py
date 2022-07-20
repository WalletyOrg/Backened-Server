import json
RED = '\u001b[31m'
GREEN = '\u001b[32m'
RESET = '\u001b[0m'
def colour_print(text: str, *effects: str) -> None:
    effect_string = "".join(effects)
    output_string = "{0}{1}{2}".format(effect_string, text, RESET)
    print(output_string)

# kusama
def kusama_server_test(wallet_address):
    from kusama import kusama_data, kusama_wallet_profile, current_dates, kusama_paper_diamond_handed, kusama_raw_transfers, general_kusama
    try:
        json.dumps(kusama_data(wallet_address[0], kusama_wallet_profile, current_dates, kusama_paper_diamond_handed, kusama_raw_transfers, general_kusama))
        colour_print(f'{wallet_address[1]} PASS', GREEN)
    except:
        colour_print(f'{wallet_address[1]} FAILED', RED)
from keys import test_wallet_address_kusama, test_wallet_address_kusama_ni, test_wallet_address_kusama_wni, test_wallet_address_kusama_wpi
# kusama test
kusama_server_test(test_wallet_address_kusama)
# kusama ni
kusama_server_test(test_wallet_address_kusama_ni)
# kusama wni
kusama_server_test(test_wallet_address_kusama_wni)
# kusama wpi
kusama_server_test(test_wallet_address_kusama_wpi)
print('\n')
# polkadot
def polkadot_server_test(wallet_address):
    from polkadot import polkadot_data, polkadot_wallet_profile, current_dates, polkadot_paper_diamond_handed, polkadot_raw_transfers, general_polkadot
    try:
        json.dumps(polkadot_data(wallet_address[0], polkadot_wallet_profile, current_dates, polkadot_paper_diamond_handed, polkadot_raw_transfers, general_polkadot))
        colour_print(f'{wallet_address[1]} PASS', GREEN)
    except:
        colour_print(f'{wallet_address[1]} FAILED', RED)
from keys import test_wallet_address_polkadot, test_wallet_address_polkadot_ni, test_wallet_address_polkadot_wni, test_wallet_address_polkadot_wpi
# polkadot test
polkadot_server_test(test_wallet_address_polkadot)
# polkadot ni
polkadot_server_test(test_wallet_address_polkadot_ni)
# polkadot wni
polkadot_server_test(test_wallet_address_polkadot_wni)
# polkadot wpi
polkadot_server_test(test_wallet_address_polkadot_wpi)

