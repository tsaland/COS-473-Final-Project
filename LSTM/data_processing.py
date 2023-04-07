import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def remove_nans_and_zeros(data):
    data = data[~np.isnan(data).any(axis=1)]
    data = data[data[:, 1] != 0.0]
    return data

def read_data_file(filename):
    path = os.path.join('data', filename)
    data = np.genfromtxt(path, delimiter=',', usecols=(1,), dtype=np.float32)
    data = remove_nans_and_zeros(data)
    return data

def combine_input_data(*arrays):
    return np.concatenate([a.reshape(-1, 1) for a in arrays], axis=1)

def data_processing() -> tuple:
    print('starting data processing...')
    scaler = MinMaxScaler()

    # read eth price
    eth_price_data = read_data_file('y_ethprice.csv')
    prev_price = eth_price_data[:, 1]
    today_price = eth_price_data[:, 0]
    y_price_change = (today_price - prev_price) / prev_price
    eth_price = today_price

    print("first eth price % change is", y_price_change[0])
    y_price_change = y_price_change.reshape(-1, 1)

    # read cex flow
    x_cexflow = read_data_file('MWUA_cexflow.csv')
    print("first cex flow is", x_cexflow[0])
    x_cexflow = scaler.fit_transform(x_cexflow.reshape(-1, 1))

    # read eth balance
    balance_data = read_data_file('MWUA_balance.csv')
    prev_balance = balance_data[:, 1]
    today_balance = balance_data[:, 0]
    x_balance = (today_balance - prev_balance) / prev_balance
    print("first balance % change is", x_balance[0])
    x_balance = x_balance.reshape(-1, 1)

    # read eth to stables ratio
    x_eth2stables = read_data_file('MWUA_eth2stable.csv')
    print("first eth2stable is", x_eth2stables[0])
    x_eth2stables = scaler.fit_transform(x_eth2stables.reshape(-1, 1))

    # read dex eth trading volume
    volume_data = read_data_file('x_ethdexvolume.csv')
    prev_volume = volume_data[:, 1]
    today_volume = volume_data[:, 0]
    x_dexvolume = (today_volume - prev_volume) / prev_volume
    print("first dex volume % change is", x_dexvolume[0])
    x_dexvolume = x_dexvolume.reshape(-1, 1)

    # read aave V2 weth stable interest rate
    x_interest_rate = read_data_file('MWUA_interestrate.csv')

    print("first interest rate is", x_interest_rate[0])

    x_interest_rate = scaler.fit_transform(x_interest_rate.reshape(-1, 1))

    x_input = combine_input_data(x_cexflow, x_balance, x_eth2stables, x_dexvolume, x_interest_rate)

    return x_input, y_price_change, eth_price
