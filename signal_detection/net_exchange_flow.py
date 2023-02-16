#@title Signal#1 Net Exchange Flow; #Whale Transfer In/Out
# find these wallets interactions with the exchanges
import requests
import certifi
import matplotlib.pyplot as plt
import statistics
import datetime
from datetime import date, timedelta
import pytz
import pandas as pd
from convert_date_to_blockNumer import convert_date_to_blockNumber
from web3 import Web3

def collect_cexflow_by_address(address, startblock, endblock, net_cexflow, exchange_wallets):
  url = "https://api.etherscan.io/api?module=account&action=txlist&address=" + address + "&startblock=" + str(startblock) + "&endblock=" + str(endblock) + "&page=1&sort=desc&apikey=XI4QMN6T6P3RB5WZT6ZH5EUDKM3QJQ7DPQ"

  response = requests.get(url, verify=certifi.where())
  print(response)
  address_content = response.json()
  result = address_content.get('result')

  new_endblock = 0
  prev_date_in = date(2000, 1, 1).strftime("%Y/%m/%d") # create a dummy date string for the previous date of transferring to an exchange
  prev_date_out = date(2000, 1, 1).strftime("%Y/%m/%d") # create a dummy date string for the previous date of transferring out of an exchange
#   print('status is: ' + str(address_content.get('status')))

  if int(startblock) > int(endblock):
    print("startblock endblock error")
    return (0,0)

  while address_content.get('status') != '1':
    print('Retrying, status is: ' + str(address_content.get('status')))
    response = requests.get(url, verify=certifi.where())
    address_content = response.json()
    result = address_content.get('result')
  
  if len(result) == 0:
    return (0,0)

  for n, transaction in enumerate(result):
    tx_from = transaction.get('from').lower()
    tx_to = transaction.get('to').lower()
    eth_value = float(transaction.get('value'))/1000000000000000000.0
    hash = transaction.get('hash')
    timestamp = transaction.get('timeStamp')
    tx_date = datetime.datetime.fromtimestamp(int(timestamp), tz=pytz.utc).strftime("%Y/%m/%d")
    if tx_from in exchange_wallets:
      net_cexflow[tx_date][0] -= eth_value # exchange outflow
      if tx_date != prev_date_out: # only increment "from exchange" whale count once for this address on one day
        net_cexflow[tx_date][1] -= 1
      # print("found a outflow! tx hash: ", hash, "tx date is ", tx_date, "prev date out is", prev_date_out, "does tx date = prev date out?", tx_date == prev_date_out)
      prev_date_out = tx_date
    if tx_to in exchange_wallets:
      net_cexflow[tx_date][0] += eth_value # exchange inflow
      if tx_date != prev_date_in: # only increment "to exchange" whale count once for this address on one day
        net_cexflow[tx_date][2] += 1
      # print("found a inflow! tx hash: ", hash, "tx date is ", tx_date, "prev date in is", prev_date_in, "does tx date = prev date in?", tx_date == prev_date_in)
      prev_date_in = tx_date # update the previous date
    if n == 9999:
      new_endblock = transaction.get('blockNumber')
  return(n, new_endblock)

def get_cexflow(exchange_wallets, selected_addresses, w3):
    start_date = date(2018, 1, 1)
    end_date = date(2023, 1, 1)
    start_block = convert_date_to_blockNumber(start_date, w3)
    end_block = convert_date_to_blockNumber(end_date+timedelta(days=1), w3) # starts from the first block in 2022 and ends in the first block in 2023

    net_cexflow = dict() # hashmap records net exchange inflow and outflows
    daterange = pd.date_range(start_date, end_date)
    for single_date in daterange:
        net_cexflow[single_date.strftime("%Y/%m/%d")] = [0,0,0] # mapping from date to [net flow, #whales transfering out of exchanges, #whales transfering to exchanges]
    
    # selected_addresses = ['0xB8001C3eC9AA1985f6c747E25c28324E4A361ec1', '0xD7efCbB86eFdD9E8dE014dafA5944AaE36E817e4', '0x6081258689a75d253d87cE902A8de3887239Fe80', '0xCD531Ae9EFCCE479654c4926dec5F6209531Ca7b', '0x4f6742bADB049791CD9A37ea913f2BAC38d01279']
    for address in selected_addresses:
        record_executed, new_endblock = collect_cexflow_by_address(address, start_block, end_block, net_cexflow, exchange_wallets)
        round = 0
        while record_executed == 9999:
            record_executed, new_endblock = collect_cexflow_by_address(address, start_block, new_endblock, net_cexflow, exchange_wallets)
            round += 1
        print('finished this address:', address, "with round", round)

    print(net_cexflow)
    

    dates = list(net_cexflow.keys())
    net_flow = []
    whales_outof_exchanges = []
    whales_into_exchanges = []
    net_inflow_excludezero = []
    for value in net_cexflow.values():
        net_flow.append(value[0])
        if value[0] != 0:
            net_inflow_excludezero.append(value[0])
        whales_outof_exchanges.append(value[1])
        whales_into_exchanges.append(value[2])

    median = statistics.median(net_inflow_excludezero)
    mean = statistics.mean(net_inflow_excludezero)
    print('median of the net exchange flow is', median)
    print('mean of the net exchange flow is', mean)
    print(net_flow)


    # visualize net flow into the exchanges
    dates = list(net_cexflow.keys())
    dates = [e[5:] for e in dates]
    print(dates)
    plt.figure(figsize=(15, 8))
    plt.bar(range(len(net_cexflow)), net_flow, width=1.0)
    plt.xticks(rotation=70)
    plt.xticks(range(0, len(dates), 30))
    plt.xticks(range(0, len(dates), 30), dates[0::30])
    plt.grid(True)

    plt.xlabel('Dates')
    plt.ylabel('Exchange Net Flow (in Ether)')
    plt.title('Whales Exchange Flow', loc='left')
    plt.show()

    # find number of whales transferring out of and into exchanges
    plt.figure(figsize=(15, 8))
    plt.bar(dates, whales_into_exchanges, color = '#337AE3', width=1.0)
    plt.bar(dates, whales_outof_exchanges, color = '#DB4444', width=1.0)
    plt.xticks(rotation=70)
    plt.xticks(range(0, len(dates), 30))
    plt.xticks(range(0, len(dates), 30), dates[0::30])
    plt.grid(True)
    legend_label = ['#Whales Transfering into Exchanges', '#Whales Transfering out of Exchanges']
    plt.legend(legend_label, ncol = 2, bbox_to_anchor=([1, 1.05, 0, 0]), frameon = False)
    plt.title('Number of whales flowing into and out of exchanges ', loc='left')
    plt.show()

    return net_cexflow
