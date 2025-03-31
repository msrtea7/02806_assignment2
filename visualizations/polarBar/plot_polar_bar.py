import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file
from bokeh.models import ColumnDataSource, Select, Label, CustomJS, HoverTool, WheelZoomTool
from math import pi, sin, cos
from bokeh.palettes import Magma256
from bokeh.layouts import column
from bokeh.models.widgets import Div
from bokeh.transform import linear_cmap
from bokeh.embed import file_html
from bokeh.resources import CDN

def create_crime_time_visualization(df, crime_type="motor vehicle theft"):
    """Create a polar bar chart for crime time distribution (improved version)"""
    
    # Ensure Year column is string type
    df['Year'] = df['Year'].astype(str)
    
    # Extract hour part from time
    df['Hour'] = df['Incident Time'].apply(lambda x: int(str(x).split(':')[0]) if ':' in str(x) else 0)
    
    # Filter for specified crime type
    # Ensure case matching for crime type
    crime_column = 'Incident Category'  # Assume crime type is stored in 'Incident Category' column
    # For more robust matching, use case-insensitive filtering
    df = df[df[crime_column].str.lower() == crime_type.lower()]
    # Aggregate data by year and hour
    years = sorted(df['Year'].unique())
    years.remove('2025')
    all_data = {}
    
    for year in years:
        year_data = df[df['Year'] == year]
        hour_data = {}
        for hour in range(24):
            hour_data[hour] = len(year_data[year_data['Hour'] == hour])
        all_data[year] = hour_data
    
    # Set output to HTML file (transparent background)
    output_file("crime_time_distribution.html", title="Crime Time Distribution")
    
    # Find maximum value in all data for scaling
    max_count = 0
    for year in all_data:
        year_max = max(all_data[year].values())
        if year_max > max_count:
            max_count = year_max
    
    # Create data sources for each year
    data_sources = {}
    for year in years:
        hours = list(range(24))
        values = [all_data[year][hour] for hour in hours]
        angles = [hour/24 * 2*pi for hour in hours]
        bar_width = 2*pi/24
        
        source_data = {
            'hour': hours,
            'value': values,
            'angle': angles,
            'inner_radius': [0.1] * len(hours),
            'outer_radius': [(v / max_count) * 180 for v in values],
            'start_angle': [a - bar_width/2 for a in angles],
            'end_angle': [a + bar_width/2 for a in angles],
        }
        data_sources[year] = ColumnDataSource(source_data)
    
    ################################################################################

    # Create base chart
    p = figure(
        tools="",
        width=500, height=500,
        x_range=(-250, 250), y_range=(-250, 250),
        toolbar_location=None,
        background_fill_color=None,
        border_fill_color=None,
        outline_line_color=None,
        min_border_left=5,   # Set left margin
        min_border_right=5,  # Set right margin
        min_border_top=5,    # Set top margin
        min_border_bottom=5, # Set bottom margin
    )
    p.add_tools(WheelZoomTool())
    # Hide axes
    p.axis.visible = False
    p.grid.visible = False
    
    # Add reference circles
    for radius in [60, 120, 180]:
        p.circle(0, 0, radius=radius, fill_color=None, line_color="#888888", 
                line_dash="dashed", line_width=1, alpha=0.7)
    
    # Add hour tick marks
    for hour in range(24):
        angle = hour/24 * 2*pi
        x = cos(angle) * 180
        y = sin(angle) * 180
        p.line([0, x], [0, y], line_color="#666666", line_width=1, alpha=0.6)
        
        # Add hour labels
        label_x = cos(angle) * 200
        label_y = sin(angle) * 200
        hour_label = Label(
            x=label_x, y=label_y, 
            text=str(hour),
            text_align="center", text_baseline="middle",
            text_font_size="9pt",
            text_font_style="bold",
            text_color="#333333"  # Dark text to ensure visibility
        )
        p.add_layout(hour_label)
    
    # Create year selector
    year_select = Select(
        title="Choose Year",
        value=years[0],
        options=years,
        width=80,
        height=30,
    )
    
    # Create title div - initially for first year
    
    # Choose a better color map - Turbo is a high saturation map
    # We'll extract a subset from the color map, avoiding colors that are too light
    color_palette = list(reversed(Magma256[75:256]))  # Avoid colors that are too light
    
    # Create wedge chart for each year
    wedges_dict = {}
    for year in years:
        source = data_sources[year]
        
        wedges = p.annular_wedge(
            x=0, y=0,
            inner_radius='inner_radius', 
            outer_radius='outer_radius',
            start_angle='start_angle', 
            end_angle='end_angle',
            fill_color=linear_cmap('value', color_palette, 0, max_count),
            line_color="#444444",  # Add thin border to enhance visibility
            line_width=0.5,
            source=source,
            visible=(year == years[0])  # Only the first year's data is initially visible
        )
        wedges_dict[year] = wedges
    
    # Create JavaScript callback to update chart
    callback = CustomJS(args=dict(wedges_dict=wedges_dict), code="""
        // Hide data for all years
        Object.keys(wedges_dict).forEach(function(year) {
            wedges_dict[year].visible = false;
        });
        
        // Show data for selected year
        var selected_year = cb_obj.value;
        wedges_dict[selected_year].visible = true;
    """)
    
    # Add callback to selector
    year_select.js_on_change('value', callback)
    
    # Create legend description
    legend_div = Div(
        text="""
        """,
        width=200
    )

        # Add hover tool
    hover = HoverTool(
        tooltips=[
            ("Incident count", "@value")
        ],
        renderers=[wedges_dict[years[0]]]  # Initially only apply to first year's data
    )
    p.add_tools(hover)
    
    # Create final layout, width should match the checkbox, otherwise not centered
    controls = column(year_select, legend_div, width=80, align="center", margin=(0, 0, 0, 0))
    layout = column(
        column(p, controls),  # Order indicates top-bottom position. matters
        align="center",
    )
    
    
    # Create HTML with all necessary JS
    html = file_html(layout, CDN, "Crime Time Distribution")
    
    # Save complete HTML file
    with open("crime_time_distribution.html", "w") as f:
        f.write(html)
    
    return layout

# Hyper parameters
## Define directories
SAVE_DIR = "./pics/"
DATA_DIR = "../../data_sf/"
CSV_NAME = 'combined_crime_data.csv'

# read it once only
df = pd.read_csv(DATA_DIR + CSV_NAME)

visualization = create_crime_time_visualization(df)