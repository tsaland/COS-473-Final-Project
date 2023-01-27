import numpy as np
from datetime import date, timedelta 
import statistics 
import matplotlib.pyplot as plt
import pandas as pd
from data import selected_addresses, net_cexflow, eth_balance, eth2stable_ratio, eth_price

def MWUA():
    start_date = date(2022, 1, 1)
    end_date = date(2022, 12, 31)
    daterange = pd.date_range(start_date, end_date, freq='W').date
    weights = dict()

    # initialize the weights of all wallets as 1, wallet all initialized in lower cases due to google colab 
    for wallet in selected_addresses:
        weights[wallet] = 1
    _lambda = 0.01
    balance_lambda = 0.1 # discount balance change due to asymmetric impact

    # get average balance of a whale
    avg_balance = dict()
    for wallet in eth_balance.keys():
        balance = 0
    for value in eth_balance[wallet].values():
        balance += value
    avg_balance[wallet] = balance / 365

    # weekly performance punishment 
    for week_start in daterange:
        week_end = week_start+timedelta(weeks=1)
        try:
            # price return: (future's closing price - today's closing price) / today's closing price 
            future_price = eth_price[week_end.strftime("%m/%d/%Y")]
            today_price = eth_price[week_start.strftime("%m/%d/%Y")] 
            price_change = (future_price - today_price) / today_price
        except:
            break # disregard the last week

        # Multiplicative Weight Update Algorithm
        for wallet in selected_addresses:
            wallet_id = selected_addresses.index(wallet)
            week_cexflow = 0
            for day in pd.date_range(week_start, week_end).date:
                week_cexflow += net_cexflow[wallet_id][day.strftime("%Y/%m/%d")]

            # change weights based on net exchange flow
            if week_cexflow != 0:
                cexflow_prediction_degree = np.abs(week_cexflow) / avg_balance[wallet] * np.abs(price_change) * _lambda # prediction discounted by purchase power
            if week_cexflow < 0 and price_change < 0: # punish if buy eth before price goes down
                weights[wallet] /= 1 + cexflow_prediction_degree
            elif week_cexflow > 0 and price_change > 0: # punish if sell eth before price goes up
                weights[wallet] /= 1 + cexflow_prediction_degree
            elif week_cexflow < 0 and price_change > 0: # reward if buy eth before price goes up
                weights[wallet] *= 1 + cexflow_prediction_degree
            elif week_cexflow > 0 and price_change > 0: # reward if sell eth before price goes down
                weights[wallet] *= 1 + cexflow_prediction_degree

            # change weights based on balance changes
            start_balance = eth_balance[wallet][week_start.strftime("%Y/%m/%d")]
            end_balance = eth_balance[wallet][week_end.strftime("%Y/%m/%d")]
            if start_balance != 0:
                balance_change = (end_balance - start_balance) / start_balance
            balance_prediction_degree = np.abs(balance_change) * np.abs(price_change) * _lambda * balance_lambda # prediction discounted 
            if balance_change > 0 and price_change < 0: # punish if balance increases before price goes down
                weights[wallet] /= 1 + balance_prediction_degree
            if balance_change < 0 and price_change > 0: # punish if balance decreases before price goes up
                weights[wallet] /= 1 + balance_prediction_degree
            if balance_change > 0 and price_change > 0: # reward if balance increases before price goes up
                weights[wallet] *= 1 + balance_prediction_degree
            if balance_change < 0 and price_change < 0: # reward if balance decreases before price goes down
                weights[wallet] *= 1 + balance_prediction_degree
        
            # change weighs based on eth / (eth + stable) ratio
            start_eth2stable = eth2stable_ratio[wallet][week_start.strftime("%Y/%m/%d")]
            end_eth2stable = eth2stable_ratio[wallet][week_end.strftime("%Y/%m/%d")]
            # eth2stable_change = (end_eth2stable - start_eth2stable) / start_eth2stable
            eth2stable_change = (end_eth2stable - start_eth2stable) 

            eth2stable_prediction_degree = np.abs(eth2stable_change) * np.abs(price_change) * _lambda
            # ideally hold higher percent of eth before price goes up 
            if eth2stable_change > 0 and price_change < 0: # punish if eth2stable ratio increases before price goes down
                weights[wallet] /= 1 + eth2stable_prediction_degree
            if eth2stable_change < 0 and price_change > 0: # punish if eth2stable ratio decreases before price goes up
                weights[wallet] /= 1 + eth2stable_prediction_degree
            if eth2stable_change > 0 and price_change > 0: # reward if eth2stable ratio increases before price goes up
                weights[wallet] *= 1 + eth2stable_prediction_degree
            if eth2stable_change > 0 and price_change < 0: # reward if eth2stable ratio decreases before price goes down
                weights[wallet] *= 1 + eth2stable_prediction_degree


        weights_list = list(weights.values())
        plt.figure(figsize=(16,8))
        plt.plot(np.arange(len(weights_list)), weights_list)
        plt.xlabel('Whales Wallet Index')
        plt.ylabel('Weights')
        plt.title('Multiplicative Weight Update Simulation')
        plt.grid(True)
        plt.show()

        print('median weight is', statistics.median(weights_list))
        print("mean weight is", statistics.mean(weights_list))
        print('standard deviation is', statistics.stdev(weights_list))
        print(weights_list)

        MWUA_wallets = sorted(weights, key=weights.get, reverse=True)[:20]
        for wallet in MWUA_wallets:
            print("selected wallet is", wallet, "weight is", weights[wallet])

        print(MWUA_wallets)
        return MWUA_wallets
