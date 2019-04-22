#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 11:13:16 2019

@author: ashtonmiller
"""





import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style


style.use('ggplot')
start = dt.datetime(1998, 3, 28)
end = dt.datetime(2018, 3, 31)

prices = web.DataReader('SPY', 'yahoo', start, end)['Close']
returns = prices.pct_change()


last_price = prices[-1]

num_simulations = 1000
num_days = 369


simulation_df = pd.DataFrame()

for x in range(num_simulations):
    count = 0 
    daily_vol = returns.std()
    
    price_series = []
    
    price = last_price * (1+ np.random.normal(0, daily_vol))
    
    price_series.append(price)
    
    for y in range(num_days):
        if count == num_days-1:
            break
        price = price_series[count] * (1+np.random.normal(0, daily_vol))
        price_series.append(price)
        count += 1
    simulation_df[x] = price_series
fig = plt.figure()
fig.suptitle('Monte Carlos Simulation: SPY')
plt.plot(simulation_df)
plt.axhline(y = last_price, color= 'r', linestyle='-')
plt.xlabel('Day')
plt.ylabel('Price')
plt.show()