import streamlit as st
import numpy as np
import pandas as pd

def op_cust(df):
    opcus = df[['Transaction_Date','Month','CustomerID','Tenure_Months']]
    opcus = opcus.assign(Occurance=np.where(~df['CustomerID'].duplicated(),'New','Existing'))
    opcus = opcus[(opcus.Occurance=='New') & (opcus.Month==1) & (opcus.Tenure_Months>12)]
    return opcus.shape[0]

def cus_monthly(df,opcus_shape):
    ed01 = df[['Transaction_Date','Month','CustomerID']]
    ed01= ed01.assign(Occurance=np.where(~df['CustomerID'].duplicated(),'New','Existing'))
    ed01 = ed01[ed01.Occurance=='New']
    ed01 = ed01.groupby('Month')['CustomerID'].nunique()
    ed01 = pd.DataFrame(ed01)
    ed01.columns=['Customers_Acquired']
    ed01.iloc[0,0]= ed01.iloc[0,0] - opcus_shape
    return ed01

data = st.session_state.datakey
st.title('Customer Behaviour Data')
st.markdown(''':red[This is a streamlit app.]''')

opcus = op_cust(data)
st.write(f'Available samples : {data.shape[0]}    |    Opening Customers : {opcus}')
cus_acquired = cus_monthly(data,opcus)
st.html('<strong>Mothwise Customer Aquisition</strong>')
st.line_chart(cus_acquired,x_label='Month',y_label='Customers Acquired')