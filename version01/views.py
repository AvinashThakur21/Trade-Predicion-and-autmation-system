from django.shortcuts import render
from  .functions2 import self_get_data, self_candle_diff, self_demand_zone_locator,   self_check_trade_status

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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render




def home(request):
    context = {'a':1, 'b':2}
    return render(request,'home.html',context)


# 20 script get all zone from 1 april 2024
scripts = ['INFY.NS','TCS.NS','360ONE.NS', '5PAISA.NS', 'AARTIDRUGS.NS', 'AARTIIND.NS', 'AARTIPHARM.NS',
          'AARTISURF.NS', 'AAVAS.NS', 'ABSLAMC.NS', 'ACC.NS', 'ACCELYA.NS', 'ACE.NS', 
           'ACI.NS', 'ADANIENSOL.NS', 'ADANIENT.NS', 'AETHER.NS', 
           'ADANIPORTS.NS', 'ADANIPOWER.NS', 'ADORWELD.NS', 'AEGISCHEM.NS']

some_scripts = [ 'AAVAS.NS', 'ABSLAMC.NS']

@login_required
def give_me_zone(request,section):
    overall_list = []
        
    all_stock_result = []
    all_history_trade = []
    all_open_trade = []
    all_upcoming_trade =[]
    for script in some_scripts:

        try:
            script =  script.split('.')[0]
            print(script.upper(),end='\t')
            row_df = self_get_data(script,(2015,4,1),(2024,4,1)) # script
            df = self_candle_diff(row_df)
            all_zone ,all_zone_index = self_demand_zone_locator(df,zone_count=5)
        
            all_results = []
            for zone in all_zone:
                result = self_check_trade_status( script,zone)
                all_results.append(result)
        
        
            
            all_stock_result.append([script,all_results])
        except:
            print("**********")
            #overall_list.append(['*****'])
        print()
        
        
   
        history_trade = []
        open_trade = []
        upcoming_trade =[]
  
       
            
        #print(all_trade_result)
        for trade in all_results:
            if trade[6] == 0 :
                upcoming_trade.append(trade)
            elif trade[6] == 1:
                open_trade.append(trade)
            else:
                history_trade.append(trade)


        all_stock_result.append([script,all_results])
        all_upcoming_trade.append([script,upcoming_trade])
        all_open_trade.append([script,open_trade])
        all_history_trade.append([script,history_trade])

    # filter value based on close , open, upcoming 
    if section == 'open':
        context= dict(all_open_trade)
    elif section == 'history':
        context= dict(all_history_trade)
    elif section == 'upcoming':
        context= dict(all_upcoming_trade)
    
    print(context)
    return render(request,'home.html',{'context': context})
''' context list like this
{'INFY': [[1379.8, 1361.0, 1398.6, '2023-11-09', '2023-11-15', 0, '0', '0', 0],
  [1293.3, 1262.2, 1324.4, '2023-06-23', '2023-06-30', 0, '0', '0', 0],
  [1228.1, 1215.0, 1241.2, '2023-04-20', '2023-04-27', 0, '0', '0', 0]],
 'TCS': [[... so on 
'''