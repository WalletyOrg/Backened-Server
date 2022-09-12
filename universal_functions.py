from keys import *
import requests




def report_analytic(network, wallet_address, display_name):
    try:
        from keys import kusama_test_addresss
        clean_message = f'Site hit from: {display_name}\n' \
                        f'Calling: {network}\n' \
                        f'https://wallety.org/kusama?wallet_address={wallet_address}'
        if wallet_address not in kusama_test_addresss:
            requests.get(f'https://api.telegram.org/bot{telegram_api_key}/sendMessage?chat_id={telegram_chat_id_report_clean}&text={clean_message}')
        return None
    except:
        return None
