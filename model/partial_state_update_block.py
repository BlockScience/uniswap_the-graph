from .parts.uniswap_model import *

PSUBs = [
    {
        'policies': {
            'user_action': p_actionDecoder
        },
        'variables': {
            'DAI_balance': s_mechanismHub_DAI,
            'ETH_balance': s_mechanismHub_ETH,
            'price_ratio': s_price_ratio
        }
    }

]
