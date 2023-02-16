import random
from hexbytes import HexBytes
from web3 import Web3
from datetime import date 
from convert_date_to_blockNumer import convert_date_to_blockNumber

def select_whales(w3, exchange_wallets):
    addresses = set()

    Multichain_bridge = ['0x13B432914A996b0A48695dF9B2d701edA45FF264']
    Zigzag_bridge = ['0xCC9557F04633d82Fb6A1741dcec96986cD8689AE']
    Narni_bridge = ['0x4103c267Fba03A1Df4fe84Bc28092d629Fa3f422']
    bridge_wallets = list(set().union(Multichain_bridge, Zigzag_bridge, Narni_bridge))

    Circle_wallets = ['0x55fe002aeff02f77364de339a1292923a15844b8']
    BitcoinSuisse_wallets = ['0x622de9bb9ff8907414785a633097db438f9a2d86', '0xdd9663bd979f1ab1bada85e1bc7d7f13cafe71f8', '0xec70e3c8afe212039c3f6a2df1c798003bf7cfe9', '0x3837ea2279b8e5c260a78f5f4181b783bbe76a8b', '0x2a7077399b3e90f5392d55a1dc7046ad8d152348', '0xc2288b408dc872a1546f13e6ebfa9c94998316a2']
    custodian_wallets = list(set().union(Circle_wallets, BitcoinSuisse_wallets, bridge_wallets))

    null_addresses = ['0x000000000000000000000000000000000000dead', '0x0000000000000000000000000000000000000000', '0x0000000000000000000000000000000000000001', '0x0000000000000000000000000000000000000002', '0x0000000000000000000000000000000000000003',
                    '0x0000000000000000000000000000000000000004', '0x0000000000000000000000000000000000000005', '0x0000000000000000000000000000000000000006', '0x0000000000000000000000000000000000000007', '0x0000000000000000000000000000000000000008',
                    '0x0000000000000000000000000000000000000009', '0x00000000000000000000045261d4ee77acdb3286', '0x0123456789012345678901234567890123456789', '0x1111111111111111111111111111111111111111', '0x1234567890123456789012345678901234567890',
                    '0x2222222222222222222222222222222222222222', '0x3333333333333333333333333333333333333333', '0x4444444444444444444444444444444444444444', '0x6666666666666666666666666666666666666666', '0x8888888888888888888888888888888888888888',
                    '0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', '0xdead000000000000000042069420694206942069', '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee', '0xffffffffffffffffffffffffffffffffffffffff', '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa']

    # randomly sample blocks from the first block in 2022 to the latest block
    latest_block = w3.eth.get_block('latest')['number']
    start_date = date(2018, 1, 1)
    start_block = convert_date_to_blockNumber(start_date, w3)
    sample_blocks = random.sample(list(range(start_block,latest_block)), 100)
    excluded_wallets = list(set().union(exchange_wallets, null_addresses, custodian_wallets))
    print("we sample 100 blocks for the past 5 years", sample_blocks)
    for nonce in sample_blocks: # takes 26min to go through 40 blocks/8853 txs, and 10 minutes to go through 7000 wallets
        block = w3.eth.getBlock(nonce)
        block_transactions = block['transactions']
        for tx in block_transactions:
            getTrans = Web3.toJSON(tx).strip('"')
            trans = w3.eth.get_transaction(getTrans)
            try:
                _from = trans['from']
                _to = trans['to']
                # only append wallet addresses that are not contract addresses or exchange wallets
                if w3.eth.get_code(_from) == HexBytes("0x") and _from.lower() not in excluded_wallets:
                    addresses.add(_from)
                if w3.eth.get_code(_to) == HexBytes("0x") and _to.lower() not in excluded_wallets:
                    addresses.add(_to)
            except KeyError:
                print("ignore the invalid transaction with hash", trans['hash'].hex())
    print("we found a total of", len(addresses), "unique addresses")

    # recreate the state of all the addresses
    state = dict()
    for address in addresses:
        balance = w3.fromWei(w3.eth.get_balance(address),'ether')
        state[address] = balance

    sorted_state = sorted(state, key=state.get, reverse=True)
    selected_addresses = sorted_state[:int(len(sorted_state)*0.05)]
    print(selected_addresses)
    print("we take 5% of the total wallets by balance and limit to a total of", len(selected_addresses), "whales addresses")
    return selected_addresses