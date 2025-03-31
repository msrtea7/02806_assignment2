# Task 1 and General
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import folium
from folium.plugins import HeatMap, MarkerCluster, HeatMapWithTime

# Hyper parameters
## Define directories
SAVE_DIR = "./pics/"
DATA_DIR = "../../data_sf/"
CSV_NAME = 'combined_crime_data.csv'

# read it once only
df = pd.read_csv(DATA_DIR + CSV_NAME)

def create_yearly_trend_map(df, start_year=2003, end_year=2024, crime_type="motor vehicle theft"):
    """
    Create a dynamic heat map based on year, with a time slider to control the display
    
    Parameters:
    df (DataFrame): DataFrame containing crime data
    start_year (int): Starting year
    end_year (int): Ending year
    crime_type (str, optional): Specified crime type, if None, analyze all types
    
    Returns:
    folium.Map: Map object containing time-based heat map
    """
    # If crime type is specified, filter the data first
    if crime_type:
        df = df[df['Incident Category'] == crime_type]
    
    # Clean data: remove NaN values and abnormal coordinates
    df_clean = df.copy()
    df_clean = df_clean.dropna(subset=['Latitude', 'Longitude'])
    df_clean = df_clean[(df_clean['Latitude'] < 40) & 
                        (df_clean['Latitude'] > 37.5) &
                        (df_clean['Longitude'] < -122.25) & 
                        (df_clean['Longitude'] > -123)]
    
    # Ensure Year column is integer type
    df_clean['Year'] = df_clean['Year'].astype(int)
    
    # Create a map with faded gray style
    tiles = 'CartoDB positron'
    m = folium.Map(location=[37.7749, -122.4194], zoom_start=12, 
                    tiles=tiles, control_scale=True)
    
    # Prepare data organized by year
    years_range = range(start_year, end_year + 1)
    heat_data = []
    year_labels = []
    
    for year in years_range:
        # Filter data for this year
        year_data = df_clean[df_clean['Year'] == year]
        
        if len(year_data) > 0:
            # Extract coordinates
            locations = year_data[['Latitude', 'Longitude']].values.tolist()
            heat_data.append(locations)
            year_labels.append(str(year))
        else:
            # Add an empty list even if there's no data to maintain index correspondence
            heat_data.append([])
            year_labels.append(str(year))
    
    # Add heat map with time control
    HeatMapWithTime(
        heat_data,
        index=year_labels,
        auto_play=True,
        max_opacity=0.8,
        radius=15,
        gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'},
        name='Yearly Crime Trends'
    ).add_to(m)
    
    return m