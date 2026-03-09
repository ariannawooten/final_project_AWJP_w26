import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# add basic text
st.write('hello world')

# add plot using pandas
st.title('Chicago Map Using Pandas')

df = pd.DataFrame(
    np.random.randn(100, 2) / [100,100] + [41.8781, -87.6298],
    columns=['lat', 'lon']
)
st.map(df)

# add plot using folium
st.title('Chicago Map using Streamlit Folium')

m = folium.Map(location=[41.8781, -87.6298], zoom_start=12)
folium.Marker([41.8781, -87.6298], popup="Chicago").add_to(m)

st_folium(m)
