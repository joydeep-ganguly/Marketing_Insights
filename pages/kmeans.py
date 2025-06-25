import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

df = st.session_state.datakey
st.subheader('KMeans Segmentation')
num = st.selectbox('Select number of clusters :',[2,3,4],0)

df_kmeans = df[::]
#adding features and categorical to numerical
le = LabelEncoder()
df_kmeans.CustomerID = le.fit_transform(df_kmeans.CustomerID)
df_kmeans['ProductID'] = le.fit_transform(df_kmeans['Product_SKU'])
df_kmeans['Product_Category'] = le.fit_transform(df_kmeans['Product_Category'])
df_kmeans['Coupon_Status'] = le.fit_transform(df_kmeans['Coupon_Status'])
df_kmeans['Location'] = le.fit_transform(df_kmeans['Location'])
df_kmeans['Gender'] = le.fit_transform(df_kmeans['Gender'])
df_kmeans['Year'] = df_kmeans.Transaction_Date.dt.year
df_kmeans['Month'] = df_kmeans.Transaction_Date.dt.month
#dropping columns
df_kmeans.drop(columns=['Transaction_ID','Transaction_Date','Product_SKU','Product_Description'],inplace=True)
df_kmeans.drop(columns=['Invoice_Value','Tax_Amount','Online_Spend'],inplace=True)

#scale the data
ss = StandardScaler()
df_kmeans = ss.fit_transform(df_kmeans)
df_kmeans = pd.DataFrame(df_kmeans)
km = KMeans(n_clusters=num, random_state=24)
km.fit(df_kmeans)
df['label'] = km.labels_
segment = pd.DataFrame(df.label.value_counts()).reset_index()
labels = []
for i in range(1,num+1):
  labels.append(f'Segment-{i}')

fig,ax = plt.subplots(figsize=(9,5))
ax.pie(segment['count'], labels=labels, autopct='%1.1f%%')
ax.axis('equal')
st.pyplot(fig)

for i in range(0,num):
  segment = df[df.label==i].iloc[:,:-1]
  st.html(f'<strong>Segment-{i+1} [{segment.shape[0]} samples]</strong>')
  st.write(segment)


#segment1 = df[df.label==0].iloc[:,:-1]
#st.html(f'<strong>1st Segment [{segment1.shape[0]} samples]</strong>')
#st.write(segment1)

#segment2 = df[df.label==1].iloc[:,:-1]
#st.html(f'<strong>2nd Segment [{segment2.shape[0]} samples]</strong>')
#st.write(segment2)
