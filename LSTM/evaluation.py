import matplotlib.pyplot as plt
import torch
import numpy as np
from data_processing import data_processing
from model import LSTM_model

def evaluation_MSEloss():
  x_input, y_price_change, eth_price = data_processing()
  last_c0, last_h0, model, criterion = LSTM_model()
  # evaluate with last 20 days
  # eval_input = torch.from_numpy(x_input[train_split+test_batch:, :]) # 20, 4
  # eval_target = torch.from_numpy(y_price[train_split+test_batch:, :]) # 20, 1
  # eval_target_shifted_right = torch.from_numpy(y_price[train_split+test_batch-1:-1, :]) # 20, 1 -- shifted eth price returns
  # print(eval_target_shifted_right.shape)
  # eval_input = torch.cat((eval_input,eval_target_shifted_right),1) # 20, 4 -- added shifted eth price to the input
  # print(eval_input.shape)

  # evaluate with the entire year
  eval_input = torch.from_numpy(x_input[1:, :]) # 364, 4
  eval_target = torch.from_numpy(y_price_change[1:, :]) # 364, 1

  eval_target_shifted_right = torch.from_numpy(y_price_change[0:-1, :]) # 364, 1 -- shifted eth price returns
  print(eval_target_shifted_right.shape)
  eval_input = torch.cat((eval_input,eval_target_shifted_right),1) # 364, 4 -- added shifted eth price to the input
  print(eval_input.shape)

  with torch.no_grad(): # temporarily sets all of the requires_grad flags to false, deactives autograd function, for model validation
    # eval_pred, (_,_) = model(eval_input, (last_h0, last_c0))
    eval_pred, (_,_) = model(eval_input)
    eval_loss = criterion(eval_pred, eval_target)
    print('evaluation loss:', eval_loss.item())
    y = eval_pred.detach().numpy() 

  plt.figure(figsize=(15,7))
  plt.title("DeltaCron LSTM Model Evaluation")
  plt.xlabel('Entire Year of 2022', fontsize=20)
  plt.ylabel('ETH Price Percentage Change', fontsize=20)
  plt.xticks(fontsize=20)
  plt.yticks(fontsize=20)
  plt.plot(np.arange(len(eval_input)), eval_target, 'c', linewidth = 2.0, label='actual price change')
  plt.plot(np.arange(len(eval_input)), y, 'm' , linewidth = 2.0, label='predicted price change')
  plt.legend(fontsize=20)

  # print predicted price
  pred_price = []
  pred_price.append(eth_price[0])
  for day in range(len(eval_pred)):
    pred = eval_pred[day]
    newpred = eth_price[day] * pred + eth_price[day] # using prev day's price to calculate prediction price
    pred_price.append(newpred.item())
  return (eval_pred, pred_price, eth_price)

# evaluate based on monetary loss in all-in strategy 
def evaluation_ALLIN(eval_pred, pred_price, eth_price):
  # based on our predictions for day 1 to day 364 (zero-indexed), we take actions from day 0 to day 363
  USDC_balance = 200
  ETH_balance = 0.5
  begin_balance = USDC_balance + ETH_balance * eth_price[0] # beginning balance at second day of the year 

  allin_balance = []
  allin_balance.append(begin_balance)

  for day in range(len(eval_pred)): 
    pred = eval_pred[day]
    if pred > 0: # buying eth
      ETH_balance += USDC_balance / eth_price[day]
      USDC_balance = 0
      allin_balance.append(ETH_balance * eth_price[day])
    elif pred < 0: # selling eth
      USDC_balance += ETH_balance * eth_price[day]
      ETH_balance = 0
      allin_balance.append(USDC_balance)
    else:
      allin_balance.append(USDC_balance + ETH_balance * eth_price[day])
  print(pred_price.shape)
  print('monetary loss under all in strategy', allin_balance[-1] - allin_balance[0])
  plt.figure(figsize=(15, 7))
  plt.plot(np.arange(365), allin_balance, 'c', linewidth=2.0, label='total balance')
  plt.plot(np.arange(365), eth_price, 'r', linewidth=2.0, label='eth price')
  plt.plot(np.arange(365), pred_price, 'b', linewidth=2.0, label='predicted eth price')
  plt.title("Monetary Loss Evaluation - All-in Strategy", fontsize=20)
  plt.xlabel('Entire Year of 2022', fontsize=20)
  plt.ylabel('Amount in USD', fontsize=20)
  plt.legend(fontsize=20)
  plt.show()

# evaluate based on monetary loss in proportional strategy 
def evaluation_PROPORTIONAL(eval_pred, pred_price, eth_price):
  USDC_balance = 200
  ETH_balance = 0.5
  begin_balance = USDC_balance + ETH_balance * eth_price[0] # beginning balance before Day 0

  proportional_balance = []
  proportional_balance.append(begin_balance)
  _lambda = 10
  for day in range(len(eval_pred)): 
    pred = eval_pred[day].item()
    if pred > 0: # buying eth
      amount_buy_usd = USDC_balance * pred * _lambda
      ETH_balance +=  amount_buy_usd / eth_price[day]
      USDC_balance -= amount_buy_usd
      proportional_balance.append(ETH_balance * eth_price[day] + USDC_balance)
    elif pred < 0: # selling eth
      amount_sold_eth = ETH_balance * (-1) * pred * _lambda
      USDC_balance += amount_sold_eth * eth_price[day]
      ETH_balance -= amount_sold_eth
      proportional_balance.append(ETH_balance * eth_price[day] + USDC_balance)
    else:
      proportional_balance.append(USDC_balance + ETH_balance * eth_price[day])

  print('monetary loss under proportional strategy', proportional_balance[-1] - proportional_balance[0])
  plt.figure(figsize=(15, 7))
  plt.plot(np.arange(365), proportional_balance, 'c', linewidth=2.0, label='total balance')
  plt.plot(np.arange(365), eth_price, 'r', linewidth=2.0, label='eth price')
  plt.plot(np.arange(365), pred_price, 'b', linewidth=2.0, label='predicted eth price')
  plt.title("Monetary Loss Evaluation - Proportional Strategy", fontsize=20)
  plt.xlabel('Entire Year of 2022', fontsize=20)
  plt.ylabel('Amount in USD', fontsize=20)
  plt.legend(fontsize=20)
  plt.show()

if __name__ == "__main__":
  eval_pred, pred_price, eth_price = evaluation_MSEloss()
  eval_pred = np.array(eval_pred)
  pred_price = np.array(pred_price)
  evaluation_ALLIN(eval_pred, pred_price, eth_price)
  evaluation_PROPORTIONAL(eval_pred, pred_price, eth_price)
