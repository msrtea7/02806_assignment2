import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, Title, HoverTool
from bokeh.palettes import Category10

# Hyper parameters
## Define directories

DATA_DIR = "../../data_sf/"
CSV_NAME = 'combined_crime_data.csv'

# read it once only
df = pd.read_csv(DATA_DIR + CSV_NAME)

# Convert date to datetime
df['Incident Date'] = pd.to_datetime(df['Incident Date'])

df['month_year'] = df['Incident Date'].dt.strftime('%Y-%m')
top_categories = df['Incident Category'].value_counts().nlargest(6).index.tolist()
filtered_df = df[df['Incident Category'].isin(top_categories)]

# Aggregate by month and category
monthly_data = filtered_df.groupby(['month_year', 'Incident Category']).size().reset_index(name='count')
monthly_data['date'] = pd.to_datetime(monthly_data['month_year'] + '-01')
monthly_data = monthly_data.sort_values(['Incident Category', 'date'])


###########################################################################################


# Set the dimensions of the figure - increase width for better display of annual markers
plot_width = 1200  # Custom width
plot_height = 600  # Custom height


# Create figure with transparent background
p = figure(
    width=plot_width, height=plot_height,
    x_axis_type='datetime',
    # tools='pan,wheel_zoom,box_zoom,reset,save',
    tools='pan,box_zoom,reset,save,zoom_in,zoom_out',
    title='Monthly Crime Trends (Top 6 Categories, 2003-2025)',
    background_fill_alpha=0,
    border_fill_alpha=0
)


# Plot lines for each category
lines = []
colors = Category10[6]
for i, category in enumerate(top_categories):
    category_data = monthly_data[monthly_data['Incident Category'] == category]
    source = ColumnDataSource({
        'x': category_data['date'],
        'y': category_data['count']
    })
    
    line = p.line(
        'x', 'y', 
        source=source, 
        color=colors[i], 
        line_width=2, 
        alpha=1,
        name=category,
        legend_label=category,
        # Only keep 'motor vehicle theft' visible, set other categories to muted
        visible=True,
        muted=category.lower() != 'motor vehicle theft'
    )
    lines.append(line)

# Configure axes and legend
p.xaxis.axis_label = "Date"
p.yaxis.axis_label = "Number of Incidents"
p.legend.location = "top_left"
p.legend.click_policy="mute"
p.legend.background_fill_alpha = 0  # Completely transparent background
p.legend.border_line_alpha = 0      # Optional: transparent border


######
hover = HoverTool()
hover.tooltips = [
    ("Category", "$name"),
    ("Date", "@x{%F}"),  # Format as YYYY-MM-DD
    ("Incidents", "@y")
]
hover.formatters = {
    "@x": "datetime"  # Use datetime formatter
}
p.add_tools(hover)


output_file('crime_trends.html')
save(p)