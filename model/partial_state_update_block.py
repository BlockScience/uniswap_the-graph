from .parts.uniswap_model import *

PSUBs = [
    {
        'policies': {
            'user_action': p_actionDecoder
        },
        'variables': {
            'RAI_balance': s_mechanismHub_RAI,
            'ETH_balance': s_mechanismHub_ETH,
            'price_ratio': s_price_ratio
        }
    }

]
