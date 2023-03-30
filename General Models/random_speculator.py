#-----------------------------------------------------------------------
# random_speculator.py
# Author: Jackie Chen
#-----------------------------------------------------------------------

import csv
import random

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

def educated_speculator():
    money = 0
    eth = 0
    # TODO unfinished

#-----------------------------------------------------------------------

def main():
    random_speculator()

#----------------------------------------------------------------------

if __name__ == '__main__':
    main()