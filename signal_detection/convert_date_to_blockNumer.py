#@title Implement convert_date_to_blockNumber(_date) 
# get block at timestamp. cited from https://github.com/ethereum/web3.py/issues/1872#issuecomment-932675448
import ciso8601

def search_block_number(timestamp, w3):
    target_timestamp = timestamp
    averageBlockTime = 15.1
    block = w3.eth.getBlock('latest')
    blockNumber = block['number']
    blockTime = block['timestamp']
    lowerLimitStamp = target_timestamp
    higherLimitStamp = target_timestamp + 30
    requestsMade = 1

    while blockTime > target_timestamp:
        decreaseBlocks = int((blockTime - target_timestamp) / averageBlockTime)
        if decreaseBlocks < 1:
            break
        blockNumber -= decreaseBlocks
        block = w3.eth.getBlock(blockNumber)
        blockTime = block['timestamp']
        requestsMade += 1

    if blockTime < lowerLimitStamp:
        while blockTime < lowerLimitStamp:
            blockNumber += 1
            block = w3.eth.getBlock(blockNumber)
            blockTime = block['timestamp']
            requestsMade += 1
    
    if blockTime > higherLimitStamp:
         while blockTime > lowerLimitStamp:
            blockNumber -= 1
            block = w3.eth.getBlock(blockNumber)
            blockTime = block['timestamp']
            requestsMade += 1       
    
    return blockNumber

def convert_date_to_blockNumber(_date, w3):
  date_string = _date.isoformat()
  timestamp = ciso8601.parse_datetime(date_string).timestamp()
  block = search_block_number(timestamp, w3)
  return block
