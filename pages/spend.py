import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.subheader("Marketing Spend")
df = st.session_state.datakey
ms = st.session_state.mskey
#ms = pd.read_csv('Marketing_Spend.csv')
#ms['Date'] = pd.to_datetime(ms.Date,format='%m/%d/%Y')

msmonth = ms[['Date','Online_Spend']]
msmonth['Month'] = msmonth.Date.dt.month
msmonth = msmonth.groupby('Month')['Online_Spend'].sum()
msmonth = pd.DataFrame(msmonth).reset_index()
msmonth = ms[['Date','Online_Spend']]
msmonth['Month'] = msmonth.Date.dt.month
msmonth = msmonth.groupby('Month')['Online_Spend'].sum()
msmonth = pd.DataFrame(msmonth).reset_index()
ed08 = pd.DataFrame(df.groupby('Month')\
.agg({'Invoice_Value':'sum'})).reset_index()
ed08 = ed08.merge(msmonth,how='left')
ed08['Spend_to_Revenue_Ratio'] = (ed08.Online_Spend/ed08.Invoice_Value)*100
fig,ax = plt.subplots(figsize=(6,4))
sns.barplot(data=ed08,x='Month',y='Spend_to_Revenue_Ratio')
ax.set_title('Spend Ratio Monthwise')
st.pyplot(fig)

ed09 = df[['Transaction_Date','Invoice_Value']]

ed09 = pd.DataFrame(ed09.groupby(by='Transaction_Date')['Invoice_Value'].sum()).reset_index()
ed09 = ed09.merge(ms,left_on='Transaction_Date',right_on='Date',how='left')
ed09['DayOfYear'] = ed09.Transaction_Date.dt.dayofyear
ed09.drop(columns=['Date','Offline_Spend','Transaction_Date'],inplace=True)

fig,ax = plt.subplots(figsize=(6,4))
sns.scatterplot(data=ed09,x='Invoice_Value',y='Online_Spend')
ax.set_title('Effect of Marketing on Daily Sales')
st.pyplot(fig)

