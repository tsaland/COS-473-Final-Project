from datetime import date, timedelta
import pandas as pd
from convert_date_to_blockNumer import convert_date_to_blockNumber
from web3 import Web3
import psycopg2

# Get most recent date from database
def get_most_recent_date(cur):
    # Execute a query
    cur.execute("SELECT * FROM eth_balance ORDER BY date DESC LIMIT 1;")

    # Fetch the results of the query
    results = cur.fetchall()

    date = results[0][1]
    return date
    

def collect_ethbalance(selected_addresses, w3, startdate_, enddate_):
    whales_individual_balance = dict()
    whales_total_balance = dict()
    range = pd.date_range(startdate_, enddate_)
    for address in selected_addresses:
        whales_individual_balance[address] = dict()
        for _date in range:
            date_string = _date.date().strftime("%Y/%m/%d")
            whales_individual_balance[address][date_string] = 0
    for _date in range:
        date_string = _date.date().strftime("%Y/%m/%d")
        whales_total_balance[date_string] = 0

    for _date in range:
        block = convert_date_to_blockNumber(_date.date(), w3)
        date_string = _date.date().strftime("%Y/%m/%d")
        for address in selected_addresses:
            checksum = Web3.toChecksumAddress(address)
            balance = float(w3.fromWei(w3.eth.get_balance(checksum, block_identifier=block), 'ether'))
            whales_individual_balance[address][date_string] = balance
            whales_total_balance[date_string] += balance

    return whales_total_balance, whales_individual_balance

# Define a function to insert individual whale balances into the database
def insert_whale_balance(cur, address, date_string, balance):
    query = "INSERT INTO eth_balance (address, date, eth_balance) VALUES (%s, %s, %s)"
    data = (address, date_string, balance)
    cur.execute(query, data)

# Get selected addresses from database
def get_selected_addresses(cur):
    # Execute a query
    cur.execute("SELECT * FROM selected_addresses;")

    # Fetch the results of the query
    results = cur.fetchall()

    selected_addresses = []
    for result in results:
        selected_addresses.append(result[0])
    return selected_addresses


# Main function
if __name__ == "__main__":
        # Establish a connection to the database
    conn = psycopg2.connect(
        host='whalewatch.postgres.database.azure.com',
        port=5432,
        dbname='data',
        user='Postgres',
        password='WhaleWatch!',
        sslmode='require'
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Get selected addresses
    selected_addresses = get_selected_addresses(cur)

    # Get most recent date
    recent_date = get_most_recent_date(cur)

    # Make start date equal to most recent date + 1 day
    startdate = recent_date + timedelta(days=1)
    print(startdate)

    # Make end date equal to today
    enddate = date.today()

    # Connect to web3
    alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/OPutfOp_VyXojpS6t3xDlHiUnWCX8D1e"
    w3 = Web3(Web3.HTTPProvider(alchemy_url))

    # Collect eth balance
    _, whales_individual_balance = collect_ethbalance(selected_addresses, w3, startdate, enddate)

    # Insert the individual whale balances into the database
    for address, balance_dict in whales_individual_balance.items():
        for date_string, balance in balance_dict.items():
            insert_whale_balance(cur, address, date_string, balance)

    # Commit the changes to the database
    conn.commit()

    # Close communication with the database
    cur.close()

    # Close the connection
    conn.close()