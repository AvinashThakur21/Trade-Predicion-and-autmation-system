from django.shortcuts import render
from  .functions import get_data, candle_diff, demand_zone_locator, index_to_price, trade_test, pl_summery, get_data2, check_trade_status2

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


# 20 script get all zone from 1 april 2024
scripts = ['INFY.NS','TCS.NS','360ONE.NS', '5PAISA.NS', 'AARTIDRUGS.NS', 'AARTIIND.NS', 'AARTIPHARM.NS',
          'AARTISURF.NS', 'AAVAS.NS', 'ABSLAMC.NS', 'ACC.NS', 'ACCELYA.NS', 'ACE.NS', 
           'ACI.NS', 'ADANIENSOL.NS', 'ADANIENT.NS', 'AETHER.NS', 
           'ADANIPORTS.NS', 'ADANIPOWER.NS', 'ADORWELD.NS', 'AEGISCHEM.NS']

def give_me_zone(request):

        
    all_stock_result = []
    for script in scripts:
        script = script.split('.')[0]
        print(script.upper(),end='\t')
        df = get_data2(script +'.NS','2023-04-01',1) # script
        df = candle_diff(df)
        df.reset_index(inplace=True)
        
        
        all_zone_index = demand_zone_locator(df)
        #all_zone,fig = plot_zone(df,all_zone_index)
        all_zone = index_to_price(df,all_zone_index)
        
        
        all_trade_result = []
        for trade in all_zone:
            trade_result = check_trade_status2(trade)
            all_trade_result.append(trade_result)
        #print(all_trade_result)
        all_stock_result.append([script,all_trade_result])
    context= dict(all_stock_result)
    print(context)
    return render(request,'home.html',{'context': context})
''' context list like this
{'INFY': [[1379.8, 1361.0, 1398.6, '2023-11-09', '2023-11-15', 0, '0', '0', 0],
  [1293.3, 1262.2, 1324.4, '2023-06-23', '2023-06-30', 0, '0', '0', 0],
  [1228.1, 1215.0, 1241.2, '2023-04-20', '2023-04-27', 0, '0', '0', 0]],
 'TCS': [[... so on 
'''