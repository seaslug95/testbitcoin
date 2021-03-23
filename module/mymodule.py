import pandas as pd
from datetime import timedelta

def mysimu(df, previous_days, money_ini, bitcoin_ini, prop_ini):
    date_first = df.index[0]
    date_last = df.index[-1]
    starting_date = date_first + timedelta(days=previous_days-1) #starting_date is the day first SELL/BUY can appear. -1 because date_first is included in previous_days

    dff = df.loc[date_first:date_last]

    money = money_ini
    bitcoin = bitcoin_ini
    money_vec = []
    bitcoin_vec = []
    worth_vec = []

    for date in dff.loc[date_first:starting_date].index:
        current_price = dff.loc[date]

        worth = money + bitcoin*current_price # Total Worth in Money

        if(date != starting_date): #at starting_date money and bitcoin can change
            money_vec += [money]
            bitcoin_vec += [bitcoin]
            worth_vec += [worth]

    for date in dff.loc[starting_date:].index:
        current_price = dff.loc[date]
        date_prior = date - timedelta(days=previous_days - 1)
        prices_previous = dff.loc[date_prior:date] # Last prices (current included)

        if(all(current_price > prices_previous[:-1].values)):    # If current bitcoin price higher I sell prop_ini of my bitcoin
            money = money + bitcoin*prop_ini*current_price       # I have more money
            bitcoin = bitcoin - prop_ini*bitcoin                 # I have less bitcoin

        if(all(current_price < prices_previous[:-1].values)):    # If current bitcoin price lower I buy bitcoin with prop_ini of my money
            bitcoin = bitcoin + (money*prop_ini)/current_price   # I have more bitcoin
            money = money - money*prop_ini                       # I have less money
            
        worth = money + bitcoin*current_price # Total Worth in Money
        
        money_vec += [money]
        bitcoin_vec += [bitcoin]
        worth_vec += [worth]

    data_simu = {'Closing Price': dff, 'Bitcoin' : bitcoin_vec, 'Money' : money_vec, 'Total Worth' : worth_vec } 
    df_simu = pd.DataFrame(data_simu)

    return(df_simu)
