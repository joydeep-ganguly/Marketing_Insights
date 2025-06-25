import streamlit as st
import pandas as pd
import numpy as np

def get_purc_days(x):
    temp = df[(df.CustomerID==x['CustomerID']) & (df.Transaction_Date!=x['Transaction_Date'])]\
    [['CustomerID','Transaction_Date','Coupon_Status','Product_Category']]
    next_days=used=clicked=notused=0
    most_bought=''
    if temp.shape[0] > 0:
        next_days = temp['Transaction_Date'].nunique()

        dt = dict(temp.Coupon_Status.value_counts())
        used = dt['Used'] if 'Used' in dt else 0
        clicked = dt['Clicked'] if 'Clicked' in dt else 0
        notused = dt['Not Used'] if 'Not Used' in dt else 0

        most_bought = temp['Product_Category'].mode()[0]
    return pd.Series([next_days,used,clicked,notused,most_bought])

def md(x):
  return pd.Series.mode(x)[0]

df = st.session_state.datakey
st.subheader('Cohort Analysis')
st.html('<strong>Customers behavior who stared in each month</strong>')

df_cohort = pd.DataFrame(df.Transaction_Date.groupby(df.CustomerID).min()).reset_index()
df_cohort['MonthName'] = df_cohort['Transaction_Date'].dt.month_name()
df_cohort['Month'] = df_cohort['Transaction_Date'].dt.month
df_cohort.head()
df_start = df_cohort.iloc[::]
df_cohort[['next_days','used','clicked','notused','most_bought']] = df_cohort.apply(lambda x: get_purc_days(x),axis=1)
df_cohort['returned'] = df_cohort['next_days'].apply(lambda x: 1 if x>0 else 0)
df_cohort = df_cohort.groupby(['Month','MonthName'])\
.agg({'next_days':'sum','used':'sum','clicked':'sum','notused':'sum','returned':'sum'})
df_cohort.reset_index(inplace=True)
st.write(df_cohort.iloc[:,1:])

st.html('<strong>Maximum retentions based on cohort month</strong>')
df_start = pd.DataFrame(df_start.groupby(['Month','MonthName'])['CustomerID'].count()).reset_index()
df_start.columns=['Month','MonthName','Joined']
df_cohort = df_cohort.merge(df_start,how='inner')
df_cohort['Retained'] = df_cohort['Joined'] - df_cohort['returned']
df_cohort.sort_values('Retained',ascending=False)[['MonthName','Retained']]
