# Pharmacies in Chicago

This project processes and visualizes relationships between Chicago pharmacies and census tracts. See final_project.pdf for a fuller summary of the project.

## Data Dashboard

```
link: https://ariannawooten-awjp-data-vis-final-project--pub-app-nogpd-xk3qtg.streamlit.app/

Note: Streamlit dashboards that have not been used in the past 24hrs must be "woken up" by running the associated code. Prepare the dashboard to run by running pub_app_nogpd.py 
```

## Setup

```
Clone the repository to your local device
```
## Data Sources and Processing

```
Data Sources:
1. Chicago Data Portal (Census Tract Boundaries): https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Census-Tracts-2010/5jrd-6zik
2. Chicago Data Portal (Pharmacy Status Map): https://data.cityofchicago.org/Health-Human-Services/Pharmacy-Status-Map-Historical/2f34-72ii
3. Chicago Health Altlas (Health and Socioeconomic Data): https://chicagohealthatlas.org/download

Data Processing:
The above datasets were converted to geospatial data using their pre-existing geodata. Data cleaning included standardizing capitalization for certain variables, converting data from strings (text) to numeric data types, dropping observations with empty values, and assigning "0" to empty values when appropriate (for example, to signify a lack of pharmacies). Our data cleaning and processing code is located under the "code" folder in preprocessing.py. 
```

## Project Structure

```
data/
  raw-data/           # Raw data files
    CensusTractsTIGER2010_20260303.cvs                      # CSV of 2010 Chicago census tracts
    CensusTractsTIGER2010_20260303.geojson                  # Geojson of 2010 Chicago census tracts
    Chicago Health Atlas Data Download - Census Tracts.csv  # Chicago health data
    Pharmacy_Status_-_Historical_20260302.csv               # Chicago pharmacy data as of March 8, 2025
    Population_by_2010_Census_Block_20260302.csv            # Population of 2010 Chicago census blocks data
    
  derived-data/       # Filtered data and output plots
    census_and_pharm_gdf.csv  # Merged data of pharmacies in Chicago census tracts
    cha_pharm.csv    # Merged Chicago health and pharmacy data 
code/
  DataVis_Final_JPAW.qmd # Dashboard code
  all_merged.csv  # Merge of all used data
  cen_tract_pop.csv # Census tracts by population data
  census_and_pharm_csv # Pharmacies by census tract data
  cha_pharm.csv # Combined Chicago health and pharmacy data
  cha_plots.qmd # Plots of cha data
  chicago_pharmacy.qmd # Development of Chicago pharmacy code
  hardship_pharm.qmd # Plots hardship rates of Chicago census tracts and pharmacies
  inc_pharm.qmd # Plots pharmacy distribution on Chicago census tracts by per capita income
  jpaw_app.py # Dashboard plots
  pharm_dens_sqmi.qmd # Plots pharmacy density per square miles of Chicago census tracts
  pharm_dist.qmd # Plots distribution of pharmacies on Chicago census tracts
  pharm_type.qmd # Plots the most common pharmacy types in Chicago
  preprocessing.py    # Filters all data
  residents_pharm.qmd # Plots pharmacies per 1000 residents of each Chicago census tract
  transit_pharm_dens.qmd # Plots pharmacy distribution over transportation burden per Chicago census tract
```
