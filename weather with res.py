#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:53:50 2024

@author: devakipatel
"""
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import pandas as pd 
data = pd.read_excel('cook2.xlsx', engine= 'openpyxl') 

df = pd.DataFrame(data)

def FtoC(farenheit):
    return (farenheit-32)*5/9

df['temperature']= df['temperature'].apply(FtoC)


plt.plot(df['time'], df['temperature'], label='temp', color = 'red', marker = 'o')

plt.xlabel("time")
plt.ylabel("temperature")
plt.title("Maax, min and avg values over days")

plt.legend()
plt.show()

def sin(x, a, b, c, d):
    x = x
    return a*np.sin(b*(x-c)) + d +

x = [t for t in df.time]
p, _ = curve_fit(
    sin, x, df.temperature, 
    p0 = [20, 2*np.pi/365, 0, 50]
    )
T = (2*np.pi/ p[1])


plt.plot(
    x, sin(x, *p), 
    lw = 3, c = 'black', zorder = 9001)

df.set_index('time').temperature.plot(
    marker= 'o', markersize = 5, lw =0, 
 alpha = .3, legend = False)
   
plt.text(
    x[0], 0,
    '$y \;=\; %.1f\,\sin(2\pi/%.2f\cdot(x %s %.2f)) + %.1f$'
    % (p[0], T, '-' if p[2]>0 else '+', abs(p[2]), p[3])
    )
                         
plt.xlabel('time (30 mins)')
plt.ylabel('temperature(degrees celcius)')
plt.show()

#residuals 
resid = df.set_index('time').temperature-sin(x, *p)
resid = resid.reset_index()

resid.set_index('time').temperature.plot(
    marker = 'o', markersize = 5, lw = 0, 
    alpha = .3, legend = False)
plt.xlabel('time')
plt.ylabel('residual (degrees celcius')
plt.show()

ptsperday=48
def dayfinder(df, ptsperday):
    day=[]
    for t in df['time']:
        day.append(int(t/ptsperday))
        df.insert(2, 'day', day, True)
        return yearfinder(df)

def yearfinder(df):
    year = []
    for d in df['day']:
        year.append(int(d/365))
    df.insert(3, 'year', year, True)
    return df

df=dayfinder(df, ptsperday)
    
    
    
