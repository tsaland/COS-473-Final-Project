from datetime import datetime, date, timedelta
from MWUA_simulation import MWUA
from data import net_cexflow, eth_balance, eth2stable_ratio, selected_addresses
import pandas as pd

def main():
    MWUA_wallets = MWUA()
    MWUA_cexflow = dict()
    MWUA_balance = dict()
    MWUA_eth2stable = dict()
    start_date = date(2022, 1, 1)
    end_date = date(2022, 12, 31)
    daterange = pd.date_range(start_date, end_date).date
    for day in daterange:
        day_string = day.strftime("%Y/%m/%d")
    day_cexflow = 0
    day_balance = 0
    day_eth2stable = 0
    for wallet in MWUA_wallets:
        wallet_index = selected_addresses.index(wallet)
        day_cexflow += net_cexflow[wallet_index][day_string]
        day_balance += eth_balance[wallet][day_string]
        day_eth2stable += eth2stable_ratio[wallet][day_string]
    MWUA_cexflow[day_string] = day_cexflow
    MWUA_balance[day_string] = day_balance
    MWUA_eth2stable[day_string] = day_eth2stable / len(MWUA_wallets)

    print(MWUA_cexflow)
    print(MWUA_balance)
    print(MWUA_eth2stable)

    df = pd.DataFrame(MWUA_balance, index=[0]) 
    df.head()
    df.to_csv(index=False)

if __name__ == "__main__":
    main()