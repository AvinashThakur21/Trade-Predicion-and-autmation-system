import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import plotly.offline as pyo
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yfin
import numpy as np
import datetime as dt
# graph primary setting 
pyo.init_notebook_mode(connected=True)
pd.options.plotting.backend = 'plotly'


# get data for given stock form start year till end year 
# return dataframe with col  -   Date ( as index ) Open 	High 	Low 	Close
# function NO/ ID - 01 
def self_get_data(stock_name,start_date,end_date): #=(2030,12,1)
    if type(start_date) == tuple:
            start_date = dt.datetime(*start_date) # input tuple to datetime object
            end_date = dt.datetime(*end_date)
    yfin.pdr_override()
    stock_symbol = stock_name + '.NS'
    df = pdr.get_data_yahoo(stock_symbol, start_date, end_date)
    df.reset_index(inplace=True)
    df = df.iloc[:,0:5] # open , high , low , close removing volume
    for col in df.drop('Date',axis=1).columns:
        df[col] = df[col].round(1)
    return df
    

# function ID 02 
def self_candle_diff(df):
    candle_type = []
    
    # to check candle is green or red and type of candle base,normal, exciting 
    def check_lable(open,high,low,close):

        if open < close :
            lable = "Green"
        else: 
            lable = "Red"
                    
        return lable
    
        
    def check_lable_intencity(open,high,low,close):
        
        body_margin = abs(open - close)
        body_persent = body_margin/ (abs( low - high )-0.00001)
        current_cmp = high/1000
        
        # ------->  find logic for base in %( cmp 0.1%<body margin   & body < 50 %)
        # if margin < 0.25% then candle must be base candle   1235.0 	1239.6 	1203.7 	1208.8 	
        if body_margin < (2.5 * ( high/1000)) :
            lable_type = "Base"

        # if margin > 0.25% then candle must be explosive candle 
        elif body_margin > (5.5 * ( high/1000)) :
            lable_type = "Explosive"
            
        else :
            lable_type = "Normal"
    
        return lable_type
            
    candle_lable = []
    candle_lable_intencity = []
    for i in df.index:
        candle_lable.append(check_lable(df['Open'][i],df['High'][i],df['Low'][i],df['Close'][i]))
        candle_lable_intencity.append(check_lable_intencity(df['Open'][i],df['High'][i],df['Low'][i],df['Close'][i]))

        
    candle_lable_ser = pd.Series(candle_lable)
    candle_lable_intencity_ser = pd.Series(candle_lable_intencity)
    df['candle_lable'] = candle_lable_ser.values
    df['candle_lable_intencity'] = candle_lable_intencity_ser.values
    
    df['is_explosive'] = df['candle_lable_intencity'] == "Explosive" 
    
    return df

# ****************
def check_zone(df,all_zone,i):
    is_green_exp = (df.iloc[i].loc['candle_lable'] == "Green")  & (df.iloc[i].loc['is_explosive'] == True )
        
    # only greeen explosive go inside 
    if is_green_exp == True:
        base = False
        leg_in = False
        for j in range(1,7):
            
            if  base == False:
                base_index = i-j
                base = df.iloc[i-j].loc['is_explosive'] == False
                if base == False:
                    break
                
            if base == True:
                leg_in_index = i -j
                leg_in = df.iloc[i-j].loc['is_explosive'] == True
            if leg_in:
                break
        if base & leg_in:
            
            
            leg_out_index = i
            #print( base_index,"<--base, legin-->" , leg_in_index,"legout-->",i)
            
            #print(zone)
            return [leg_in_index,base_index,leg_out_index]
        else: 
            
            return []
    
    return []

