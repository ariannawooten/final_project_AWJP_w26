# Pharmacies in Chicago

This project processes and visualizes relationships between Chicago pharmacies and census tracts.

## Setup

```bash
conda env create -f environment.yml
conda activate fire_analysis
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

## Usage

1. Run preprocessing to filter data:
   ```bash
   python code/preprocessing.py
   ```

2. Generate the fire perimeter plot:
   ```bash
   python code/plot_fires.py
   ```
