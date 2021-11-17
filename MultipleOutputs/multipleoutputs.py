from pandas.core import base
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import base64

df = pd.read_csv('/Users/thamyvas/Desktop/Plotly-Dashboards-with-Dash-master/Data/wheels.csv')

#create the application

app = dash.Dash()

def encode_img(image_file):
    encoded = base64.b64encode(open(image_file,'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())


app.layout = html.Div([
        #from core componets get radio items, id for input
        dcc.RadioItems(
        id='wheels',
        #list of dictionaries, for unique values values in column wheels it will show a label and the value
        options=[{'label': i, 'value': i} for i in df['wheels'].unique()],
         #give a default value
        value=1
    ),   
        html.Div(id='wheels-output'),  #display the outputs, id is for output

        html.Hr(), #line break
        dcc.RadioItems(
            id='colors',#another set of radiotems. For the colors
            options=[{'label': i, 'value': i} for i in df['color'].unique()], #list of dictionaries, for unique values values in column wheels it will show a label and the value
            value='blue' #value
    ),
        html.Div(id = 'colors-output'),
        html.Img(id='display-image', src='children', height = 300)


], style={'fontFamily': 'helvetica', 'fontSize':18}) #add style to the div, optional

#create 2 functions One for the wheels and one for the color values.
@app.callback(Output('wheels-output', 'children'),
              [Input('wheels', 'value')]
              )
def callback_a(wheels_value):
    return "You chose {} ".format(wheels_value)

@app.callback(Output('colors-output', 'children'),
              [Input('colors', 'value')]
              )
def callback_b(colors_value):
    return "You chose {} ".format(colors_value)


#call images
@app.callback(Output('display-image', 'src'),
              [Input('wheels', 'value'),
               Input('colors', 'value')])
               
def callback_img(wheel,color):
    path = '../data/images/'
    return encode_img(path+df[(df['wheels']==wheel) & \
    (df['color']==color)]['image'].values[0])


if __name__ == '__main__':
    app.run_server()

