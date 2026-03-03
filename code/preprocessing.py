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


### CHICAGO CENSUS DATA

# load census tract gdf
census_gpd = gpd.read_file('C:\\Users\\blueb\\final_project_AWJP_w26\\data\\raw-data\\Census_Tracts_20260302.geojson')


# load population csv
pop_csv = pd.read_csv('C:\\Users\\blueb\\final_project_AWJP_w26\\data\\raw-data\\Population_by_2010_Census_Block_20260302.csv')



### CHICAGO HEALTH ATLAS DATA

#load data
cha_datapath = '/Users/ariannawooten/Downloads/final_project_AWJP_w26/data/raw-data/Chicago Health Atlas Data Download - Census Tracts.csv' #chicago health atlas data (2020)'
cha = pd.read_csv(cha_datapath) #chicago health atlas data (2020)

# remove first 3 rows, which have data definitions, citations, etc.
cha = cha.iloc[4:809]