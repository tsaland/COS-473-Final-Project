from sklearn.preprocessing import MinMaxScaler
import numpy as np

def data_processing() -> tuple:
    print('starting data processing...')
    scaler = MinMaxScaler()
    # read eth price
    inFile = '/mnt/c/Users/bofan/on-chain-defi-analytics/LSTM/all_data/y_ethprice.csv'
    y_price_change = []
    eth_price = []
    with open(inFile) as f:
        for row in f:
            if row.split(',')[2]: 
                prev_price = np.float32(row.split(',')[2])
                today_price = np.float32(row.split(',')[1])
                percent_change = (today_price - prev_price) / prev_price
                y_price_change.append(percent_change)
                eth_price.append(today_price)

    print("first eth price % change is", y_price_change[0])
    y_price_change = np.array(y_price_change).reshape(365, 1)

    # read cex flow
    inFile = '/mnt/c/Users/bofan/on-chain-defi-analytics/LSTM/all_data/MWUA_cexflow.csv'
    x_cexflow = []
    with open(inFile) as f:
        for row in f:
            if row.split(',')[1]:
                net_cexflow = row.split(',')[1]
            x_cexflow.append(np.float32(net_cexflow))

    print("first cex flow is", x_cexflow[0])
    x_cexflow = scaler.fit_transform(np.array(x_cexflow).reshape(365, 1))

    # read eth balance
    inFile = '/mnt/c/Users/bofan/on-chain-defi-analytics/LSTM/all_data/MWUA_balance.csv'
    x_balance = []
    with open(inFile) as f:
        for row in f:
            if row.split(',')[0]:
                prev_balance = np.float32(row.split(',')[2])
                today_balance = np.float32(row.split(',')[1])
                percent_change = (today_balance - prev_balance) / prev_balance
                x_balance.append(np.float32(percent_change))

    print("first balance % change is", x_balance[0])
    x_balance = np.array(x_balance).reshape(365, 1)

    # read eth to stables ratio
    inFile = '/mnt/c/Users/bofan/on-chain-defi-analytics/LSTM/all_data/MWUA_eth2stable.csv'
    x_eth2stables = []
    with open(inFile) as f:
        for row in f:
            if row.split(',')[0]:
                eth_to_stables = row.split(',')[1]
                x_eth2stables.append(np.float32(eth_to_stables))

    print("first eth2stable is", x_eth2stables[0])
    x_eth2stables = scaler.fit_transform(np.array(x_eth2stables).reshape(365, 1))

    # read dex eth trading volume
    inFile = '/mnt/c/Users/bofan/on-chain-defi-analytics/LSTM/all_data/x_ethdexvolume.csv'
    x_dexvolume = []
    with open(inFile) as f:
        for row in f:
            if row.split(',')[2]:
                prev_volume = np.float32(row.split(',')[2])
                today_volume = np.float32(row.split(',')[1])
                percent_change = (today_volume - prev_volume) / prev_volume
                x_dexvolume.append(np.float32(percent_change))

    print("first dex volume % change is", x_dexvolume[0])
    x_dexvolume = np.array(x_dexvolume).reshape(365, 1)

    # read aave V2 weth stable interest rate 
    inFile = '/mnt/c/Users/bofan/on-chain-defi-analytics/LSTM/all_data/x_aavestableir.csv'
    x_interest_rate = []
    with open(inFile) as f:
        for row in f:
            ir = row.split(',')[1]
            if ir: x_interest_rate.append(np.float32(ir))

    print("first interest rate is", x_interest_rate[0])
    x_interest_rate = scaler.fit_transform(np.array(x_interest_rate).reshape(365, 1))

    # aggregate all inputs into a single numpy array
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
    return x_input, y_price_change, eth_price