# update - add all zone index list , date , of entry and exit candle 
def self_demand_zone_locator(full_df,date=None,zone_count=1000,): # plot_zone = False, add in new update 
    # currently not checking last candle is zone or not
    all_zone = []
    if date == None:
        start_date = full_df.iloc[-1]['Date']
    else:
        start_date = datetime.datetime(*date)
        
    df = full_df.iloc[:full_df[full_df['Date'] == start_date].index[0],:] # find zone from this date 
    # last candle low in proximal 
    proximal = int(df.iloc[-1,:].loc['Low'])
    
    previous_candle_index = df.shape[0]-2
    while previous_candle_index != 0 :
        #print(previous_candle_index)
        # break if zone 
        if len(all_zone) >= zone_count:
            break
            
        zone = []
        previous_candle = df.iloc[previous_candle_index,:]
        # numpy.float64 to int( floor value) so we can use in range
        previous_low = int(previous_candle.loc['Low'])
        previous_high = int(previous_candle.loc['High'])
        previous_open = int(previous_candle.loc['Open'])
        previous_close = int(previous_candle.loc['Close'])

        #print(type(previous_low),type(proximal))
        if previous_low > proximal:
            pass

        elif (previous_low < proximal) & ( proximal in range(previous_open,previous_low)):
            proximal = previous_low

        else:
            zone = check_zone(df,all_zone,previous_candle_index) # return  legin , base , legout index

            
            
            
            # all_zone in list with new zone, zone details [leg_in_index,base_index,leg_out_index]
            if zone != [] :
                
                leg_in_index = zone[0] 
                base_index = zone[1]
                leg_out_index = zone[2]

                # appending legin and legout date in zone 
                leg_in_date = str(df.iloc[leg_in_index]['Date']).split(' ')[0] # keeping only date , removing time 
                leg_out_date = str(df.iloc[leg_out_index]['Date']).split(' ')[0]
                zone.append(leg_in_date)
                zone.append(leg_out_date)

                all_zone.append(zone)
                proximal = df.loc[leg_in_index:leg_out_index,'Low'].min()
                #print(proximal)
                previous_candle_index = leg_in_index - 1
                
            else:
                proximal = int(previous_low)

        # while loop update 
        if zone == [] :
            previous_candle_index = previous_candle_index -1
    all_zone_price = index_to_price(df,all_zone)
    return all_zone_price,all_zone # all zone price and index


# update - to [ entry, stoploss, target_price, legin,legout_date]

# ********
def index_to_price(df,all_zone):
    
    
    dart_list = []
    for i in range(len(all_zone)):
        legin = all_zone[i][0]
        legout = all_zone[i][2] 
     
        lower_wick1 = df.iloc[all_zone[i][1]]['Low']
        upper_body1 = df.iloc[all_zone[i][1]]['Close']
         
        for j in range(legin+1,legout):
            upper_body2 = df.iloc[j]['Close']
            upper_body3 = df.iloc[j]['Open']
            upper_body2 = max(df.iloc[j]['Open'],df.iloc[j]['Close'])
            lower_wick2 = df.iloc[j]['Low']
            if lower_wick1 > lower_wick2:
                lower_wick1 = lower_wick2
            if upper_body2 > upper_body1:
                upper_body1 = upper_body2
    
        target = upper_body1 + (upper_body1 - lower_wick1 )
        target = round(target,1)
        dart_list.append([upper_body1,lower_wick1, target,all_zone[i][-2],all_zone[i][-1]])
   
        
    return dart_list


