# DASHBOARD CODE #

#load libraries
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
#import pydeck as pdk
import json

# load data

cpum = pd.read_csv('/Users/ariannawooten/Downloads/final_project_AWJP_w26/data/raw-data/meps_00001.csv.gz') # CPUM national health data
cha = pd.read_csv('/Users/ariannawooten/Downloads/final_project_AWJP_w26/data/raw-data/Chicago Health Atlas Data Download - Census Tracts.csv')#chicago health atlas data (2020)

# remove first 3 rows, which have data definitions, citations, etc.
cha = cha.iloc[4:809]

# create histogram

hist = alt.Chart(cha).mark_bar().encode(
    alt.X('Name:O').bin(),
    alt.Y('average(EKR_2024)')
)

hist

scatter = alt.Chart(cha).mark_point().encode(
    alt.X('Name:O'),
    alt.Y('EKR_2024')
)

scatter

hist = alt.Chart(cha).mark_bar().encode(
    alt.X('Name:O'),
    alt.Y('INC_2020-2024:Q')
)

hist

# ── File mappings ──────────────────────────────────────────────
DASHBOARD_DIR = "data/dashboard"
EXTERNAL_DIR = "data/external/dashboard"

demo_options = ['Median household income','option 2']

# ── Page config ────────────────────────────────────────────────
st.set_page_config(page_title="Chicago Health and Pharmacy Access Dashboard", layout="wide")
st.title("Chicago Health and Pharmacy Access Dashboard")

# ── Sidebar controls ──────────────────────────────────────────
demographics = st.sidebar.selectbox("Demographic", demo_options)

#show_unchanged = st.sidebar.checkbox("Show routes with no cuts", value=True)
#mode_filter = st.sidebar.multiselect("Mode", ["Bus", "L"], default=["Bus", "L"])

# ── Column 1: Plot ────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Chicago Demographics by Census Tract ({demographics})")

    hist = alt.Chart(cha).mark_bar().encode(
        alt.X('Name:O'),
        alt.Y('INC_2020-2024:Q')
    )

    hist

    st.altair_chart(hist, use_container_width=True)

