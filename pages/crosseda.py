import streamlit as st
import pandas as pd
import numpy as np
from itertools import combinations
from collections import Counter

df = st.session_state.datakey
st.subheader('Cross Selling Products')
common = st.slider('How many most common products sold',5,25,10)

new_df = df[df.Transaction_ID.duplicated(keep=False)]
new_df['Product_Bundle']=new_df.groupby('Transaction_ID')['Product_Description'].transform(lambda x: '|'.join(x))
new_df = new_df[['Transaction_ID','Product_Bundle']].drop_duplicates()

count= Counter()
for row in new_df['Product_Bundle']:
    row_list = row.split('|')
    count.update(Counter(combinations(row_list,2)))
mostcommon = pd.DataFrame(count.most_common(common))
mostcommon.columns=['Products','Frequency']

st.write(mostcommon)