def self_check_zone_trend(zone,plot_graph=True): # data shape must be more then 100 rows
    legout_date = zone[4]
    # get data from 5 month before , till legout date 
    import datetime as dt
    from dateutil.relativedelta import relativedelta
    from datetime import datetime, timedelta
    legout_date = tuple([int(x)for x in legout_date.split('-')])
    legout_date = dt.datetime(*legout_date)
     
    # Calculate the date and time five months before the current date and time
    five_months_before = legout_date - relativedelta(months=5)
    
    #print("Current date and time:", legout_date)
    #print("Date and time five months before:", five_months_before)


    ##### 
    
    row_df =self_get_data(script,five_months_before,legout_date + timedelta(days=1))

    df = self_candle_diff(row_df)

    all_zone_price = self_demand_zone_locator(df)
    
    # get last 100 rows from legout candle by date 
    #print(legout_date)
    current_zone_index = df[df['Date'] == legout_date].index[0]
    #print(legout_index)
    #input_df = df.iloc[legout_index-99:legout_index+1,:]['Close']
    input_df = df.iloc[current_zone_index-99:current_zone_index+1,:]['Close']
    
    from sklearn.preprocessing import MinMaxScaler # scaling not proper may be keep eye
    scaler=MinMaxScaler(feature_range=(0,1))
    #input_df['Close'] = input_df['Close'] #.astype(numpy.int64)
    #print( input_df['Close'])
    input_df=scaler.fit_transform(np.array(input_df).reshape(-1,1))
    test_data = input_df
    from keras.models import load_model
    model= load_model('yt_nextdays.keras')
    x_input = test_data.reshape(1,-1)
    temp_input=list(x_input)
    temp_input=temp_input[0].tolist()
    
    # demonstrate prediction for next 10 days
    from numpy import array
    
    lst_output=[]
    n_steps=100
    i=0
    while(i<10):
    
        if(len(temp_input)>100):
            #print(temp_input)
            x_input=np.array(temp_input[1:])
            #print("{} day input {}".format(i,x_input))
            x_input=x_input.reshape(1,-1)
            x_input = x_input.reshape((1, n_steps, 1))
            #print(x_input)
            yhat = model.predict(x_input, verbose=0)
            #print("{} day output {}".format(i,yhat))
            temp_input.extend(yhat[0].tolist())
            temp_input=temp_input[1:]
            #print(temp_input)
            lst_output.extend(yhat.tolist())
            i=i+1
        else:
            x_input = x_input.reshape((1, n_steps,1))
            yhat = model.predict(x_input, verbose=0)
            #print(yhat[0])
            temp_input.extend(yhat[0].tolist())
            #print(len(temp_input))
            lst_output.extend(yhat.tolist())
            i=i+1
    
    #clear_output()
    #print(lst_output)

    day_new=np.arange(1,101)
    day_pred=np.arange(101,111)
    #y = len(df1) -100
    if plot_graph:
        import matplotlib.pyplot as plt
        # last 100 days close line blue color and predicted line in yellow 
        #plt.plot(day_new,scaler.inverse_transform(df1[y:]))
        plt.plot(day_pred,scaler.inverse_transform(lst_output))
        plt.plot(df.iloc[current_zone_index-99:current_zone_index+11,:]['Close'].reset_index().drop('index',axis=1))
        plt.show()
    #print(predicted_close_list)
    #print(zone)
    predicted_close = scaler.inverse_transform(lst_output)[-10:]
    #print(predicted_close)
    #print(zone)
    if zone[1] >= predicted_close[-1][0]:
        return 0
    return 1



def self_check_trade_status(stock_name,trade_list):
    # print('trade-->',trade_list)
    updated_trade_list= []
    updated_trade_list = [x for x in trade_list]
    entry, stoploss, target, legin_date, legout_date =  tuple(trade_list)
    #start_date = legout_date

    start_date = tuple([int(x)for x in legout_date.split('-')])
    start_date = dt.datetime(*start_date)

    end_date = dt.datetime(*(2030,12,30)) # till now update leter 
    
    df2 = self_get_data(stock_name, start_date, end_date )
    #df2 = get_data2('tcs.ns',start_date,1)
    df2 = df2.iloc[1:,:]
    is_entry = False
    status = 0 # upcoming 
    entry_date = 0
    exit_date = 0
    
    for i in range(df2.shape[0]):
        candle = df2.iloc[i,:]
        candle_low = float(candle.loc['Low'])
        candle_high = float(candle.loc['High'])
        candle_open = float(candle.loc['Open'])
        candle_close = float(candle.loc['Close'])

        
        # entry and stoploss by same candle logic
        
        if ( candle_low < entry ) and ( candle_low < stoploss ) and ( is_entry == False) :
            # print('target',target)
            # print('1',candle)
            # print('stoploss',stoploss)
            # print('candle_low',candle_low)
            status = 2 # sl
            entry_date = candle.loc['Date']
            exit_date = candle.loc['Date']
            break

        # entry logic
        elif (candle_low  <= entry) and ( is_entry == False ):
            # print('Entry***********')
            # print('entry',candle)
            is_entry = True
            status = 1
            entry_date = candle.loc['Date']
             
        # stoploss
        elif candle_low <= stoploss:
            # print('sl',candle)
            status = 2
            exit_date = candle.loc['Date']
            break

        # target
        elif (candle_high >= target) and (is_entry == True):
            # print('target',candle)
            status = 3
            exit_date = candle.loc['Date']
            
            break


    net_pnl = 0 
    capital = 100000 

    quantity = 1000/( entry - stoploss )
    afordabel_qun = capital/entry
    buy_qun = round(min(quantity, afordabel_qun))
    if status == 2 :
        net_pnl -= 1000
    
    elif status ==3 :
        net_pnl = round(buy_qun * ( target - entry ),1)

    
    updated_trade_list.extend([buy_qun,status,str(entry_date),str(exit_date),net_pnl])
    return updated_trade_list

        

