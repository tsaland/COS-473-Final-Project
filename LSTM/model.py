import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
import torch.nn as nn
from data_processing import *
import matplotlib.ticker as mtick

class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size, dropout=0.2):
        super(LSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, dropout=dropout)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out)
        return out


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
    model = LSTM(input_signals+1, 64, 2, 1, dropout=0.2)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=5e-3)
    n_steps = 100
    validate_every = 10
    validation_loss_threshold = 0.0000001

    #begin to train
    model.train()
    for i in range(n_steps):
        out = model(train_input)

        optimizer.zero_grad()
        loss = criterion(out, train_target)
        loss.backward()
        optimizer.step()  # causes the optimizer to take a step based on the gradients
        # begin to predict, no need to track gradient here
        if i % validate_every == 0:
            print('STEP: ', i)
        with torch.no_grad():  # temporarily sets all of the requires_grad flags to false, deactives autograd function, for model validation
            pred = model(test_input)
            test_loss = criterion(pred, test_target)
            print('test loss:', loss.item())
            y = pred.detach().numpy()
            if test_loss < validation_loss_threshold:
                break

    return model

if __name__ == '__main__':

    # model = LSTM_model()

    # # Save the model
    # torch.save(model.state_dict(), 'model.pth')

    x_input, y_price_change, __ = data_processing()

    index = 292

    x_input = x_input[index:, :]
    y_price_change = y_price_change[index:, :]

    train_split = 73
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

    model = LSTM(len(x_input[0])+1, 64, 2, 1, dropout=0.2)

    model.load_state_dict(torch.load('model.pth'))

    # Make prediction
    pred = model(train_input)

    # Plot the prediction
    plt.plot((pred.detach().numpy())*100, color='red', label='LSTM Prediction')
    plt.plot((train_target.detach().numpy())*100, color='blue', label='Actual Price')
    plt.title('ETH Price Prediction')
    plt.xlabel('Days')
    plt.ylabel('Change in ETH Price')

    # Format y-axis as percentage
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend()
    plt.show()

    # Plot strategy returns that result from the predicted price changes
    money = 100000
    ethereum_value = 100000
    money_list = []
    ethereum_value_list = []

    for i in range(len(pred)):
        if pred[i] > 0.015:
            money = money * (1 + train_target[i])

        if pred[i] < -0.015:
            money = money * (1 - train_target[i])

        money_list.append(money)
        ethereum_value = ethereum_value * (1 + train_target[i])
        ethereum_value_list.append(ethereum_value)


    plt.plot(money_list, color='blue', label='LSTM Prediction Returns')
    plt.plot(ethereum_value_list, color='red', label='Buy and Hold Returns')
    plt.title('Strategy Returns')
    plt.xlabel('Days')
    plt.ylabel('Portfolio Value ($)')
    plt.ylim(80000, 155000)
    plt.legend(loc='upper left')
    plt.show()


