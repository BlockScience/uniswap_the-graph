from .policy_aux import *
from .suf_aux import *

# Policy

def p_actionDecoder(_params, substep, sH, s):


    """
    uniswap events is a pd.DataFrame

    Mapping to Uniswap-V2
    1. No transfer events
    2. Mint = Positive mint
    3. Burn = Negative mint
    4. Swap = tokenPurchase or ethPurchase

    event = {'tokenPurchase', 'ethPurchase',
             'mint', 'Transfer'}
    Columns:
        events (event)
        eth_balance (numeric)
        eth_delta (numeric)
        token_balance (numeric)
        token_delta (numeric)
        uni_delta (numeric)
        UNI_supply (numeric)

    """
    uniswap_events = _params['uniswap_events']
    
    prev_timestep = s['timestep']
    if substep > 1:
        prev_timestep -= 1
        
    #skip the first two events, as they are already accounted for in the initial conditions of the system
    t = prev_timestep + 2 
    
    action = {
        'eth_sold': 0,
        'tokens_sold': 0,
        'eth_deposit': 0,
        'UNI_burn': 0, 
        'UNI_pct': 0,
        'fee': 0,
        'conv_tol': 0,
        'price_ratio': 0
    }

    #Event variables
    event = uniswap_events.iloc[t]['event']
    action['action_id'] = event

    if event in ['tokenPurchase', 'ethPurchase']:
        I_t, O_t, I_t1, O_t1, delta_I, delta_O, action_key = get_parameters(uniswap_events, event, s, t)
        if _params['retail_precision'] == -1:
            action[action_key] = delta_I
        elif classifier(delta_I, delta_O, _params['retail_precision']) == "Conv":            #Convenience trader case
            calculated_delta_O = int(get_output_amount(delta_I, I_t, O_t, _params))
            if calculated_delta_O >= delta_O * (1-_params['retail_tolerance']):
                action[action_key] = delta_I
            else:
                action[action_key] = 0
            action['price_ratio'] =  delta_O / calculated_delta_O
        else:            #Arbitrary trader case
            P = I_t1 / O_t1
            actual_P = I_t / O_t
            if(actual_P > P):
                I_t, O_t, I_t1, O_t1, delta_I, delta_O, action_key = get_parameters(uniswap_events, reverse_event(event), s, t)
                P = I_t1 / O_t1
                actual_P = I_t / O_t
                delta_I = get_delta_I(P, I_t, O_t, _params)
                delta_O = get_output_amount(delta_I, I_t, O_t, _params)
                if(unprofitable_transaction(I_t, O_t, delta_I, delta_O, action_key, _params)):
                    delta_I = 0
                action[action_key] = delta_I
            else:
                delta_I = get_delta_I(P, I_t, O_t, _params)
                delta_O = get_output_amount(delta_I, I_t, O_t, _params)
                if(unprofitable_transaction(I_t, O_t, delta_I, delta_O, action_key, _params)):
                    delta_I = 0
                action[action_key] = delta_I
    elif (event == 'mint') | (event == 'burn'):
        delta_I = uniswap_events['eth_delta'][t]
        action['eth_deposit'] = delta_I
    elif event == 'Transfer':
        UNI_delta = uniswap_events['uni_delta'][t]
        UNI_supply = uniswap_events['UNI_supply'][t-1]
        if UNI_delta < 0:
            action['UNI_burn'] = -UNI_delta
            action['UNI_pct'] = -UNI_delta / UNI_supply
    del uniswap_events
    return action

def profitable(P, delta_I, delta_O, action_key, _params):
    gross_profit = (delta_O*P) - delta_I
    if(action_key == 'token'):
        convert_to_ETH = gross_profit/P
        is_profitable = (convert_to_ETH > _params['fix_cost'])
    else:
        is_profitable = (gross_profit > _params['fix_cost'])


# SUFs

def s_mechanismHub_RAI(_params, substep, sH, s, _input):
    action = _input['action_id']
    if action == 'tokenPurchase':
        return ethToToken_RAI(_params, substep, sH, s, _input)
    elif action == 'ethPurchase':
        return tokenToEth_RAI(_params, substep, sH, s, _input)
    elif action == 'mint':
        return mint_RAI(_params, substep, sH, s, _input)
    elif action == 'Transfer':
        return removeLiquidity_RAI(_params, substep, sH, s, _input)
    return('RAI_balance', s['RAI_balance'])
    
def s_mechanismHub_ETH(_params, substep, sH, s, _input):
    action = _input['action_id']
    if action == 'tokenPurchase':
        return ethToToken_ETH(_params, substep, sH, s, _input)
    elif action == 'ethPurchase':
        return tokenToEth_ETH(_params, substep, sH, s, _input)
    elif action == 'mint':
        return mint_ETH(_params, substep, sH, s, _input)
    elif action == 'Transfer':
        return removeLiquidity_ETH(_params, substep, sH, s, _input)
    return('ETH_balance', s['ETH_balance'])

def s_mechanismHub_UNI(_params, substep, sH, s, _input):
    action = _input['action_id']
    if action == 'mint':
        return mint_UNI(_params, substep, sH, s, _input)
    elif action == 'burn':
        return removeLiquidity_UNI(_params, substep, sH, s, _input)
    return('UNI_supply', s['UNI_supply'])

def s_price_ratio(_params, substep, sH, s, _input):
    return('price_ratio',_input['price_ratio'])