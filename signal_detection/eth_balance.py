# track whales' eth balance

#@title Signal#2 Whales Balance
from datetime import timedelta, date
import pandas as pd
import pytz
import statistics 
from convert_date_to_blockNumer import convert_date_to_blockNumber
from web3 import Web3
import matplotlib.pyplot as plt

def collect_ethbalance(selected_addresses, w3):
    whales_individual_balance = dict()
    whales_total_balance = dict()
    startdate_ = date(2018, 1, 1)
    enddate_ = date(2023, 1, 1)
    range = pd.date_range(startdate_, enddate_)
    for address in selected_addresses:
        whales_individual_balance[address] = dict()
        for _date in range:
            date_string = _date.date().strftime("%Y/%m/%d")
            whales_individual_balance[address][date_string] = 0
    for _date in range:
        date_string = _date.date().strftime("%Y/%m/%d")
        whales_total_balance[date_string] = 0

    for _date in range:
        block = convert_date_to_blockNumber(_date.date(), w3)
        date_string = _date.date().strftime("%Y/%m/%d")
        for address in selected_addresses:
            checksum = Web3.toChecksumAddress(address)
            balance = float(w3.fromWei(w3.eth.get_balance(checksum, block_identifier=block), 'ether'))
            whales_individual_balance[address][date_string] = balance
            whales_total_balance[date_string] += balance
        print("finished date", _date.date())
        if _date.date() == date(2019, 1, 1):
            print("2018 whales individual balance", whales_individual_balance)  # for MWUA test
            print("2018 whales total balance", whales_total_balance) # for trend analysis
        elif _date.date() == date(2020, 1, 1):
            print("2018-2019 whales individual balance", whales_individual_balance)
            print("2018-2019 whales total balance", whales_total_balance)
        elif _date.date() == date(2021, 1, 1):
            print("2018-2020 whales individual balance", whales_individual_balance)
            print("2018-2020 whales total balance", whales_total_balance)
    print("whales individual balance", whales_individual_balance)  # for MWUA test
    print("whales total balance", whales_total_balance) # for trend analysis
    print("median is", statistics.median(whales_total_balance.values()))
    print("mean is", statistics.mean(whales_total_balance.values()))

    dates = list(whales_total_balance.keys())
    plt.figure(figsize=(15, 8))
    plt.bar(range(len(whales_total_balance)), whales_total_balance.values(), width=1.0)
    plt.xticks(rotation=70)
    plt.xticks(range(0, len(dates), 30))
    plt.xticks(range(0, len(dates), 30), dates[0::30])
    plt.grid(True)

    plt.xlabel('Dates')
    plt.ylabel('Ether Balance')
    plt.title('Whales Total ETH Balnace', loc='left')
    plt.show()

    return whales_total_balance, whales_individual_balance
