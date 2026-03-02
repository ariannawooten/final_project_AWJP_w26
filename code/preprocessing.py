import geopandas as gpd
import pandas as pd
from pathlib import Path
from shapely import wkt
import pydeck as pdk

### PHARMACY DATA
# load data
data_path = 'C:\\Users\\blueb\\final_project_AWJP_w26\\data\\raw-data\\Pharmacy_Status_-_Historical_20260302.csv'
df_pharm = pd.read_csv(data_path)


# explore data
df_pharm.shape
df_pharm.head()

# make pharmacy names in all caps
df_pharm['Pharmacy Name'] = df_pharm['Pharmacy Name'].str.upper()


# load gdf
census = gpd.read_file('C:\\Users\\blueb\\final_project_AWJP_w26\\data\\raw-data\\Census_Tracts_20260302.geojson')






df['geometry'] = df['geometry'].apply(wkt.loads)
fire_gdf = gpd.GeoDataFrame(df, geometry='geometry')

fire_gdf = fire_gdf[fire_gdf['FIRE_YEAR'] > 2015]

fire_gdf.to_file(output_fire)

# Process Canadian CPI data
raw_cpi = script_dir / '../data/raw-data/canadian_cpi.csv'
output_cpi = script_dir / '../data/derived-data/cpi_filtered.csv'

cpi_df = pd.read_csv(raw_cpi)
cpi_df = cpi_df.rename(columns={cpi_df.columns[0]: 'Product'})

# Filter to columns from 2020 onwards
date_cols = [col for col in cpi_df.columns if '2020' in col or '2021' in col or '2022' in col or '2023' in col or '2024' in col]
cpi_filtered = cpi_df[['Product'] + date_cols].dropna(subset=['Product'])

cpi_filtered.to_csv(output_cpi, index=False)
print(f"CPI data filtered: {len(cpi_filtered)} products, {len(date_cols)} months")


### CHICAGO HEALTH ATLAS DATA

#load data
cha_datapath = '/Users/ariannawooten/Downloads/final_project_AWJP_w26/data/raw-data/Chicago Health Atlas Data Download - Census Tracts.csv' #chicago health atlas data (2020)'
cha = pd.read_csv(cha_datapath) #chicago health atlas data (2020)

# remove first 3 rows, which have data definitions, citations, etc.
cha = cha.iloc[4:809]