from data import eth_balance

import csv

# Open a new CSV file for writing
with open('eth_balance.csv', 'w', newline='') as file:

    # Define the CSV writer object
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['Wallet Address', 'Date', 'Balance'])

    # Iterate over each wallet address in the dictionary
    for wallet_address, balance_dict in eth_balance.items():

        # Iterate over each date and balance in the balance dictionary
        for date, eth2stable in balance_dict.items():

            # Write a row to the CSV file with the wallet address, date, and balance
            writer.writerow([wallet_address, date, eth2stable])