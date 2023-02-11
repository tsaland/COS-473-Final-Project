# track whales' eth balance

#@title Signal#2 Whales Balance
from datetime import timedelta, date
import pandas as pd
import pytz
import statistics 
from convert_date_to_blockNumer import convert_date_to_blockNumber
from web3 import Web3

def collect_ethbalance(selected_addresses, w3):
    whales_balance = dict()
    startdate_ = date(2022, 1, 1)
    enddate_ = date(2023, 1, 1)
    range = pd.date_range(startdate_, enddate_)

    for _date in range:
        block = convert_date_to_blockNumber(_date.date(), w3)
        balance = 0
        for address in selected_addresses:
            checksum = Web3.toChecksumAddress(address)
            balance += float(w3.fromWei(w3.eth.get_balance(checksum, block_identifier=block), 'ether'))
    whales_balance[_date.date().strftime("%Y/%m/%d")] = balance
    print("finished date", _date.date(), "with balance", balance)
    print(whales_balance)
    print("median is", statistics.median(whales_balance.values()))
    print("mean is", statistics.mean(whales_balance.values()))

    return whales_balance
