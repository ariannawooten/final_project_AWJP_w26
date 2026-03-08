import geopandas as gpd
import pandas as pd
from pathlib import Path
from shapely import wkt
import pydeck as pdk

script_dir = Path(__file__).parent



### PHARMACY DATA
# load data
pharmacy = script_dir / '../data/raw-data/Pharmacy_Status_-_Historical_20260302.csv'
df_pharm = pd.read_csv(pharmacy)

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
census_2000 = script_dir / '../data/raw-data/Census_Tracts_20260302.geojson'
census_2000_gpd = gpd.read_file(census_2000)


#################
### CHICAGO 2010 CENSUS DATA

# load census tract gdf
census_2010 = script_dir / '../data/raw-data/CensusTractsTIGER2010_20260303.geojson'
census_2010_gpd = gpd.read_file(census_2010)


#################
### POPULATION DATA

# load population csv
pop = script_dir / '../data/raw-data/Population_by_2010_Census_Block_20260302.csv'
pop_csv = pd.read_csv(pop)

#################
### CHICAGO HEALTH ATLAS DATA

#load data
cha_datapath = script_dir / '../data/raw-data/Chicago Health Atlas Data Download - Census Tracts.csv'
cha = pd.read_csv(cha_datapath)



# remove first 3 rows, which have data definitions, citations, etc.
cha = cha.iloc[4:809]

#################
### COMBINING PHARMACIES AND CENSUS BLOCKS 
### INTO census_and_pharm.gdf

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

# join gdfs
combined1_gdf = gpd.sjoin(pharm_gdf, census_2010_gdf, 
    how='left',
    predicate='within')

# group data by census tract
pharm_by_tract = (
    combined1_gdf
    .groupby('geoid10')
    .size()
    .reset_index(name='pharmacy_count')
)

# merge counts back to census polygons
census_and_pharm_gdf = census_2010_gdf.merge(
    pharm_counts,
    on='tractce10',
    how='left'
)

# fill missing tracts with zero pharmacies
census_and_pharm_gdf['pharmacy_count'] = (
    census_and_pharm_gdf['pharmacy_count']
    .fillna(0)
)

# project to crs in meters
census_and_pharm_gdf = census_and_pharm_gdf.to_crs(epsg=26916)

# calculate area in square miles
census_and_pharm_gdf['area_sq_miles'] = (
    census_and_pharm_gdf.geometry.area / 2_589_988
)

# compute density
census_and_pharm_gdf['pharm_density'] = (
    census_and_pharm_gdf['pharmacy_count'] /
    census_and_pharm_gdf['area_sq_miles']
)





