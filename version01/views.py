from django.shortcuts import render
from  .functions import get_data, candle_diff, demand_zone_locator, index_to_price, trade_test, pl_summery
# Create your views here.

import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import plotly.offline as pyo
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yfin

# graph primary setting 
pyo.init_notebook_mode(connected=True)
pd.options.plotting.backend = 'plotly'












def home(request):
    context = {'a':1, 'b':2}
    return render(request,'home.html',context)


def give_me_zone(request):

    overall_results = []
    script= 'tcs.ns'


    print(script,end='\t')
        
    df = get_data(script,1990,2022)
    
    df = candle_diff(df)
    df.reset_index(drop=True, inplace=True)
    all_zone_index = demand_zone_locator(df)
    
    #all_zone,fig = plot_zone(df,all_zone_index)
    all_zone = index_to_price(df,all_zone_index)
    for i in all_zone:
        
        i[2] = round(float(i[2]),2)
    
    train_candles = df.shape[0]
    
    # deploydataset
    df =get_data(script,2022,2024)
    
    df = candle_diff(df)
    df.reset_index(drop=True, inplace=True)
    df.index = range(train_candles, train_candles + len(df))
    
    #update_fig(fig,index,open,high,close,low)
    
    all_results = trade_test(df,all_zone,3)
    
    loss,profit   = pl_summery(all_results)
    #loss,profit   = (10,20)

    overall_results.append([script,loss,profit])
    print(loss,profit)





    data = {}  # Initialize an empty dictionary

    # Define your keys and values
    keys = [script.split('.')[0]]
    #ids = ['01id', '02id', '03id']
    #values = [[1, 2, 3] for _ in range(len(ids))]  # Example values, you can replace this with your actual data

    # Loop to populate the dictionary
    for key in keys:
        data['script'] = script 
        data[key] = {}  # Initialize nested dictionary for each key
        for i in range(len(all_zone)):
            entry= all_zone[i][1]
            sl = all_zone[i][0]
            target = entry+ all_zone[i][2] 
            data[key][key + str(i)] = [entry,sl,target]

    
    print(data)
    return render(request,'home.html',context= data)
