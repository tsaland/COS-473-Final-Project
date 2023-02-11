from web3 import Web3
from eth_balance import collect_ethbalance
from net_exchange_flow import get_cexflow
from eth_to_stablecoin import collect_eth2stable
from lending_rates import collect_lending_rates

def read_exchange_wallets():
    # inFile = '/mnt/c/Users/bofan/on-chain-defi-analytics/signal_detection/exchange_addresses.csv' for linux
    inFile = 'C:\\Users\\bofan\on-chain-defi-analytics\signal_detection\exchange_addresses.csv'
    exchange_wallets = []
    with open(inFile) as f:
        for row in f:
            if row.split(',')[0]:
                exchange = row.split(',')[0]
                exchange_wallets.append(exchange)
    return exchange_wallets

def read_selected_addresses():
    # inFile = '/mnt/c/Users/bofan/on-chain-defi-analytics/signal_detection/selected_addresses.csv' for linux
    inFile = 'C:\\Users\\bofan\on-chain-defi-analytics\signal_detection\selected_addresses.csv'
    selected_addresses = []
    with open(inFile) as f:
        for row in f:
            if row.split(',')[0]:
                address = row.split(',')[0].lower()
                if address == 'address':
                    print('problem')
                selected_addresses.append(address)

    return selected_addresses

if __name__ == "__main__":
    exchange_wallets = read_exchange_wallets()
    selected_addresses = read_selected_addresses()

    alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/OPutfOp_VyXojpS6t3xDlHiUnWCX8D1e"
    w3 = Web3(Web3.HTTPProvider(alchemy_url))
    print(w3.isConnected())

    # eth_balance = collect_ethbalance(selected_addresses, w3) # a dictionary mapping from date ("%Y/%m/%d") to eth balance
    # net_cexflow = get_cexflow(exchange_wallets, selected_addresses, w3) # a dictionary mapping from date ("%Y/%m/%d") to net cex flow
    # ethtostables = collect_eth2stable(selected_addresses, w3) # a dictionary mapping from date ("%Y/%m/%d") to eth to stable ratio
    lending_rates = collect_lending_rates() # a dictionary mapping from date ("%Y/%m/%d") to lending rates

    # put them into database
    
