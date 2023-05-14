#-----------------------------------------------------------------------
# random_speculator.py
# Author: Jackie Chen
#-----------------------------------------------------------------------

import csv
import random
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from datetime import timedelta

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
    date = []
    portfolio_value = []

    with open('General Models/eth_price.csv') as file:
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
            date.append(datetime.strptime(row[0], '%d%b%Y'))
            portfolio_value.append(money + float(row[1]) * eth)

    plt.plot(date, portfolio_value)
    plt.xlabel('Year')
    plt.ylabel('Portfolio Value ($)')
    plt.title('Buying Dip Speculator')
    print(str(money) + " " + str(eth))
    plt.show()

# Simple momentum speculator that only opens long positions
def long_momentum_speculator(n=3, start_date ='2018-01-04', end_date ='2023-01-01'):
    moneyStart = 100000
    money = moneyStart
    eth = 0
    df = pd.read_csv('General Models\eth_price_2022.csv',
                     header=None, names=['date', 'open_price', 'close_price', 'change'])
    
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Sort by date
    df.sort_index(inplace=True)

    # Restrict to start and end date
    df = df.loc[start_date:end_date]

    initial_ETH_price = df['open_price'][0]
    ETH_hold = moneyStart/initial_ETH_price

    df['momentum_returns'] = df['open_price'].pct_change(periods=n)

    df['signal'] = 0  # 0 = hold, 1 = buy, -1 = sell
    df.loc[df['momentum_returns'] > 0, 'signal'] = 1  # buy signal
    df.loc[df['momentum_returns'] < 0, 'signal'] = -1  # sell signal

    # Calculate daily eth amount and money spent
    portfolio_values = []
    hold_value = []
    dates = []
    for date, row in df.iterrows():
        # Calculate ETH to hold at beginning of period
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
        hold_value.append(ETH_hold * price)

        dates.append(date)
        portfolio_values.append(portfolio_value)

    # Plot portfolio value over time
    plt.plot(portfolio_values, label='Momentum Strategy')
    plt.plot(hold_value, label='Buying and Holding Only')
    plt.xlabel('Days')
    plt.ylabel('Portfolio Value ($)')
    plt.title('Long Momentum Speculator (n=' + str(n) + ')')
    plt.legend()
    plt.show()

    portfolio_return = ((portfolio_value[-1] - moneyStart) / moneyStart) * 100
    
    return portfolio_return

def main():
    # dip_hill_speculator()
    long_momentum_speculator(n=7, start_date='2022-10-19')

    # # Test momentum strategy with different number of days
    # num_days = [i for i in range(1, 31)]

    # # Calculate returns for each number of days
    # portfolio_returns = []
    # for n in num_days:
    #     portfolio_returns.append(long_momentum_speculator(n))

    # # Create bar chart of returns
    # plt.bar(num_days, portfolio_returns)
    # plt.xlabel('Number of Days Used for Momentum')
    # plt.ylabel('Portfolio Return (%)')
    # plt.title('Momentum Speculator Returns From 2018 to 2023', fontsize=10)

    # plt.show()

    # # Print the number of days and return for the best strategy
    # highest_returns_index = portfolio_returns.index(max(portfolio_returns))
    # print(f'Best Strategy: {num_days[highest_returns_index]} days')

    # # Calculate the best momentum window size for different window ranges (1 week, 2 weeks, 1 month, 3 months, 6 months, 1 year)
    # start_date = datetime.strptime('2018-01-04', '%Y-%m-%d')
    # end_date = datetime.strptime('2022-10-31', '%Y-%m-%d')

    # # Calculate end dates for each window range
    # num_days = (end_date - start_date).days
    # end_dates = []
    # num_weeks_from_start = []
    # for days in range(21, num_days + 1, 7):
    #     end_dates.append(start_date + timedelta(days))
    #     num_weeks_from_start.append((int)(days / 7))

    # # Calculate the best momentum window size for each window range
    # num_days = [i for i in range(1, 22)]
    # best_momentum_window_size = []
    # for end_date in end_dates:
    #     print(f'Calculating best momentum window size for {end_date}...')
    #     # Calculate returns for each number of days
    #     portfolio_returns = []
    #     for n in num_days:
    #         portfolio_returns.append(long_momentum_speculator(n, start_date, end_date))

    #     # Append the best momentum window size for the current window range
    #     highest_returns_index = portfolio_returns.index(max(portfolio_returns))
    #     best_momentum_window_size.append(num_days[highest_returns_index])

    # # Create graph of best momentum window size for each window range
    # plt.scatter(num_weeks_from_start, best_momentum_window_size)
    # plt.xlabel('Number of Weeks')
    # plt.ylabel('Best Momentum Window Size')
    # plt.title('Best Momentum Window Size for Different Window Ranges', fontsize=10)
    # plt.show()



    

#----------------------------------------------------------------------

if __name__ == '__main__':
    main()