from universal_functions import format_coins, format_dollars
from kusama import kusama_price


def paper_diamond_handed(all_withdrawals, diamond_handed_coins):
    # paper handed

    paper_handed_coins = 0

    for i in all_withdrawals['all_withdraws']:
        paper_handed_coins += float(i['amount'])

    # paperhanded dollar amounts and formatting numbers
    paper_handed_coins_dollars = float(kusama_price) * float(paper_handed_coins)

    # formatting numbers
    paper_handed_coins = format_coins(paper_handed_coins)
    paper_handed_coins_dollars = format_dollars(paper_handed_coins_dollars)

    # diamond handed
    diamond_handed_coins = diamond_handed_coins['diamond_handed_coins']
    diamond_handed_coins_dollars = float(kusama_price) * float(diamond_handed_coins)
    diamond_handed_coins = format_coins(diamond_handed_coins)
    diamond_handed_coins_dollars = format_dollars(diamond_handed_coins_dollars)

    return {'handed': {'paper_handed': {'paper_handed_coins': paper_handed_coins,
                                        'paper_handed_coins_dollars': paper_handed_coins_dollars},

                       'diamond_handed': {'diamond_handed_coins': diamond_handed_coins,
                                          'diamond_handed_coins_dollars': diamond_handed_coins_dollars}
                       }
            }

