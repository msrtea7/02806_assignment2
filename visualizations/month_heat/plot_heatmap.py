import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar, BasicTicker
from bokeh.transform import transform
from bokeh.palettes import Iridescent18
import datetime

# Hyper parameters
## Define directories

DATA_DIR = "../../data_sf/"
CSV_NAME = 'combined_crime_data.csv'

# read it once only
df = pd.read_csv(DATA_DIR + CSV_NAME)


# First filter out "motor vehicle theft" type crimes
motor_theft_df = df[df['Incident Category'].str.lower() == 'motor vehicle theft'].copy()

# Ensure the date column is datetime type
motor_theft_df['Incident Date'] = pd.to_datetime(motor_theft_df['Incident Date'])

# Create year and month columns
motor_theft_df['Year'] = motor_theft_df['Incident Date'].dt.year
motor_theft_df['Month'] = motor_theft_df['Incident Date'].dt.month

# Get the minimum and maximum years in the data
min_year = 2003  # You can replace with the actual minimum year in your dataset
max_year = 2025  # You can replace with the actual maximum year in your dataset

# Create counts for each month of each year
monthly_counts = motor_theft_df.groupby(['Year', 'Month']).size().reset_index(name='count')

# Create complete year-month index (including months without data)
years = range(min_year, max_year + 1)
months = range(1, 13)

# Create all possible year-month combinations
all_year_month = pd.MultiIndex.from_product([years, months], names=['Year', 'Month']).to_frame(index=False)

# Merge actual data with all possible year-months, fill missing values with 0
monthly_counts = pd.merge(all_year_month, monthly_counts, on=['Year', 'Month'], how='left').fillna(0)

# Convert count column to integer type
monthly_counts['count'] = monthly_counts['count'].astype(int)

# Create data format needed for heatmap
# Convert month numbers to month names for display in the chart
month_names = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}
monthly_counts['Month_Name'] = monthly_counts['Month'].map(month_names)

# Create data source
source = ColumnDataSource(
    data=dict(
        year=[str(year) for year in monthly_counts['Year']],
        month=monthly_counts['Month_Name'],
        month_idx=monthly_counts['Month'],
        count=monthly_counts['count']
    )
)

# Create color mapper - from light blue to dark blue
# colors = list(reversed(Blues9))  # Reverse colors so high values are dark
colors = list(Iridescent18)
mapper = LinearColorMapper(palette=colors, low=0, high=monthly_counts['count'].max())

# Set figure size and tools
TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

# Create year-month labels
years = [str(year) for year in range(min_year, max_year + 1)]
months = list(month_names.values())

# Create heatmap
p = figure(
    # title="Monthly Motor Vehicle Theft (2003-2025)",
    toolbar_location=None,
    y_range=months,
    x_range=list(years),  # Reverse order so earliest years are at the bottom
    x_axis_location="above",
    width=600,
    height=600,
    tools=TOOLS,
    # toolbar_location='below',
    tooltips=[('Year-Month', '@year-@month'), ('Count', '@count')],
    background_fill_color=None,  # Transparent background
    border_fill_color=None,      # Transparent border
    outline_line_color=None      # Transparent outline
)

# Add heatmap rectangles
p.rect(
    y="month",
    x="year",
    width=1,
    height=1,
    source=source,
    fill_color=transform('count', mapper),
    line_color=None
)

# Add color bar
color_bar = ColorBar(
    color_mapper=mapper,
    ticker=BasicTicker(desired_num_ticks=7),
    label_standoff=6,
    border_line_color=None,
    location=(0, 0),
    width=20,
    height=300,                        # Adjust to a shorter height
    title="",                          # Remove default title
    scale_alpha=1,                     # no slightly transparent color bar
    background_fill_color=None, 
    # major_label_text_font_style='bold',
    
)

p.add_layout(color_bar, 'right')

# Set axes
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "10px"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = 1.0
# p.title.text_font_size = '12pt'

# Set x-axis (year) labels to display at an angle
p.xaxis.major_label_orientation = 0.9  # About 40 degrees

# Set grid lines to transparent
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None


# Save as HTML file (transparent background)
output_file("motor_vehicle_theft_heatmap.html")
save(p)