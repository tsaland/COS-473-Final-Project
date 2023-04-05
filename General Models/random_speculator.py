#-----------------------------------------------------------------------
# random_speculator.py
# Author: Jackie Chen
#-----------------------------------------------------------------------

import csv
import random
import matplotlib.pyplot as plt

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

def momentum_specutlator():
    #TODO, Thanks Tucker
    return

#-----------------------------------------------------------------------

def main():
    dip_hill_speculator()

#----------------------------------------------------------------------

if __name__ == '__main__':
    main()