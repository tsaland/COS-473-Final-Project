from web3 import Web3
from eth_balance import collect_ethbalance
from net_exchange_flow import get_cexflow
from eth_to_stablecoin import collect_eth2stable
from lending_rates import collect_lending_rates
from select_whales import select_whales
import dropbox
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
    inFile = 'C:\\Users\\bofan\on-chain-defi-analytics\signal_detection\whales_addresses.csv'
    selected_addresses = []
    with open(inFile) as f:
        for row in f:
            if row.split(',')[0]:
                address = row.split(',')[0].lower()
                address = address.split('\n')[0]
                if address == 'address':
                    print('problem')
                selected_addresses.append(address)

    return selected_addresses

def connect_to_dropbox():
    token = "sl.BY62pvNVaDoxDBdNXD1SmNyqkHJhoQeBrvdRbSrSedE2UZYgjnOeUf-UyCGN08dfUjHA5nVsLnzxLYCTkLjVSTPoXYYjF9dbYN7ZZ_j7naqK4BpnH2EHyRAu7LJCxMLRoL6_HBvSJVE"
    
    try:
        dbx = dropbox.Dropbox(token)
        print('Connected to Dropbox successfully')
      
    except Exception as e:
        print(str(e))
      
    return dbx

if __name__ == "__main__":
    # selected_addresses = select_whales(w3, exchange_wallets)
    # print(selected_addresses)
    exchange_wallets = read_exchange_wallets()
    selected_addresses = read_selected_addresses()
    alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/OPutfOp_VyXojpS6t3xDlHiUnWCX8D1e"
    w3 = Web3(Web3.HTTPProvider(alchemy_url))
    print(w3.isConnected())

    # dbx = connect_to_dropbox()

    eth_balance = collect_ethbalance(selected_addresses, w3) # a dictionary mapping from date ("%Y/%m/%d") to eth balance
    # net_cexflow = get_cexflow(exchange_wallets, selected_addresses, w3) # a dictionary mapping from date ("%Y/%m/%d") to net cex flow
    # ethtostables = collect_eth2stable(selected_addresses, w3) # a dictionary mapping from date ("%Y/%m/%d") to eth to stable ratio
    # lending_rates = collect_lending_rates() # a dictionary mapping from date ("%Y/%m/%d") to lending rates

    # put them into database
    
