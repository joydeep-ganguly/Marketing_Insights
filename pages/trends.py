import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.subheader("Trends / Seasonality of Sales")
df = st.session_state.datakey

option = st.radio(
    "Display results in the basis of:",
    [":rainbow[Category]", "Location", "***Month***"]
)

if option==':rainbow[Category]':
  ed06_1 = df.groupby(by='Product_Category')['Invoice_Value'].sum().round()
  ed06_1 = pd.DataFrame(ed06_1)
  ed06_1.reset_index(inplace=True)
  fig, ax = plt.subplots(figsize=(8,6))
  ax.set_ylabel('Revenue')
  ax.set_title('By Category')
  ax.set_xticks(ed06_1['Product_Category'].index,ed06_1['Product_Category'].values, rotation=90)
  ax.set_yticks([])
  ax.plot(ed06_1['Invoice_Value'])
  st.pyplot(fig)
elif option=='Location':
  ed06_2 = df.groupby(by='Location')['Invoice_Value'].sum().round()
  ed06_2 = pd.DataFrame(ed06_2)
  ed06_2.reset_index(inplace=True)
  fig, ax = plt.subplots(figsize=(8,6))
  ax.set_ylabel('Revenue')
  ax.set_title('By Location')
  ax.set_xticks(ed06_2['Location'].index,ed06_2['Location'].values, rotation=90)
  ax.set_yticks([])
  ax.bar(ed06_2['Location'],ed06_2['Invoice_Value'])
  st.pyplot(fig)
elif option=="***Month***":
  ed06_3 = df.groupby(by='Month')['Invoice_Value'].sum().round()
  ed06_3 = pd.DataFrame(ed06_3)
  ed06_3.reset_index(inplace=True)
  fig, ax = plt.subplots(figsize=(8,6))
  ax.set_ylabel('Revenue')
  ax.set_title('By Month')
  ax.set_xticks(ed06_3['Month'].index,ed06_3['Month'].values)
  ax.set_yticks([])
  ax.plot(ed06_3['Invoice_Value'])
  st.pyplot(fig)
  