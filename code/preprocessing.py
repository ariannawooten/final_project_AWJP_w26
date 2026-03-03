import geopandas as gpd
import pandas as pd
from pathlib import Path
from shapely import wkt
import pydeck as pdk

### PHARMACY DATA
# load data
data_path = 'C:\\Users\\blueb\\final_project_AWJP_w26\\data\\raw-data\\Pharmacy_Status_-_Historical_20260302.csv'
df_pharm = pd.read_csv(data_path)

# make pharmacy names in all caps
df_pharm['Pharmacy Name'] = df_pharm['Pharmacy Name'].str.upper()

# create mapping for pharmacy status
mapping = {
    'OPEN':'Open',
    'CLOSED': 'Closed',
    'Permanently closed': 'Closed',
    'closed': 'Closed',
    'open': 'Open',
    'permanently closed': 'Closed',
    'unknown': 'Unknown'
}

# recode the status column
df_pharm['Status'] = df_pharm['Status'].replace(mapping)


#################
### CHICAGO 2000 CENSUS DATA

# load census tract gdf
census_gpd = gpd.read_file('C:\\Users\\blueb\\final_project_AWJP_w26\\data\\raw-data\\Census_Tracts_20260302.geojson')


#################
### CHICAGO 2010 CENSUS DATA

# load census tract gdf
census_gpd = gpd.read_file('C:\\Users\\blueb\\final_project_AWJP_w26\\data\\raw-data\\Census_Tracts_20260302.geojson')



#################
### POPULATION DATA

# load population csv
pop_csv = pd.read_csv('C:\\Users\\blueb\\final_project_AWJP_w26\\data\\raw-data\\Population_by_2010_Census_Block_20260302.csv')

#################
### CHICAGO HEALTH ATLAS DATA

#load data
cha_datapath = '/Users/ariannawooten/Downloads/final_project_AWJP_w26/data/raw-data/Chicago Health Atlas Data Download - Census Tracts.csv' #chicago health atlas data (2020)'
cha = pd.read_csv(cha_datapath) #chicago health atlas data (2020)

# remove first 3 rows, which have data definitions, citations, etc.
cha = cha.iloc[4:809]

#################
### COMBINING PHARMACIES AND CENSUS BLOCKS

# load pharmacies as a geodataframe

# drop nas
df_pharm = df_pharm.dropna(subset=['New Georeferenced Column'])

# drop na strings
df_pharm = df_pharm[
    df_pharm['New Georeferenced Column']
    .str.lower()
    .ne('nan')
]

# convert wkt to a geometry
df_pharm['geometry'] = gpd.GeoSeries.from_wkt(
    df_pharm['New Georeferenced Column'],
    on_invalid='ignore'
)

# drop failed parses
df_pharm = df_pharm.dropna(subset=['geometry'])

# create geodataframe
pharm_gdf = gpd.GeoDataFrame(
    df_pharm,
    geometry='geometry',
    crs='EPSG:4326'
)

# sanity check
print(df_pharm.shape)
print(df_pharm.head())

# join gdfs
combined1_gdf = gpd.sjoin(pharm_gdf, census_2010_gdf, 
    how='left',
    predicate='within')

# check object type
print('Object type:', type(combined1_gdf))

# check geometry type
print('\nGeometry type:', combined1_gdf.geom_type.value_counts())





