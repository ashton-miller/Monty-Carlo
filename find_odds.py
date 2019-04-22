#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 11:57:10 2019

@author: ashtonmiller
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 12:09:07 2019

@author: ashtonmiller
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from math import sqrt, log, exp, pi

#first define these 2 functions
def d1(S,X,T,r,sigma):
    return (log(S/X)+(r+sigma*sigma/2.)*T)/(sigma*sqrt(T))

def d2(S,X,T,r,sigma):
    return d1(S,X,T,r,sigma)-sigma*sqrt(T)

#define the call option price function
def bs_call(S,X,T,r,sigma):
     return S*CND(d1(S,X,T,r,sigma))-X*exp(-r*T)*CND(d2(S,X,T,r,sigma))

#define the put options price function
def bs_put(S,X,T,r,sigma):
      return X*exp(-r*T)-S + bs_call(S,X,T,r,sigma)

#define cumulative standard normal distribution
def CND(X):
     (a1,a2,a3,a4,a5)=(0.31938153,-0.356563782,1.781477937,-1.821255978,1.330274429)
     L = abs(X)
     K=1.0/(1.0+0.2316419*L)
     w=1.0-1.0/sqrt(2*pi)*exp(-L*L/2.)*(a1*K+a2*K*K+a3*pow(K,3)+a4*pow(K,4)+a5*pow(K,5))
     if X<0:
        w=1.0-w
     return w 
 
"""
–>Current stock price S
–>Exercise price X
–>Maturity in years T
–>Continuously compounded risk free rate r
–>Volatility of the underlying stock sigma
"""




atm_debit_spread_cost = 0.27
num_days = 8


lower_strike_price = 286.5
higher_strike_price = 287
riskFreeRate = 0.0238



import pandas_datareader.data as web

import pandas as pd
import datetime as dt
import numpy as np


start = dt.datetime(1998, 3, 28)
end = dt.datetime.now()

prices = web.DataReader('SPY', 'yahoo', start, end)['Close']
returns = prices.pct_change()

percent_profit = 0.25
last_price = prices[-1]

num_simulations = 1000
num_hits = 0


yearly_vol = 1

lower_inital_option_price = float(bs_call(last_price, lower_strike_price, (num_days/365), riskFreeRate, yearly_vol))
higher_inital_option_price = float(bs_call(last_price, higher_strike_price, (num_days/365), riskFreeRate, yearly_vol))



debit_cost = lower_inital_option_price - higher_inital_option_price

while debit_cost <= atm_debit_spread_cost - 0.01 or debit_cost >= atm_debit_spread_cost + 0.01:
    yearly_vol -= 0.001

    lower_inital_option_price = float(bs_call(last_price, lower_strike_price, (num_days/365), riskFreeRate, yearly_vol))
    higher_inital_option_price = float(bs_call(last_price, higher_strike_price, (num_days/365), riskFreeRate, yearly_vol))
    debit_cost = lower_inital_option_price - higher_inital_option_price

print(debit_cost, yearly_vol)
debit_cost = lower_inital_option_price - higher_inital_option_price


max_profit = (higher_strike_price - lower_strike_price) - debit_cost

simulation_df = pd.DataFrame()


win = max_profit*1000*percent_profit
loss = 70




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
            break

        price = price_series[count] * (1+np.random.normal(0, daily_vol))
        #Here we will calculate the BS Price of the call option
        lower_option_price = float(bs_call(price, lower_strike_price, (day_count/365), riskFreeRate, yearly_vol))
        higher_option_price = float(bs_call(price, higher_strike_price, (day_count/365), riskFreeRate, yearly_vol))
        
        close_price = lower_option_price - higher_option_price
        
        profit = close_price - debit_cost
        if profit >= max_profit*percent_profit:
            num_hits += 1
            break
        price_series.append(price)
        day_count -= 1
        count += 1

print(num_hits/num_simulations)
