import numpy as np
from sklearn.preprocessing import MinMaxScaler

def data_processing() -> tuple:
    print('starting data processing...')
    scaler = MinMaxScaler()
    # read eth price
    URL = r'C:\\Users\\tucke\\OneDrive\\Documents\\on-chain-defi-analytics\\LSTM\\all_data\\'
    inFile = URL + 'y_ethprice.csv'
    
    data = np.genfromtxt(inFile, delimiter=',',
                         usecols=(1, 2), dtype=np.float32)
    
    data = data[~np.isnan(data).any(axis=1)]
    data = data[data[:, 1] != 0.0]

    prev_price = data[:, 1]
    today_price = data[:, 0]
    mask = prev_price != 0.0

    y_price_change = (today_price[mask] - prev_price[mask]) / prev_price[mask]
    eth_price = today_price[mask]

    print("first eth price % change is", y_price_change[0])
    y_price_change = y_price_change.reshape(-1, 1)

    # read cex flow
    inFile = URL + 'MWUA_cexflow.csv'
    x_cexflow = np.genfromtxt(inFile, delimiter=',', usecols=(1), dtype=np.float32)
    x_cexflow = x_cexflow[~np.isnan(x_cexflow)]


    print("first cex flow is", x_cexflow[0])
    x_cexflow = scaler.fit_transform(x_cexflow.reshape(-1, 1))

    # read eth balance
    inFile = URL + 'MWUA_balance.csv'
    data = np.genfromtxt(inFile, delimiter=',',usecols=(1, 2), dtype=np.float32)
    data = data[~np.isnan(data).any(axis=1)]
    data = data[data[:, 1] != 0.0]

    prev_balance = data[:, 1]
    today_balance = data[:, 0]
    mask = prev_balance != 0.0

    x_balance = (today_balance[mask] - prev_balance[mask]) / prev_balance[mask]
    x_balance = x_balance.reshape(-1, 1)

    print("first balance % change is", x_balance[0])
    x_balance = np.array(x_balance).reshape(-1, 1)

    # read eth to stables ratio
    inFile = URL + 'MWUA_eth2stable.csv'
    x_eth2stables = np.genfromtxt(inFile, delimiter=',', usecols=(1), dtype=np.float32)
    x_eth2stables = x_eth2stables[~np.isnan(x_eth2stables)]

    print("first eth2stable is", x_eth2stables[0])
    x_eth2stables = scaler.fit_transform(x_eth2stables.reshape(-1, 1))

    # read dex eth trading volume
    inFile = URL + 'x_ethdexvolume.csv'
    data = np.genfromtxt(inFile, delimiter=',', usecols=(1, 2), dtype=np.float32)
    data = data[~np.isnan(data).any(axis=1)]
    data = data[data[:, 1] != 0.0]

    prev_volume = data[:, 1]
    today_volume = data[:, 0]
    mask = prev_volume != 0.0

    x_dexvolume = (today_volume[mask] - prev_volume[mask]) / prev_volume[mask]
    x_dexvolume = x_dexvolume.reshape(-1, 1)

    print("first dex volume % change is", x_dexvolume[0])

    # read aave V2 weth stable interest rate
    inFile = URL + 'x_aavestableir.csv'
    x_interest_rate = np.genfromtxt(inFile, delimiter=',', usecols=(1), dtype=np.float32)
    x_interest_rate = x_interest_rate[~np.isnan(x_interest_rate)]

    print("first interest rate is", x_interest_rate[0])
    x_interest_rate = scaler.fit_transform(x_interest_rate.reshape(-1, 1))

    #  aggregate all inputs into a single numpy array with length of cex flow
    x_input = []
    for row in range(len(x_cexflow)):
        input_row = []
        input_row.append(x_cexflow[row][0])
        input_row.append(x_balance[row][0])
        input_row.append(x_eth2stables[row][0])
        input_row.append(x_dexvolume[row][0])
        input_row.append(x_interest_rate[row][0])
        x_input.append(input_row)

    x_input = np.array(x_input)
    print("training input has shape", x_input.shape)
    print(x_input, y_price_change, eth_price)
    return x_input, y_price_change, eth_price
    

data_processing()


    

    