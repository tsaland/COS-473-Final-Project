from web3 import Web3
from eth_balance import collect_ethbalance
from net_exchange_flow import get_cexflow, net_cexflow_to_csv
from eth_to_stablecoin import collect_eth2stable, balance_to_csv
from lending_rates import collect_lending_rates, lending_rate_to_csv
from select_whales import select_whales

def read_exchange_wallets():
    inFile = r'C:\\Users\\tucke\\OneDrive\\Documents\\on-chain-defi-analytics\\signal_detection\exchange_addresses.csv'
    exchange_wallets = []
    with open(inFile) as f:
        for row in f:
            if row.split(',')[0]:
                exchange = row.split(',')[0]
                exchange_wallets.append(exchange)
    return exchange_wallets

def read_selected_addresses():
    inFile = r'C:\\Users\\tucke\\OneDrive\\Documents\\on-chain-defi-analytics\\signal_detection\whales_addresses.csv'
    selected_addresses = []
    with open(inFile) as f:
        for row in f:
            address = row.strip().lower().split(',')[0]
            selected_addresses.append(address)
    return selected_addresses

if __name__ == "__main__":
    # selected_addresses = select_whales(w3, exchange_wallets)
    # print(selected_addresses)
    exchange_wallets = read_exchange_wallets()
    selected_addresses = read_selected_addresses()
    alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/OPutfOp_VyXojpS6t3xDlHiUnWCX8D1e"
    w3 = Web3(Web3.HTTPProvider(alchemy_url))
    print(w3.isConnected())

    # aggregate_balance, individual_balance = collect_ethbalance(selected_addresses, w3) # a dictionary mapping from date ("%Y/%m/%d") to eth balance
    # net_cexflow = get_cexflow(exchange_wallets, selected_addresses, w3) # a dictionary mapping from date ("%Y/%m/%d") to net cex flow
    # print(net_cexflow)
    # net_cexflow_to_csv(net_cexflow)
    # a dictionary mapping from date ("%Y/%m/%d") to eth to stable ratio
    # ETH_perent_holding, wallet_balances = collect_eth2stable(selected_addresses, w3)
    # balance_to_csv(ETH_perent_holding, wallet_balances)
    lending_rates = collect_lending_rates() # a dictionary mapping from date ("%Y/%m/%d") to lending rates
    lending_rate_to_csv(lending_rates)

    

    # put them into database
    
