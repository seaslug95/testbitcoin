import module.mymodule as mymodule
import pytest

import pandas as pd
from datetime import timedelta
# python -m pytest -v --cov module tests/
# python tests/test_mymodule.py
# python -m pytest -v --cov=module --cov-report html tests/

path = './tests/'

def mydf(path, data):
    col_list = ['Date', 'Close', 'bitcoin', 'money', 'worth']
    df = pd.read_csv(path+data, usecols=col_list)
    df['Date'] = pd.to_datetime(df['Date'])
    df.rename(columns={'Close': 'Closing Price', 'bitcoin': 'Bitcoin', 'money': 'Money', 'worth': 'Total Worth'}, inplace=True)
    df.set_index('Date', inplace=True)
    df = df.squeeze('columns')
    return(df)

def test_stable():
    data = 'test_stable_solved.csv'
    df_solved = mydf(path, data)
    df_test = df_solved['Closing Price']

    previous_days = 5
    money_ini = 100
    bitcoin_ini = 1
    prop_ini = 0.1

    df_simu = mymodule.mysimu(df_test, previous_days, money_ini, bitcoin_ini, prop_ini)

    assert df_simu.round(3).equals(df_solved.round(3))

def test_decrease():
    data = 'test_decrease_solved.csv'
    df_solved = mydf(path, data)
    df_test = df_solved['Closing Price']

    previous_days = 10
    money_ini = 100
    bitcoin_ini = 1
    prop_ini = 0.2

    df_simu = mymodule.mysimu(df_test, previous_days, money_ini, bitcoin_ini, prop_ini)

    assert df_simu.round(3).equals(df_solved.round(3))

def test_increase():
    data = 'test_increase_solved.csv'
    df_solved = mydf(path, data)
    df_test = df_solved['Closing Price']

    previous_days = 15
    money_ini = 100
    bitcoin_ini = 1
    prop_ini = 0.3

    df_simu = mymodule.mysimu(df_test, previous_days, money_ini, bitcoin_ini, prop_ini)

    assert df_simu.round(3).equals(df_solved.round(3))

def test_mix():
    data = 'test_mix1_solved.csv'
    df_solved = mydf(path, data)
    df_test = df_solved['Closing Price']

    previous_days = 5
    money_ini = 100
    bitcoin_ini = 1
    prop_ini = 0.1

    df_simu = mymodule.mysimu(df_test, previous_days, money_ini, bitcoin_ini, prop_ini)

    assert df_simu.round(3).equals(df_solved.round(3))
