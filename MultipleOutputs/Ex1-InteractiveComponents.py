#######
# Objective: Create a dashboard that takes in two or more
# input values and returns their product as the output.
######

# Perform imports here:
from pandas.core import base
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd


# Launch the application:
app = dash.Dash()

# Create a Dash layout that contains input components
# and at least one output. Assign IDs to each component:

app.layout = html.Div([
    dcc.RangeSlider(
        id='slider-1',
        min=0,
        max=10,
        marks={i:str(i) for i in range(0,10)},
        value=[0,10]
    ), #default seletions,
     html.P(id='product')
], style={'width':'50%'})


# Create a Dash callback:

@app.callback(
     Output('product', 'children'),
    [Input('slider-1', 'value')])

def update_value(value_list):
    return value_list[0] * value_list[1]


# Add the server clause:

if __name__ == '__main__':
    app.run_server()
