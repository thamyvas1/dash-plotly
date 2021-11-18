import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
import dash_bootstrap_components as dbc
from datetime import datetime
import pandas as pd

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Stock Ticker Dashboard",
    brand_href="#",
    color="primary",
    dark=True,
)

nsdq = pd.read_csv('../data/NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    options.append({'label': '{} {}'.format(
        tic, nsdq.loc[tic]['Name']), 'value': tic})

app.layout = dbc.Container([navbar,
    html.Div([html.H1('Milestone Dashboard', style={
             'textAlign': 'center', 'color': 'black'})]),

    html.Br(),

    html.Div(
        [
            dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Enter a stock symbol:', className="lead",
                               style={'paddingRight': '30px'}),
                        dcc.Dropdown(
                         id='my_ticker_symbol',
                         options=options,
                         value=['TSLA'],
                         multi=True),

                    ], style={'display': 'inline-block', 'flex-direction': 'column', 'verticalAlign': 'top', 'width': '30%'}),
                    ]),
                html.Br(),
                dbc.Col(
                    [
                        html.P('Select start and end dates:',className="lead"),
                        dcc.DatePickerRange(
                                            id='my_date_picker',
                                            min_date_allowed=datetime(2015, 1, 1),
                                            max_date_allowed=datetime.today(),
                                            start_date=datetime(2018, 1, 1),
                                            end_date=datetime.today())], style={'display': 'inline-block'}),

                        html.Button(id='submit-button',
                                    n_clicks=0,
                                    children='Submit',
                                    style={'fontSize': 24, 'marginLeft': '30px'}),
                    ]),
                   

    dcc.Graph(id='my_graph',
             figure={'data': [{'x': [1, 2], 'y': [3, 1]}]}
             )

], className="p-4",)

@ app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_ticker_symbol', 'value'),
     State('my_date_picker', 'start_date'),
     State('my_date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start=datetime.strptime(start_date[:10], '%Y-%m-%d')
    end=datetime.strptime(end_date[:10], '%Y-%m-%d')

    traces=[]
    for tic in stock_ticker:
        df=web.DataReader(tic, 'yahoo', start, end)
        traces.append({'x': df.index, 'y': df['Close'], 'name':tic})
    fig={
        'data': traces,
        'layout': {'title': ', '.join(stock_ticker)+' Closing Prices'}
    }
    return fig

if __name__ == '__main__':
    app.run_server()
