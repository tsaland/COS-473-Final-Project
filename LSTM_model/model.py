import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from data_processing import x_input, y_price_change
import torch.nn as nn

if __name__ == '__main__':
    # load data and make training set
    train_split = 325
    train_input = torch.from_numpy(x_input[:train_split, :]) # train_split, 3
    train_target = torch.from_numpy(y_price_change[:train_split, :]) # train_split, 1 -- eth price returns = (p_{t+1}-p_{t})/p_{t}
    
    train_target_shifted_right = torch.from_numpy(y_price_change[:train_split-1, :]) # 324, 1 -- shifted eth price returns
    train_target_shifted_right = torch.cat((torch.zeros(1,1),train_target_shifted_right)) # train_split, 1 -- shifted eth price returns
    
    train_input = torch.cat((train_input,train_target_shifted_right),1) # 325, 4 -- added shifted eth price to the input
    print(train_input.shape)

    test_batch = 20
    test_input = torch.from_numpy(x_input[train_split:train_split+test_batch, :]) # 20, 4
    test_target = torch.from_numpy(y_price_change[train_split:train_split+test_batch, :]) # 20, 1

    test_target_shifted_right = torch.from_numpy(y_price_change[train_split-1:-1-test_batch, :]) # 20, 1 -- shifted eth price returns
    print(test_target_shifted_right.shape)
    test_input = torch.cat((test_input,test_target_shifted_right),1) # 20, 4 -- added shifted eth price to the input
    print(test_input.shape)

    # build the model
    input_signals = len(x_input[0])
    model = nn.LSTM(input_signals+1,30,2,proj_size=1)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=5e-3)
    n_steps = 1000
    validate_every = 10
    validation_loss_threshold = 0.000001
    last_h0 = ''
    last_c0 = ''

    #begin to train
    model.train()
    for i in range(n_steps):
        optimizer.zero_grad() 
        out,(h0,c0) = model(train_input)
        if i == n_steps - 1:
            last_h0 = h0
            last_c0 = c0
        
        loss = criterion(out, train_target)
        loss.backward()
        optimizer.step() # causes the optimizer to take a step based on the gradients
        # begin to predict, no need to track gradient here
        if i%validate_every == 0:
            print('STEP: ', i)
        with torch.no_grad(): # temporarily sets all of the requires_grad flags to false, deactives autograd function, for model validation
            pred, (_,_) = model(test_input)
            test_loss = criterion(pred, test_target)
            print('test loss:', loss.item())
            y = pred.detach().numpy() 
            if test_loss < validation_loss_threshold:
                break
    
        
