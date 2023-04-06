#-----------------------------------------------------------------------
# random_speculator.py
# Author: Jackie Chen
#-----------------------------------------------------------------------

import csv
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#-----------------------------------------------------------------------

def random_speculator():
    money = 0
    eth = 0
    with open('General Models/ETH Price 2022 - open_price, close_price.csv') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            num = random.random()
            if num < 0.2:
                money -= float(row[1])
                eth += 1
            if num >= 0.8 and eth > 0:
                money += float(row[1])
                eth -= 1

    print(str(money) + " " + str(eth))
    print(money + eth*1500)



def dip_hill_speculator():
    moneyStart = 100000
    money = moneyStart
    ethspentmoney = 0
    eth = 0
    plot = []
    with open('General Models/ETH Price 2022 - open_price, close_price.csv') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            num = random.random()
            if eth == 0:
                if num < 0.4:
                    money -= float(row[1])
                    ethspentmoney -= float(row[1])
                    eth += 1
            elif ethspentmoney / eth + float(row[1]) > 0:
                # Sell probability
                percentIncrease = (ethspentmoney / eth + float(row[1]))/float(row[1])
                if percentIncrease + num*0.3 > 0.3:
                    money += eth * float(row[1])
                    eth = 0
                    ethspentmoney = 0
            elif ethspentmoney / eth + float(row[1]) <= 0:
                # Buy probablility
                percentDecrease = -(ethspentmoney / eth + float(row[1]))/float(row[1])
                percentMoniesLeft = money/moneyStart
                if percentDecrease + num*0.5 > 0.5 and money > 0:
                    if random.random() < percentMoniesLeft:
                        money -= float(row[1])
                        ethspentmoney -= float(row[1])
                        eth +=1
            plot.append(money + float(row[1]) * eth)
    plt.plot(plot)
    plt.xlabel('Days since 1/1/22')
    plt.ylabel('total cash')
    plt.title('buying dip speculator')
    print(str(money) + " " + str(eth))
    plt.show()


def momentum_speculator():
    moneyStart = 100000
    money = moneyStart
    eth = 0
    df = pd.read_csv('General Models/ETH Price 2022 - open_price, close_price.csv',
                     header=None, names=['date', 'open_price', 'close_price', 'change_price'])
    plot = []
    
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    df['three_day_returns'] = df['open_price'].pct_change(periods=3)

    df['signal'] = 0  # 0 = hold, 1 = buy, -1 = sell
    df.loc[df['three_day_returns'] > 0, 'signal'] = 1  # buy signal
    df.loc[df['three_day_returns'] < 0, 'signal'] = -1  # sell signal

    # Calculate daily eth amount and money spent
    for _, row in df.iterrows():
        price = row['open_price']
        signal = row['signal']

        if signal == 1:
            # Buy ETH with available money
            eth_to_buy = money / price
            eth += eth_to_buy
            money -= eth_to_buy * price
        elif signal == -1:
            # Sell all ETH and receive money
            money += eth * price
            eth = 0

        # Calculate current portfolio value and store in plot list
        portfolio_value = money + (eth * price)
        plot.append(portfolio_value)

    # Plot portfolio value over time
    plt.plot(plot)
    plt.xlabel('Days Since 1/1/22')
    plt.ylabel('Portfolio Value')
    plt.title('Simple Three Day Momentum Speculator')

    plt.show()
    return

def advanced_momentum_speculator():
    moneyStart = 100000
    money = moneyStart
    eth = 0
    plot = []

    df = pd.read_csv('General Models/ETH Price 2022 - open_price, close_price.csv',
                     header=None, names=['date', 'open_price', 'close_price', 'change_price'])

    # Calculate technical indicators
    df['three_day_returns'] = df['open_price'].pct_change(periods=3)
    df['rsi'] = compute_rsi(df)

    # Compute signals based on technical indicators
    df['signal'] = np.where((df['three_day_returns'] > 0) &
                            (df['rsi'] < 30), 1, 0)
    df['signal'] = np.where((df['three_day_returns'] > 0) &
                            (df['rsi'] > 70), -1, df['signal'])

    # Calculate daily eth amount and money spent
    for _, row in df.iterrows():
        price = row['open_price']
        signal = row['signal']

        if signal == 1:
            # Buy ETH with available money
            eth_to_buy = money / price
            eth += eth_to_buy
            money -= eth_to_buy * price

        elif signal == -1:
            # Sell all ETH and receive money
            money += eth * price
            eth = 0
        
        # Calculate current portfolio value and store in plot list
        portfolio_value = money + (eth * price)
        plot.append(portfolio_value)

    # Plot portfolio value over time
    plt.plot(plot)
    plt.xlabel('Days Since 1/1/22')
    plt.ylabel('Portfolio Value')
    plt.title('Advanced Momentum Speculator')

    plt.show()
    return

#-----------------------------------------------------------------------

# Compute rsi
def compute_rsi(df, n=30):
    # Calculate price differences
    delta = df['open_price'].diff()

    # Get the upward and downward price movements
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    # Calculate the smoothed average gain and loss over n periods
    avg_gain = up.rolling(window=n).mean()
    avg_loss = abs(down.rolling(window=n).mean())

    # Calculate the Relative Strength (RS) and RSI
    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))

    # Return the RSI values as a DataFrame
    return pd.DataFrame({'rsi': rsi})

def main():
    # dip_hill_speculator()
    momentum_speculator()
    advanced_momentum_speculator()

#----------------------------------------------------------------------

if __name__ == '__main__':
    main()