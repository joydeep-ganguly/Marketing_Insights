import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.subheader("KPIs")
df = st.session_state.datakey

option = st.radio(
    "Display results in the basis of:",
    [":rainbow[Category]", "***Month***", "Day of week"]
)

if option==':rainbow[Category]':
  ed05_1 = df.groupby(by='Product_Category').agg({'Invoice_Value':'sum','Transaction_ID':'count'\
  ,'Avg_Price':'sum','CustomerID':'nunique','Quantity':'sum'})
  ed05_1.columns=['Revenue','No_of_orders','Avg_order_value','No_of_customers','Quantity']
  ed05_1['Revenue'] = ed05_1['Revenue'].round()

  st.html('<strong>Product Categorywise</strong>')
  fig, ax = plt.subplots()
  plt.barh(ed05_1.index,ed05_1['Revenue'])
  plt.xlabel('Value')
  plt.title('Revenue')
  st.pyplot(fig)
  fig, ax = plt.subplots()
  plt.barh(ed05_1.index,ed05_1['No_of_orders'])
  plt.xlabel('Order Count')
  plt.title('No. of Orders')
  st.pyplot(fig)
  fig, ax = plt.subplots()
  plt.barh(ed05_1.index,ed05_1['No_of_customers'])
  plt.xlabel('Customer Count')
  plt.title('No. of Customers')
  st.pyplot(fig)
  fig, ax = plt.subplots()
  plt.barh(ed05_1.index,ed05_1['Avg_order_value'])
  plt.xlabel('Avg. Order Value')
  plt.title('Order Value')
  st.pyplot(fig)
  fig, ax = plt.subplots()
  plt.barh(ed05_1.index,ed05_1['Quantity'])
  plt.xlabel('Units')
  plt.title('Order in Units')
  st.pyplot(fig)

elif option=="***Month***":
  ed05_2 = df.groupby(by='Month').agg({'Invoice_Value':'sum','Transaction_ID':'count'\
  ,'Avg_Price':'sum','CustomerID':'nunique','Quantity':'sum'})
  ed05_2.columns=['Revenue','No_of_orders','Avg_order_value','No_of_customers','Quantity']
  ed05_2['Revenue'] = ed05_2['Revenue'].round()
  
  st.html('<strong>Month wise</strong>')
  fig, ax = plt.subplots(figsize=(12,8))
  sns.lineplot(ed05_2['Revenue'])
  plt.title('Revenue')
  st.pyplot(fig)
  fig, ax = plt.subplots(figsize=(12,8))
  sns.lineplot(ed05_2['No_of_orders'])
  plt.title('No. of Orders')
  st.pyplot(fig)
  fig, ax = plt.subplots(figsize=(12,8))
  sns.lineplot(ed05_2['No_of_customers'])
  plt.title('No. of Customers')
  st.pyplot(fig)
  fig, ax = plt.subplots(figsize=(12,8))
  sns.lineplot(ed05_2['Avg_order_value'])
  plt.title('Order Value')
  st.pyplot(fig)
  fig, ax = plt.subplots(figsize=(12,8))
  sns.lineplot(ed05_2['Quantity'])
  plt.title('Order in Units')
  st.pyplot(fig)

elif option=='Day of week':
  ed05 = df[::]
  ed05['Day'] = ed05.Transaction_Date.dt.dayofweek
  ed05_4 = ed05.groupby(by='Day').agg({'Invoice_Value':'sum','Transaction_ID':'count'\
  ,'Avg_Price':'sum','CustomerID':'nunique','Quantity':'sum'})
  ed05_4.columns=['Revenue','No_of_orders','Avg_order_value','No_of_customers','Quantity']
  ed05_4['Revenue'] = ed05_4['Revenue'].round()

  st.html('<strong>Day of Week wise</strong>')
  fig, ax = plt.subplots(figsize=(6,4))
  plt.bar(ed05_4.index,ed05_4['Revenue'])
  plt.ylabel('Value')
  plt.title('Revenue')
  st.pyplot(fig)
  fig, ax = plt.subplots(figsize=(6,4))
  plt.bar(ed05_4.index,ed05_4['No_of_orders'])
  plt.ylabel('Order Count')
  plt.title('No. of Orders')
  st.pyplot(fig)
  fig, ax = plt.subplots(figsize=(6,4))
  plt.bar(ed05_4.index,ed05_4['No_of_customers'])
  plt.ylabel('Customer Count')
  plt.title('No. of Customers')
  st.pyplot(fig)
  fig, ax = plt.subplots(figsize=(6,4))
  plt.bar(ed05_4.index,ed05_4['Avg_order_value'])
  plt.ylabel('Avg. Order Value')
  plt.title('Order Value')
  st.pyplot(fig)
  fig, ax = plt.subplots(figsize=(6,4))
  plt.bar(ed05_4.index,ed05_4['Quantity'])
  plt.ylabel('Units')
  plt.title('Order in Units')
  st.pyplot(fig)