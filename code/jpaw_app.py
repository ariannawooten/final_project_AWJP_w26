# DASHBOARD CODE #

#load libraries
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
#import pydeck as pdk
import json

# load data
cha = pd.read_csv('/Users/ariannawooten/Downloads/final_project_AWJP_w26/data/raw-data/Chicago Health Atlas Data Download - Census Tracts.csv')#chicago health atlas data (2020)

# remove first 3 rows, which have data definitions, citations, etc.
cha = cha.iloc[4:809]

# create histogram: proximity to roads, railways, and airports by census
#hist = alt.Chart(cha).mark_bar().encode(
#    alt.X('Name:N', title='Census Tract', 
#    sort = alt.EncodingSortField(field='EKR_2024', order = 'descending')),
#    alt.Y('average(EKR_2024):Q', title = 'Proximity to Roads, Railways, and Airports')
#    )

#hist

#scatter = alt.Chart(cha).mark_point().encode(
#    alt.X('Name:O'),
#    alt.Y('EKR_2024')
#)

#scatter

# bar plot 2: median household income by census tract
#hist2 = alt.Chart(cha).mark_bar().encode(
#    alt.X('Name:O', title='Census Tract', sort = alt.EncodingSortField(field='INC_2020-2024', order = 'descending')),
#    alt.Y('INC_2020-2024:Q', title='Median Household Income')
#)

#hist2

# transportation burden plot
#transpo = alt.Chart(cha).mark_bar().encode(
#    alt.X('Name:O', title='Census Tract', sort = alt.EncodingSortField(field='RITB_2022', order = 'descending')),
#    alt.Y('RITB_2022:Q', title='Transportation Burden (Percentile)')
#    )

#transpo

# ── File mappings ──────────────────────────────────────────────
DASHBOARD_DIR = "data/dashboard"
EXTERNAL_DIR = "data/external/dashboard"

demo_options = ['All', 'Low Median Household Income','Hardship Index', 'Percentage of Seniors Living Alone']

# ── Page config ────────────────────────────────────────────────
st.set_page_config(page_title="Chicago Health and Pharmacy Access Dashboard", layout="wide")
st.title("Chicago Health and Pharmacy Access Dashboard")

# ── Sidebar controls ──────────────────────────────────────────
demographics = st.sidebar.selectbox("Demographic", demo_options)

#show_unchanged = st.sidebar.checkbox("Show routes with no cuts", value=True)
#mode_filter = st.sidebar.multiselect("Mode", ["Bus", "L"], default=["Bus", "L"])

st.subheader(f"Chicago Demographics by Census Tract ({demographics})")

transpo = alt.Chart(cha).mark_bar().encode(
    alt.X('Name:O', title='Census Tract', sort = alt.EncodingSortField(field='RITB_2022', order = 'descending')),
    alt.Y('RITB_2022:Q', title='Transportation Burden (Percentile)')
    )

# add a line showing the 50th percentile
# source: https://stackoverflow.com/questions/77802979/how-to-draw-a-horizontal-line-at-y-0-in-an-altair-line-chart
median = alt.Chart(pd.DataFrame({'y': [50]})).mark_rule(
    color='red',
    size=2
).encode(
    y='y:Q'
)

transpo = transpo + median
transpo

