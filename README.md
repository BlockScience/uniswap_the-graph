# Uniswap + The Graph Model

## List of TODOS

**Finished**
1. Compute the UNI supply on the cadCAD model
- This involves computing the initial UNI supply and also implementing logic
for calculating changes given mint / burn events 
2. Re-do the original Uniswap demo analysis in regards to Liq Providers (blocked by above)

**New Issues**
1. Get complete dataset for RAI/ETH pair so model actually makes sense
2. Figure out more efficient method to obtain data from The Graph

## Event data structure

uniswap events is a pd.DataFrame

Mapping to Uniswap-V2
1. No transfer events
2. Mint = Positive addLiquidity
3. Burn = Negative addLiquidity
4. Swap = TokenPurchase or EthPurchase

event = {'TokenPurchase', 'EthPurchase',
            'AddLiquidity', 'Transfer'}
Columns:
    events (event)
    eth_balance (numeric)
    eth_delta (numeric)
    token_balance (numeric)
    token_delta (numeric)
    uni_delta (numeric)
    UNI_supply (numeric)

## Mapping Uniswap V1 (Ethereum-ETL) to Uniswap V2 (The Graph)

uni_delta and UNI_supply is always going to be zero, and we're not going to use transfer events

Initial ETH and Token balance are retrieved through a
single data point of PairHourData.
(eth_balance, token_balance) = (reserve0, reserve1)

Afterwards, all swaps, mints and burns are collected given
that their timestamp is after this single point.

Swap = (+eth_delta, -token_delta) (TokenPurchase)
Swap = (-eth_delta, +token_delta) (EthPurchase)
Mint = (+eth_delta, +token_delta) (AddLiquidity)
Burn = (-eth_delta, -token_delta) (AddLiquidity)

### For all

(eth_balance, token_balance) += (eth_delta, token_delta)
### Mint

(eth_delta, token_delta) = (amount0, amount1)

### Burn

(eth_delta, token_delta) = (-amount0, -amount1)

### Swaps

*TokenPurchase*
(eth_delta, token_delta) = (amount0Out, -amount1In)

*EthPurchase*
(eth_delta, token_delta) = (-amount0In, amount1Out)
