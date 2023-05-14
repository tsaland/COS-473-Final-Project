#@title Signal#5 Interest Rates
import requests
import certifi
from datetime import date


def collect_lending_rates():
    url = 'https://aave-api-v2.aave.com/data/rates-history?reserveId=0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc20xB53C1a33016B2DC2fF3653530bfF1848a515c8c5&resolutionInHours=24'
    response = requests.get(url, verify=certifi.where())
    address_content = response.json()
    interest_rate = dict()

    for daily_stats in address_content:
        this_date = daily_stats['x']
        _date = date(this_date['year'], int(
            this_date['month'])+1, this_date['date']).strftime("%Y/%m/%d")
        rate = daily_stats['stableBorrowRate_avg']
        interest_rate[_date] = rate

    return interest_rate

# Take interest rate and convert to a csv
def lending_rate_to_csv(lending_rate):
    with open('lending_rate.csv', 'w') as f:
        for date_str, rate in lending_rate.items():
            f.write(date_str + ',' + str(rate) + '\n')




   

