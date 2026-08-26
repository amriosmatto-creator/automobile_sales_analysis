"""
DV0101EN — Data Visualization with Python
Final Assignment, Part 2: Automobile Sales Statistics Dashboard (Plotly + Dash)

Two reports, selectable from a dropdown:
  1. Yearly Automobile Sales Statistics  (year dropdown enabled)
  2. Recession Period Statistics         (year dropdown disabled)

Each report renders four plots in a 2x2 grid.
"""

# Import required libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------------------------------
# Load the data using pandas
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/'
    'IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/'
    'historical_automobile_sales.csv'
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

# ---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'},
]

# List of years
year_list = [i for i in range(1980, 2024, 1)]

# ---------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    # TASK 2.1: Add title to the dashboard
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24},
    ),

    # TASK 2.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type',
            style={
                'width': '80%',
                'padding': '3px',
                'font-size': '20px',
                'text-align-last': 'center',
            },
        ),
    ]),

    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='Select-year',
            placeholder='Select-year',
            style={
                'width': '80%',
                'padding': '3px',
                'font-size': '20px',
                'text-align-last': 'center',
            },
        ),
    ]),

    # TASK 2.3: Add a division for output display
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ]),
])


# ---------------------------------------------------------------------------------
# TASK 2.4: Creating Callbacks
# Callback to enable/disable the year dropdown based on the selected report type
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'),
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True


# Callback to update the output container based on the selected statistics and year
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [
        Input(component_id='dropdown-statistics', component_property='value'),
        Input(component_id='select-year', component_property='value'),
    ],
)
def update_output_container(selected_statistics, input_year):
    # -------------------------------------------------------------------------
    # TASK 2.5: Create and display graphs for Recession Report Statistics
    # -------------------------------------------------------------------------
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales fluctuation over Recession Period (year wise) — line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales Fluctuation over Recession Period",
            )
        )

        # Plot 2: Average number of vehicles sold by vehicle type — bar chart
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Number of Vehicles Sold by Vehicle Type",
            )
        )

        # Plot 3: Total expenditure share by vehicle type during recessions — pie chart
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Total Expenditure Share by Vehicle Type During Recessions",
            )
        )

        # Plot 4: Effect of unemployment rate on vehicle type and sales — bar chart
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={
                    'unemployment_rate': 'Unemployment Rate',
                    'Automobile_Sales': 'Average Automobile Sales',
                },
                title='Effect of Unemployment Rate on Vehicle Type and Sales',
            )
        )

        return [
            html.Div(
                className='chart-item',
                children=[html.Div(children=R_chart1), html.Div(children=R_chart2)],
                style={'display': 'flex'},
            ),
            html.Div(
                className='chart-item',
                children=[html.Div(children=R_chart3), html.Div(children=R_chart4)],
                style={'display': 'flex'},
            ),
        ]

    # -------------------------------------------------------------------------
    # TASK 2.6: Create and display graphs for Yearly Report Statistics
    # -------------------------------------------------------------------------
    elif (input_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly average automobile sales for the whole period — line chart
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Yearly Average Automobile Sales',
            )
        )

        # Plot 2: Total monthly automobile sales for the selected year — line chart
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales',
            )
        )

        # Plot 3: Average vehicles sold by vehicle type in the selected year — bar chart
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year),
            )
        )

        # Plot 4: Total advertisement expenditure for each vehicle type — pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure for Each Vehicle',
            )
        )

        return [
            html.Div(
                className='chart-item',
                children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)],
                style={'display': 'flex'},
            ),
            html.Div(
                className='chart-item',
                children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)],
                style={'display': 'flex'},
            ),
        ]

    # Nothing selected yet
    else:
        return None


# ---------------------------------------------------------------------------------
# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
