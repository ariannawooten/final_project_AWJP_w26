import streamlit as st
import pandas as pd
import numpy as np


st.write('hello world')

st.title('Chicago Map')

df = pd.DataFrame(
    np.random.randn(100, 2) / [100,100] + [41.8781, -87.6298],
    columns=['lat', 'lon']
)
st.map(df)

