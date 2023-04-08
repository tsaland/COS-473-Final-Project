# from sklearn.model_selection import KFold
# import torch
# import torch.nn as nn
# import torch.optim as optim
# import numpy as np
# import matplotlib.pyplot as plt
# import torch.nn as nn
# from data_processing import *

# def LSTM_model():
#     # load data and make training set
#     x_input, y_price_change, __ = data_processing()
#     train_split = 325
#     train_input = torch.from_numpy(x_input[:train_split, :])  # train_split, 3
#     # train_split, 1 -- eth price returns = (p_{t+1}-p_{t})/p_{t}
#     train_target = torch.from_numpy(y_price_change[:train_split, :])

#     train_target_shifted_right = torch.from_numpy(
#         y_price_change[:train_split-1, :])  # 324, 1 -- shifted eth price returns
#     # train_split, 1 -- shifted eth price returns
#     train_target_shifted_right = torch.cat(
#         (torch.zeros(1, 1), train_target_shifted_right))

#     # 325, 4 -- added shifted eth price to the input
#     train_input = torch.cat((train_input, train_target_shifted_right), 1)

#     # use K-fold cross-validation to split the data
#     n_splits = 5
#     kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

#     # initialize variables to store results
#     all_test_loss = []
#     all_last_h0 = []
#     all_last_c0 = []
#     all_models = []
#     all_criterions = []

#     # iterate through each fold
#     for fold, (train_idx, test_idx) in enumerate(kf.split(x_input)):
#         print(f'Fold {fold+1}/{n_splits}')

#         train_input = torch.from_numpy(x_input[train_idx, :])
#         train_target = torch.from_numpy(y_price_change[train_idx, :])
#         train_target_shifted_right = torch.from_numpy(y_price_change[train_idx-1, :])

#         assert train_input.shape[0] == train_target_shifted_right.shape[0], "Dimensions do not match"
#         train_input = torch.cat((train_input, train_target_shifted_right), 1)

#         test_input = torch.from_numpy(x_input[test_idx, :])
#         test_target = torch.from_numpy(y_price_change[test_idx, :])
#         test_target_shifted_right = torch.from_numpy(y_price_change[test_idx-1, :])
#         test_input = torch.cat((test_input, test_target_shifted_right), 1)

#         # build the model
#         input_signals = len(x_input[0])
#         model = nn.Sequential(
#             nn.Linear(input_signals+1, 64),
#             nn.LSTM(64, 30, 2, dropout=0.2, proj_size=1)
#         )
#         criterion = nn.MSELoss()
#         optimizer = optim.Adam(model.parameters(), lr=5e-3)

#         # set up training parameters
#         n_steps = 100
#         validate_every = 10
#         validation_loss_threshold = 0.0001
#         last_h0 = ''
#         last_c0 = ''

#         # begin to train
#         model.train()
#         for i in range(n_steps):
#             optimizer.zero_grad()
#             out = model(train_input)
#             if i == n_steps - 1:
#                 last_h0 = out[1][0]
#                 last_c0 = out[1][1]

#             loss = criterion(out[0], train_target)
#             loss.backward()
#             optimizer.step()

#             if i % validate_every == 0:
#                 model.eval()
#                 test_loss = criterion(model(test_input)[0], test_target)
#                 print(f'Epoch {i}: train loss = {loss.detach().numpy():.4f}, test loss = {test_loss.detach().numpy():.4f}')
#                 all_test_loss.append(test_loss.detach().numpy())
#                 model.train()

#                 if test_loss < validation_loss_threshold:
#                     break

#         all_last_h0.append(last_h0.detach().numpy())
#         all_last_c0.append(last_c0.detach().numpy())
#         all_criterions.append(criterion)


#     return all_test_loss, all_last_h0, all_last_c0, all_models, all_criterions


import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
import torch.nn as nn
from data_processing import *


