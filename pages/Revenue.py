import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.subheader('Revenue')
df = st.session_state.datakey

st.html('<strong>Revenue Monthwise</strong>')
ed03 = df[['CustomerID','Month','Invoice_Value']]
ed03['status'] = np.where(df['Tenure_Months']>12,'Existing','New')
ed03 = ed03.groupby(by=['Month','status'])['Invoice_Value'].sum()
ed03 = pd.DataFrame(ed03)
ed03.reset_index(inplace=True)
ed03 = ed03.pivot(index='Month',columns='status',values='Invoice_Value')
st.bar_chart(data=ed03,x_label='Months',y_label='Revenue',stack=False)

st.html('<strong>Revenue based on Promotions</strong>')
ed04 = df.groupby(by=['Discount_pct'])['Invoice_Value'].sum().round()
ed04 = pd.DataFrame(ed04)
fig1, ax1 = plt.subplots()
labels = ['No Promotions','10% off','20% off','30% off']  
ax1.pie(ed04.Invoice_Value,labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig1)