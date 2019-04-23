"""This module does a Monte Carlo simulation and calculates the option price for each of the days"""
from math import sqrt, log, exp
import datetime as dt
import pandas_datareader.data as web
import pandas as pd
import numpy as np
from scipy.stats import norm
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Mar 28 12:09:07 2019

@author: ashton-miller
"""


def d_1(underlying, strike_price, time, risk_free_rate, sigma):
    """This function does the first part of black scholes function,
        specifically for calls """
    return (log(underlying/strike_price)+(risk_free_rate+sigma*sigma/2)*time)/(sigma*sqrt(time))


def d_2(underlying, strike, time, risk_free_rate, sigma):
    """This function does the firs part of the black scholes for puts """
    return d_1(underlying, strike, time, risk_free_rate, sigma)-sigma*sqrt(time)

def bs_call(underlying, strike, time, risk_free_rate, sigma):
    """ this function calculates the price of a call options """
    return underlying*norm.cdf(
        d_1(
            underlying, strike, time, risk_free_rate, sigma))-strike*exp(
                -risk_free_rate*time)*norm.cdf(
                    d_2(
                        underlying, strike, time, risk_free_rate, sigma))

def bs_put(underlying, strike, time, risk_free_rate, sigma):
    """ This function uses the black scholes model to calculate put option pricing"""
    return strike*exp(
        -risk_free_rate*time)-underlying + bs_call(underlying, strike, time, risk_free_rate, sigma)

"""
–>Current stock price S
–>Exercise price X
–>Maturity in years T
–>Continuously compounded risk free rate r
–>Volatility of the underlying stock sigma
"""


lower_strike_price = 303
higher_strike_price = 304
riskFreeRate = 0.0238

start = dt.datetime(1998, 3, 28)
end = dt.datetime.now()

prices = web.DataReader('SPY', 'yahoo', start, end)['Close']
returns = prices.pct_change()

percent_profit = 0.15
last_price = prices[-1]

num_simulations =1000
num_hits = 0
num_days = 35

yearly_vol = 0.10

lower_inital_option_price = float(bs_call(last_price, lower_strike_price, (num_days/365), riskFreeRate, yearly_vol))
higher_inital_option_price = float(bs_call(last_price, higher_strike_price, (num_days/365), riskFreeRate, yearly_vol))



debit_cost = lower_inital_option_price - higher_inital_option_price
max_profit = (higher_strike_price - lower_strike_price) - debit_cost

simulation_df = pd.DataFrame()


win = max_profit*1000*percent_profit
loss = 70



ttw = []
for x in range(num_simulations):

    count = 0 
    daily_vol = returns.std()
    #daily_vol = 0.015
    price_series = []
    
    price = last_price * (1+ np.random.normal(0, daily_vol))
    
    price_series.append(price)
    day_count = num_days
    for y in range(num_days):
        
        if count == num_days-1:
            ttw.append(count)
            break

        price = price_series[count] * (1+np.random.normal(0, daily_vol))
        #Here we will calculate the BS Price of the call option
        lower_option_price = float(bs_call(price, lower_strike_price, (day_count/365), riskFreeRate, yearly_vol))
        higher_option_price = float(bs_call(price, higher_strike_price, (day_count/365), riskFreeRate, yearly_vol))
        
        close_price = lower_option_price - higher_option_price
        
        profit = close_price - debit_cost
        if profit >= max_profit*percent_profit:
            num_hits += 1
            ttw.append(count)            
            break
        price_series.append(price)
        day_count -= 1
        count += 1 

print(num_hits/num_simulations)
print(sum(ttw)/len(ttw))
