import streamlit as st

data = st.session_state.datakey
datahead = f'{data.shape[0]} samples'
st.subheader('Raw Data')
st.write(datahead)

st.write(data)