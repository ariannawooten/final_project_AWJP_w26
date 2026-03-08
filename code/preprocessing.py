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

# make pharmacy names capitalized
df_pharm['Pharmacy Name'] = df_pharm['Pharmacy Name'].str.capitalize()

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
census_2000_gdf = gpd.read_file(census_2000)


#################
### CHICAGO 2010 CENSUS DATA

# load census tract gdf
census_2010 = script_dir / '../data/raw-data/CensusTractsTIGER2010_20260303.geojson'
census_2010_gdf = gpd.read_file(census_2010)


#################
### POPULATION DATA

# load population csv
pop = script_dir / '../data/raw-data/Population_by_2010_Census_Block_20260302.csv'
df_pop = pd.read_csv(pop)

#################
### CHICAGO HEALTH ATLAS DATA

#load data
cha_datapath = script_dir / '../data/raw-data/Chicago Health Atlas Data Download - Census Tracts.csv'
cha = pd.read_csv(cha_datapath)

# remove first 3 rows, which have data definitions, citations, etc.
cha = cha.iloc[4:809]

# source: https://geopandas.org/en/stable/gallery/create_geopandas_from_pandas.html
cha_gdf = gpd.GeoDataFrame(
    cha, geometry=gpd.points_from_xy(cha.Longitude, cha.Latitude), crs="EPSG:4326"
)







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

# map colors to pharmacy status

# create color dictionary
color_dict = {
    'Open': 'green',
    'Closed': 'red',
    'Unknown': 'purple'
}

# map colors to gdf
pharm_gdf['color'] = pharm_gdf['Status'].map(color_dict)

# join gdfs
combined1_gdf = gpd.sjoin(pharm_gdf, census_2010_gdf, 
    how='left',
    predicate='within')

# rename combined_gdf1 column for spatial joining purposes
combined1_gdf.rename(columns={'geoid10':'GEOID'}, inplace=True)

# group data by census tract
pharm_by_tract = (
    combined1_gdf
    .groupby('GEOID')
    .size()
    .reset_index(name='pharmacy_count')
)

# count pharmacies per tract
pharm_counts = (
    combined1_gdf
    .groupby('tractce10')
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

# convert census and pharm gdf to csv
census_and_pharm_gdf.to_csv('census_and_pharm_csv')






### COMBINING CENSUS AND PHARMS WITH POPULATION
# create a function to convert
def blocks_to_tracts(df_pop, geoid_col='CENSUS BLOCK FULL'): 
    df = df_pop.copy()

    # ensure geoid is string
    df[geoid_col] = df[geoid_col].astype(str).str.zfill(15)

    # convert population to numeric
    df['TOTAL POPULATION'] = pd.to_numeric(
        df['TOTAL POPULATION'],
        errors='coerce'
    )

    # extract tract geoid
    df['geoid10'] = df[geoid_col].str[:11]

    # group by tract and sum numeric values
    tract_df = (
        df
        .groupby('geoid10', as_index=False)['TOTAL POPULATION']
        .sum()
    )

    return tract_df

# recode population census blocks to census tracts
pop_tract_df = blocks_to_tracts(df_pop)


# merge census tract populations to census and pharm gdf
cen_tract_pop_gdf = census_and_pharm_gdf.merge(pop_tract_df,
on='geoid10',
how='outer'
)

# create col of number of pharmacies per 1000 residents
cen_tract_pop_gdf['pharm_per_1000'] = (
    cen_tract_pop_gdf['pharmacy_count'] / 
    cen_tract_pop_gdf['TOTAL POPULATION']
) * 1000

# convert to csv
cen_tract_pop_gdf.to_csv('cen_tract_pop.csv')



### MERGE CHA AND PHARMACIES
# join gdfs (alternative merge with more census data and less pharm data)
combined2_gdf = gpd.sjoin(census_2010_gdf, pharm_gdf, 
    how='left',
    predicate='intersects')

#rename geo id column to merge with cha later
combined2_gdf = combined2_gdf.rename(columns={'geoid10':'GEOID'})

cha_pharm = combined2_gdf.merge(cha_gdf, on='GEOID')

# define geometry column for plotting later
#cha_pharm = cha_pharm.set_geometry('geometry_y')

# set as geometry for future chloropleth maps
cha_pharm = cha_pharm.set_geometry('geometry_x')

# save as csv
cha_pharm.to_csv('cha_pharm.csv')



### DIFFERENT PHARM AND CENSUS JOIN GDF

# join gdfs
combined3_gdf = gpd.sjoin(pharm_gdf, census_2000_gdf, 
    how='left',
    predicate='within')

# group data by census tract
pharm_by_tract2 = (
    combined3_gdf
    .groupby('census_t_1')
    .size()
    .reset_index(name='pharmacy_count')
)

# count pharmacies per tract
pharm_counts2 = (
    combined3_gdf
    .groupby('tract_ce_3')
    .size()
    .reset_index(name='pharmacy_count')
)



