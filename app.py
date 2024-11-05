import plotly.express as px
import seaborn as sns
from palmerpenguins import load_penguins
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from shiny import reactive



# Load the Palmer Penguins dataset
penguins_df = load_penguins()

# Set the page options with the title "Penguin Data Exploration"
ui.page_opts(title="Webb of Data", fillable=True)



# Add a Shiny UI sidebar for user interaction

# Set sidebar open by default
with ui.sidebar(position="right", bg="#D2E7F2", open="open"):  
    # Use the ui.h2() function to add a 2nd level header to the sidebar
    ui.h2("Sidebar")  # Sidebar header

    # Use ui.input_selectize() to create a dropdown input to choose a column
    
    ui.input_selectize(
        "selected_attribute", # Input Name
        "Choose an attribute", # Label for the dropdown
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]  
    )

    # Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
   
    ui.input_numeric(
        "plotly_bin_count", # Input Name
        "Number of Plotly Histogram Bins", # Label
        value=30  # Default value
    )

    # Use ui.input_slider() to create a slider input for the number of Seaborn bins
   
    ui.input_slider(
        "seaborn_bin_count", # Input Name
        "Number of Seaborn Histogram Bins",  # Label
        min=10, # Minimum value
        max=100, # Maximum value
        value=30 # Default value
    )

    # Use ui.input_checkbox_group() to create a checkbox group input to filter the species
   
    ui.input_checkbox_group(
        "selected_species_list", # Input Name
        "Filter by Species", # Label
        ["Adelie", "Gentoo", "Chinstrap"], # Options
        selected=["Adelie", "Gentoo", "Chinstrap"],  # Default selection
        inline=True  # Display inline
    )
    
    # 
    ui.hr()

    # Add a hyperlink to your GitHub repo
    ui.a(
        "GitHub Repository",                      # Link text
        href="https://github.com/AdriannaWebb/cintel-02-data/tree/main",  # Link URL
        target="_blank"                           # Open link in a new tab
    )


# Main Content
  
# Render DataTable and Datagrid within the same layout column.
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Data Table of Penguins")
        @reactive.event(input.selected_species_list)
        def species_data():
            return penguins_df[penguins_df['species'].isin(input.selected_species_list())]
# this render.data_frame decorator returns filtered data 
        @render.data_frame
        def table():
           return species_data() 
            
    with ui.card(full_screen=True):
        ui.card_header("Data Grid of Penguins")
        @render.data_frame
        def grid():
           return render.DataGrid(data=penguins_df)

# Render plotly and seaborn histogram within the same layout column.
            
with ui.layout_columns():
     with ui.card(full_screen=True):
        ui.card_header("Distribution of Penguins bill length")
        @render_plotly
        def plot1():
            return px.histogram(penguins_df, x="bill_length_mm",nbins=input.plotly_bin_count())
            
     with ui.card(full_screen=True):
        ui.card_header("Distribution of Penguin Species Studied")
        @render.plot
        def plot2():
            return sns.histplot(data=penguins_df, x="species")

# Render plotly and seaborn scatterplot within the same layout column.
            
with ui.layout_columns(height="1000px"):
     with ui.card(full_screen=True):
        ui.card_header("Bill Length vs. Body Mass Visual with Plotly")
        @render_plotly
        def plot3():
         return px.scatter(data_frame=penguins_df,x="bill_length_mm", y="body_mass_g",color="species",hover_name="island",symbol="sex")
