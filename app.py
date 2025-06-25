import streamlit as st
import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

def get_ivalue(x):
    return ((x.Quantity*x.Avg_Price)*(1-x.Discount_pct)*(1+x.GST)) + x.Delivery_Charges

def prepare_data():
    cd = pd.read_excel('CustomersData.xlsx')
    dc = pd.read_csv('Discount_Coupon.csv')
    ms = pd.read_csv('Marketing_Spend.csv')
    ta = pd.read_excel('Tax_amount.xlsx')
    os = pd.read_csv('Online_Sales.csv')
    dc.columns = ['Month', 'Product_Category', 'Coupon_Code', 'Discount_pct']
    ms['Date'] = pd.to_datetime(ms.Date,format='%m/%d/%Y')
    os['Transaction_Date'] = pd.to_datetime(os['Transaction_Date'],format='%Y%m%d')
    os['Month'] = os.Transaction_Date.apply(lambda x: x.month_name()[:3])
    df = os.merge(cd,how='left').merge(ta,how='left').merge\
    (ms,how='left',left_on='Transaction_Date',right_on='Date').merge\
    (dc,how='left',left_on=['Month','Product_Category'],right_on=['Month','Product_Category'])
    df['Month'] = df.Transaction_Date.apply(lambda x: x.month)
    df['Discount_pct'].fillna(0,inplace=True)
    df.drop(columns=['Coupon_Code'],inplace=True)
    df.drop(columns=['Date','Offline_Spend'],inplace=True)
    df.Discount_pct = df.Discount_pct/100
    df['Invoice_Value'] = df.apply(lambda x : get_ivalue(x), axis=1)
    df['Tax_Amount'] = df.Invoice_Value * df.GST
    return df,ms

if 'datakey' not in st.session_state:
    data,mkt = prepare_data()
    st.session_state['datakey'] = data
    st.session_state['mskey'] = mkt
else:
    data = st.session_state['datakey']
    mkt = st.session_state['mskey']

page1 = st.Page('pages/Dashboard.py',title='Dashboard')
page2 = st.Page('pages/Revenue.py',title='Revenue')
page4 = st.Page('pages/Kpis.py',title='KPIs')
page5 = st.Page('pages/trends.py',title='Trends/Seasonality')
page6 = st.Page('pages/spend.py',title='Marketing Spend')
page7 = st.Page('pages/segment.py',title='Segmentation-Heuristic')
page8 = st.Page('pages/kmeans.py',title='Segmentation-KMeans')
page9 = st.Page('pages/crosseda.py',title='Cross Selling Products')
page10 = st.Page('pages/cohort.py',title='Cohort Analysis')
page99 = st.Page('pages/RawData.py',title='Raw Data')

pg = st.navigation([page1,page2,page4,page5,page6,page7,page8,page9,page10,page99])
st.set_page_config(page_title='Customer Behavior')
pg.run()