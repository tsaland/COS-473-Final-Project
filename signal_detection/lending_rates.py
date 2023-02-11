#@title Signal#5 Interest Rates
import requests
import certifi
from datetime import date

def collect_lending_rates():
    url = 'https://aave-api-v2.aave.com/data/rates-history?reserveId=0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc20xB53C1a33016B2DC2fF3653530bfF1848a515c8c5&from=1640995200&resolutionInHours=24'
    response = requests.get(url, verify=certifi.where())
    address_content = response.json()
    interest_rate = dict()
    for daily_stats in address_content:
        rate = daily_stats['stableBorrowRate_avg']
        this_date = daily_stats['x']
        if this_date['year'] == 2023:
            break
        _date = date(this_date['year'], int(this_date['month'])+1, this_date['date']).strftime("%Y/%m/%d")
        interest_rate[_date] = rate

    print(interest_rate)
    return interest_rate
   

