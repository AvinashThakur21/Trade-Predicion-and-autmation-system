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


# get data for given stock form start year till end year 
# return dataframe with col  -   Date ( as index ) Open 	High 	Low 	Close
def get_data(stock_symbol,start_year,end_year=0):
    
    if end_year == 0:
        end = dt.datetime.now()
    else:
        end = dt.datetime(end_year,1,1)
    start = dt.datetime(start_year,1,1)
    yfin.pdr_override()
    df = pdr.get_data_yahoo(stock_symbol, start, end)
    df.head(2)
    
    df = df.iloc[:,0:4]
    for col in df.columns:
        df[col] = df[col].round(1)
    return df

def get_data2(stock_symbol,start_date,next_year): # end_date

    print(start_date)
    year,month,date = [int(x)for x in  '2023-04-01'.split('-')] # start_date
    start_date = dt.datetime(year,month,date)
    
    #year,month,date = [int(x)for x in start_date.split('-')] # to use end date date change start_date to end_date and remove +1 in year next line
    end_date = dt.datetime(year+next_year ,month,date)   # currently next 1 year from start date , 
    
    yfin.pdr_override()
    df = pdr.get_data_yahoo(stock_symbol, start_date, end_date)
    
    #print(df.shape)
    df = df.iloc[:,0:4] 
    for col in df.columns:
        df[col] = df[col].round(1)
    return df


def check_trade_status2(trade_list):
    
    updated_trade_list= []
    updated_trade_list = [x for x in trade_list]
    entry, stoploss, target, legin_date, legout_date =  tuple(trade_list)
    start_date = legout_date
    
    df2 = get_data2('tcs.ns',start_date,1)
    df2 = df2.iloc[1:,:]
    df2.reset_index(inplace=True)
    
    for i in range(df2.shape[0]):
        candle = df2.iloc[i,:]
        candle_low = int(candle.loc['Low'])
        candle_high = int(candle.loc['High'])
        candle_open = int(candle.loc['Open'])
        candle_close = int(candle.loc['Close'])
        is_entry = False
        status = 0 # upcoming 
        entry_date = 0
        exit_date = 0
        
        # entry and stoploss by same candle logic
        if ( candle_low < entry ) & ( candle_low < stoploss ) & ( is_entry == False) :
            status = 2 # sl
            entry_date = candle.loc['Date']
            exit_date = candle.loc['Date']
            break

        # entry logic
        elif (candle_low  <= entry) & ( is_entry == False ):
            is_entry = True
            status = 1
            entry_date = candle.loc['Date']
             
        # stoploss
        elif candle_low <= stoploss:
            status = 2
            exit_date = candle.loc['Date']
            break

        # target
        elif (candle_high >= target) & (is_entry == True):
            
            status = 3
            exit_date = candle.loc['Date']
            net_pnl
            break
            
    net_pnl = 0 
    capital = 100000 

    quantity = 1000/( entry - stoploss )
    afordabel_qun = capital/entry
    buy_qun = round(min(quantity, afordabel_qun))
    if (status == 2) :
        net_pnl -= 1000
    
    elif status ==3 :
        net_pnl = round(buy_qun * ( target - entry ),1)

    
    updated_trade_list.extend([ buy_qun,status,str(entry_date),str(exit_date),net_pnl])
    return updated_trade_list



def candle_diff(df):
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

def demand_zone_locator(df):
    # currently not checking last candle is zone or not
    all_zone = []
    
    # last candle low in proximal 
    proximal = int(df.iloc[-1,:].loc['Low'])
    
    previous_candle_index = df.shape[0]-2
    while previous_candle_index != 0 :
        #print(previous_candle_index)
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
                all_zone.append(zone)
                leg_in_index = zone[0] 
                base_index = zone[1]
                leg_out_index = zone[2]
                proximal = df.loc[leg_in_index:leg_out_index,'Low'].min()
                #print(proximal)
                previous_candle_index = leg_in_index - 1
                
            else:
                proximal = int(previous_low)

        # while loop update 
        if zone == [] :
            previous_candle_index = previous_candle_index -1
    return all_zone

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


# zone is all zone list 0 is closest zone to cmp 
# zone = [entry,sl,target_price]
def trade_test(test_df,all_zone,target_x):
    i=0
    j = 0 
    is_completed = False
    all_results = []
    for zone in all_zone:
        #print(zone,end='\t') #************** active print
        i=j
        #print("i------>",i)
        entry = zone[1]
        stoploss = zone[0]
        target = entry + ( target_x * zone[2] )
        is_entry = False
        for next_candle_index in range(i,test_df.shape[0]):
            
            next_candle = test_df.iloc[next_candle_index]
            candle_low = int(next_candle.loc['Low'])
            candle_high = int(next_candle.loc['High'])
            candle_open = int(next_candle.loc['Open'])
            candle_close = int(next_candle.loc['Close'])
            #print(candle_low,end='\t')
            
            if ( candle_low < entry ) & ( candle_low < stoploss ) & ( is_entry == False) :
                #print(f"Entry \tStoploss -------> - {entry - stoploss}") #************** active print
                all_results.append([entry,stoploss,target,'SL'])
                j = next_candle_index
                #print("i------------->",i)
                break
            elif (candle_low  <= entry) & ( is_entry == False ):
                is_entry = True
                #print("Entry  ",end="\t") #**********active 
                #print('Target--->',target)
                

            elif candle_low <= stoploss:
                #print(f"StopLoss -------> - {entry - stoploss}") #************* active print 
                j = next_candle_index
                all_results.append([entry,stoploss,target,'SL'])
                #print("i------------->",i)
                break
            elif (candle_high >= target) & (is_entry == True):
                #print(f"Target ---------> + {target - entry }")
                j = next_candle_index
                all_results.append([entry,stoploss,target,'TR'])
                break
            
            if next_candle_index == ((test_df.shape[0])-1):
                
                is_completed = True
                #print("Working")
                break
        if is_completed :
            #print("All candle done")
            break
            
    return all_results
        
        
def pl_summery(all_results):
    loss = 0
    profit = 0 
    capital = 100000

    
    for result in all_results:
        if result[3] == 'SL':
            loss -= 1000
        else:
            entery = result[0]
            stoploss = result[1]
            target = result[2]
            
            quantity = 1000/( entery - stoploss )
            afordabel_qun = capital/entery
            buy_qun = min(quantity, afordabel_qun)

            profit = profit + (buy_qun * ( target - entery ))
    return loss,profit 
    
    

















