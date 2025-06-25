import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = st.session_state.datakey
segtype = st.sidebar.radio('Type of segmentation',['Value','RFM'])

if segtype == 'Value':
  st.subheader("Customer Segmentation : Value Based")

  range0 = 0
  range1 = st.slider('1st Range',25,100,50)
  range2 = st.slider('2nd Range',101,200,150)
  range3 = st.slider('3rd Range',201,500,300)
  range4 = np.inf

  cusval = df[['CustomerID','Invoice_Value']]
  #mbins = [0,50,150,300,np.inf]
  mbins = [range0,range1,range2,range3,range4]
  mlabels = ['Standard','Silver','Gold','Premium']
  cusval['binned'] = pd.cut(df.Invoice_Value,bins=mbins,labels=mlabels)
  cusval = pd.DataFrame(cusval.binned.value_counts()).reset_index()

  fig,ax = plt.subplots(figsize=(9,5))
  ax.pie(cusval['count'], labels=mlabels, autopct='%1.1f%%')
  ax.axis('equal')
  st.pyplot(fig)
else:
  st.subheader("Customer Segmentation : RFM Based")

  mlabels = ['Standard','Silver','Gold','Premium']

  df_recency = pd.DataFrame(df.groupby(by='CustomerID')['Transaction_Date'].max()).reset_index()
  df_recency.columns=['Customer','LastPurchaseDate']
  recent_date= df_recency.LastPurchaseDate.max()
  df_recency['Recency'] = df_recency.LastPurchaseDate.apply(lambda x: (recent_date-x).days)
  df_recency.drop(columns='LastPurchaseDate',inplace=True)
  df_frequency = pd.DataFrame(df.groupby(by='CustomerID')['Transaction_ID'].count()).reset_index()
  df_frequency.columns=['Customer','Frequency']
  df_monetary = pd.DataFrame(df.groupby(by='CustomerID')['Invoice_Value'].sum()).reset_index()
  df_monetary.columns=['Customer','Monetary']
  df_rfm = df_recency.merge(df_frequency).merge(df_monetary)

  df_rfm['r_rank'] = df_rfm['Recency'].rank(ascending=False)
  df_rfm['f_rank'] = df_rfm['Frequency'].rank(ascending=True)
  df_rfm['m_rank'] = df_rfm['Monetary'].rank(ascending=True)
  df_rfm['r_rank_norm'] = (df_rfm['r_rank']/df_rfm['r_rank'].max())*100
  df_rfm['f_rank_norm'] = (df_rfm['f_rank']/df_rfm['f_rank'].max())*100
  df_rfm['m_rank_norm'] = (df_rfm['m_rank']/df_rfm['m_rank'].max())*100
  df_rfm['rfm_score'] = (df_rfm['r_rank_norm']+df_rfm['f_rank_norm']+df_rfm['m_rank_norm'])/3
  df_rfm.drop(columns=['r_rank','f_rank','m_rank'],inplace=True)

  cusrfm = df_rfm[['Customer','rfm_score']]
  
  range0 = 0
  range1 = st.slider('1st Range',10,40,30)
  range2 = st.slider('2nd Range',31,75,60)
  range3 = st.slider('3rd Range',76,95,90)
  range4 = cusrfm.rfm_score.max()
  #rfmbins = [0,10,25,50,cusrfm.rfm_score.max()]
  rfmbins = [range0,range1,range2,range3,range4]
  rfmlabels = ['Standard','Silver','Gold','Premium']
  cusrfm['binned'] = pd.cut(cusrfm['rfm_score'],bins=rfmbins,labels=rfmlabels)
  cusrfm = pd.DataFrame(cusrfm.binned.value_counts()).reset_index()

  fig,ax = plt.subplots(figsize=(9,5))
  ax.pie(cusrfm['count'], labels=cusrfm['binned'], autopct='%1.1f%%')
  ax.axis('equal')
  st.pyplot(fig)

  st.html('<strong>RFM Score</strong>')
  st.write(df_rfm[['Customer','rfm_score']])