def LSTM_model():
    # load data and make training set
    x_input, y_price_change, __ = data_processing()
    x_input = x_input[:264, :]
    y_price_change = y_price_change[:264, :]
    train_split = 224
    train_input = torch.from_numpy(x_input[:train_split, :])  # train_split, 3
    # train_split, 1 -- eth price returns = (p_{t+1}-p_{t})/p_{t}
    train_target = torch.from_numpy(y_price_change[:train_split, :])

    train_target_shifted_right = torch.from_numpy(
        y_price_change[:train_split-1, :])  # 324, 1 -- shifted eth price returns
    # train_split, 1 -- shifted eth price returns
    train_target_shifted_right = torch.cat(
        (torch.zeros(1, 1), train_target_shifted_right))

    # 325, 4 -- added shifted eth price to the input
    train_input = torch.cat((train_input, train_target_shifted_right), 1)
    print(train_input.shape)

    test_batch = 20
    test_input = torch.from_numpy(
        x_input[train_split:train_split+test_batch, :])  # 20, 4
    test_target = torch.from_numpy(
        y_price_change[train_split:train_split+test_batch, :])  # 20, 1

    test_target_shifted_right = torch.from_numpy(
        y_price_change[train_split-1:-1-test_batch, :])  # 20, 1 -- shifted eth price returns
    print(test_target_shifted_right.shape)
    # 20, 4 -- added shifted eth price to the input
    test_input = torch.cat((test_input, test_target_shifted_right), 1)
    print(test_input.shape)

    # build the model
    input_signals = len(x_input[0])
    model = nn.Sequential(
        nn.Linear(input_signals+1, 64),
        nn.LSTM(64, 30, dropout=0.8, proj_size=1)
    )
    # model = nn.LSTM(input_signals+1, 30, 2, proj_size=1)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=5e-3)
    n_steps = 100
    validate_every = 10
    validation_loss_threshold = 0.0000001
    last_h0 = ''
    last_c0 = ''

    #begin to train
    model.train()
    for i in range(n_steps):
        optimizer.zero_grad()
        out, (h0, c0) = model(train_input)
        if i == n_steps - 1:
            last_h0 = h0
            last_c0 = c0

        loss = criterion(out, train_target)
        loss.backward()
        optimizer.step()  # causes the optimizer to take a step based on the gradients
        # begin to predict, no need to track gradient here
        if i % validate_every == 0:
            print('STEP: ', i)
        with torch.no_grad():  # temporarily sets all of the requires_grad flags to false, deactives autograd function, for model validation
            pred, (_, _) = model(test_input)
            test_loss = criterion(pred, test_target)
            print('test loss:', loss.item())
            y = pred.detach().numpy()
            if test_loss < validation_loss_threshold:
                break

    return last_c0, last_h0, model, criterion

if __name__ == '__main__':

    # c0, h0, model, criterion = LSTM_model()

    # # Save the model
    # torch.save(model.state_dict(), 'model.pth')

    x_input, y_price_change, __ = data_processing()
    print(len(x_input))
    # Generate random number
    index = 250

    x_input = x_input[index:index+100, :]
    y_price_change = y_price_change[index:index+100, :]

    train_split = 100
    train_input = torch.from_numpy(x_input[:train_split, :])  # train_split, 3
    # train_split, 1 -- eth price returns = (p_{t+1}-p_{t})/p_{t}
    train_target = torch.from_numpy(y_price_change[:train_split, :])

    train_target_shifted_right = torch.from_numpy(
        y_price_change[:train_split-1, :])  # 324, 1 -- shifted eth price returns
    # train_split, 1 -- shifted eth price returns
    train_target_shifted_right = torch.cat(
        (torch.zeros(1, 1), train_target_shifted_right))

    # 325, 4 -- added shifted eth price to the input
    train_input = torch.cat((train_input, train_target_shifted_right), 1)
    print(train_input.shape)

    model = nn.Sequential(
        nn.Linear(len(x_input[0])+1, 64),
        nn.LSTM(64, 30, dropout=0.8, proj_size=1)
    )

    model.load_state_dict(torch.load('model.pth'))

    # Make prediction
    pred, (_, _) = model(train_input)

    # Plot the prediction
    plt.plot(pred.detach().numpy(), color='red', label='LSTM Prediction')
    plt.plot(train_target.detach().numpy(), color='blue', label='Actual Price')
    plt.title('ETH Price Prediction')
    plt.xlabel('Days')
    plt.ylabel('ETH Price')
    plt.legend()
    plt.show()

    # Plot strategy returns that result from the predicted price changes
    money = 100000
    money_list = []

    for i in range(len(pred)):
        if pred[i] > 0.015:
            money = money * (1 + train_target[i])

        if pred[i] < -0.015:
            money = money * (1 - train_target[i])

        money_list.append(money)

    plt.plot(money_list, color='blue', label='LSTM Prediction Returns')
    plt.title('Strategy Returns')
    plt.xlabel('Days')
    plt.ylabel('Portfolio Value')
    plt.legend()
    plt.show()


