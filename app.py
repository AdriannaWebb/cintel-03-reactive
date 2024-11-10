###############
# Imports 
###############

import plotly.express as px
import seaborn as sns
from palmerpenguins import load_penguins
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from shiny import reactive


###############
# Load Data
###############

# Load the Palmer Penguins dataset
penguins_df = load_penguins()


######################
# Page Options & Title
######################

# Set the page options with the title "Penguin Data Exploration"
ui.page_opts(title="Webb of Data", fillable=True)


##################################
# Add sidebar for user interaction
##################################

# Set sidebar open by default
with ui.sidebar(position="right", bg="#D2E7F2", open="open"):  
    # Use the ui.h2() function to add a 2nd level header to the sidebar
    ui.h2("Sidebar")  

    # Dropdown to choose an attribute
    ui.input_selectize(
        "selected_attribute", "Choose an attribute",
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
        inline=True  
    )
    
    # Hyperlink to GitHub
    ui.hr()
    ui.a("GitHub Repository", href="https://github.com/AdriannaWebb/cintel-02-data/tree/main", target="_blank")


##################
# Main Content
##################

# Define reactive function for filtered data
@reactive.Calc
def filtered_data():
    # Filter DataFrame by selected species
    selected_species = input.selected_species_list()
    if selected_species:
        filtered_df = penguins_df[penguins_df['species'].isin(selected_species)]
    else:
        filtered_df = penguins_df
    return filtered_df

# Render DataTable and Datagrid within the same layout column.
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Data Table of Penguins")
        @render.data_frame
        def table():
            return filtered_data()
            
    with ui.card(full_screen=True):
        ui.card_header("Data Grid of Penguins")
        @render.data_frame
        def grid():
           return render.DataGrid(data=penguins_df)

# plotly and seaborn histogram within the same layout column.
            
# Render Plotly histogram with the selected attribute from the sidebar
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Distribution of Penguins Attribute")
        @render_plotly
        def plot1():
            # Use the selected attribute from the input for the x-axis
            selected_attr = input.selected_attribute()
            return px.histogram(filtered_data(), x=selected_attr, nbins=input.plotly_bin_count())
    
    with ui.card(full_screen=True):
        ui.card_header("Distribution of Penguin Species Studied")
        @render.plot
        def plot2():
            return sns.histplot(data=penguins_df, x="species")

# Render Plotly scatterplot within the same layout column.
with ui.layout_columns(height="1000px"):
    with ui.card(full_screen=True):
        ui.card_header("Bill Length vs. Body Mass Visual with Plotly")
        @render_plotly
        def plot3():
            return px.scatter(
                data_frame=filtered_data(),
                x="bill_length_mm", y="body_mass_g",
                color="species", hover_name="island", symbol="sex"
            )
