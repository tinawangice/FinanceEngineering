from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import seaborn as sns


quote = pd.read_csv('quote.csv')
trade = pd.read_csv('trade.csv')
trade['pre_price']=trade['PRICE'].shift(1)
trade['diff']=trade['PRICE']-trade['pre_price']

trade['TIME_M'] = pd.to_datetime(trade['TIME_M']) + pd.DateOffset(days=-755)


def interval_cov(trade,day=20160104, a='2016-01-04 10:10:00', b= '2016-01-04 10:40:00'):
    df = trade.loc[(trade['DATE'] == day)]
    print("df is \n\n")
    print(df.head(20))
    print("df is \n\n")
    if pd.to_datetime(a)< min(df['TIME_M']) or pd.to_datetime(b) > max(df['TIME_M']):
        return None
    else:
        temp = df.loc[(df['TIME_M']>=pd.to_datetime(a))&(df['TIME_M']<=pd.to_datetime(b))\
            &(df['DATE']==day)][['TIME_M','diff']]
        print(temp)
        cov= np.cov(temp.iloc[0:-1,-1],temp.iloc[1:,-1])[0][1]
        star_cov = 2*((abs(cov))**0.5)
        print("cov=",cov)
        print("2*sqrt(-cov):",star_cov)
        return(star_cov)

quote['TIME_M'] = pd.to_datetime(quote['TIME_M']) + pd.DateOffset(days=-755)

def interval_spread(quote, day=20160104, a='2016-01-04 10:10:00', b= '2016-01-04 10:40:00'):
    df = quote.loc[(quote['DATE'] == day)]
    if pd.to_datetime(a)< min(df['TIME_M']) or pd.to_datetime(b) > max(df['TIME_M']):
        return None
    else:
        temp = df.loc[(df['TIME_M'] >= pd.to_datetime(a)) & (df['TIME_M'] <= pd.to_datetime(b))\
            &(df['ASK']>0)&(df['BID']>0)&(df['DATE']==day)][['TIME_M', 'BID','ASK']]
        temp['spread']= temp['ASK']-temp['BID']
        print(temp.head())
        return(temp)

def compare_s_cov(quote,trade,day0=20160104, a0='2016-01-04 10:10:00', b0= '2016-01-04 10:40:00'):
    star_cov = interval_cov(trade, day= day0, a=a0, b=b0)
    temp = interval_spread(quote,day= day0, a=a0, b=b0)

    """
    UNCOMMENT FOLLOWING CODES IF NEED OUTPUT THE GRAPH & THE RATIO OF SPREAD IN (0.5*STAR_COV, 1.5*STAR_COV)
    IF UNCOMMENT, CHANGE RETURN, ADD RATIO
    """
    # count =0
    # for i in range(len(temp['spread'])):
    #     if temp.iloc[i,-1]>star_cov*0.5 and temp.iloc[i,-1]<star_cov*1.5:
    #         count+=1
    # plt.axvline(star_cov,color='k')
    # pd.Series(temp['spread']).plot(kind='density')
    # plt.legend(['2*sqrt(-cov)', 'PDF of spread'])
    # plt.suptitle('Transact_time Comparasion during %s to %s' %(a0,b0), fontsize=16)
    # plt.show()
    # ratio = count/ len(temp['spread'])
    # print("ratio=",ratio)
    return star_cov, temp['spread'].tolist()

def get_timelist(start='2016-01-04 10:00:00', interval_min = 30):
    a = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    timelist =[str(a)]
    for i in range(12):
        a += datetime.timedelta(minutes=interval_min)
        timelist.append(str(a))
    return timelist

star_cov=[]
spread =[]
timelist04 = get_timelist(start='2016-01-04 10:00:00', interval_min = 30)
for i in range(len(timelist04)-1):
    a, b = compare_s_cov(quote, trade, 20160104, timelist04[i], timelist04[i + 1])
    star_cov.append(a)
    spread.append(b)

print(spread)
print(star_cov)

df04 = pd.DataFrame(columns=['time_start','time_end','spread_mean','star_cov'])
df04['time_start']= timelist04[:-1]
df04['time_end'] = timelist04[1:]
df04['spread_mean'] = spread
df04['star_cov']= star_cov

df04.to_csv('spread20160104.csv', sep='\t')



