import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt

import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output,State
from dash.exceptions import PreventUpdate


# dash instance
app = dash.Dash(__name__)
server=app.server
item1=html.Div(
          [
            html.P("Welcome!", className="start"),
            html.Img(src=app.get_asset_url('image.png')),
            html.Br(),
            html.Div([
              # stock code input
              html.Div(["Enter Stock Code: ",
              dcc.Input(id='stock-input', value='', type='text')]),
              html.Button('Submit', id='submit-stock-btn'),
              
            ],className="stockinput"),
            html.Div([
              
              # Date range picker input
              dcc.DatePickerRange(
              id="date-picker-range",
              display_format="YYYY-MM-DD",
              start_date_placeholder_text="Start Period",
              end_date_placeholder_text="End Period",
              calendar_orientation='vertical',
             ),
                       
            ]),
            html.Div([
              # Stock price button
              html.Button('Stock Price', id='stock-price-btn', n_clicks=0),

              # Indicators button
              html.Button('Indicators', id='indicator-btn', n_clicks=0),
              html.Br(),
              # Number of days of forecast input
              dcc.Input(id='noofdays-input', value='No. of Days', type='text'),

              # Forecast button
              html.Button('Forecast', id='forecast', n_clicks=0),

            ]),
          ],
        className="inputs")

item2=html.Div(
          [
            html.H1("Stock Price Prediction", className="heading"),
            html.H5("Please Enter Legitimate Stock Code"),
            html.Div(
                  [  # Logo
                    # Company Name
                  ],id="stock-name",
                className="header"),
            html.Div( #Description
              id="stock-description", className="decription_ticker"),
            html.Div(
                # Stock price plot
            dcc.Graph (id="stock-price-plot")),
            html.Div(
                # Indcator plot
                dcc.Graph (id="indicator-plot")),
            html.Div([
                # Forecast plot
            ], id="forecast-plot")
          ],
        className="header")

        
app.layout = html.Div([item1, item2],className="container")
# download


@app.callback(Output('stock-name', 'children'),
              Output('stock-description', 'children'),
              Input('submit-stock-btn', 'n_clicks'),
              State('stock-input', 'value'))
def about_company(n_clicks, input1):
    if n_clicks is None:
        raise PreventUpdate
    else:
        ticker = yf.Ticker(input1)
        inf = ticker.info
        df = pd.DataFrame().from_dict(inf, orient="index").T
        print(df.head)
        return df.shortName, df.longBusinessSummary

@app.callback(Output('stock-price-plot', 'figure'),           
              Input('stock-price-btn','n_clicks'),
              State('date-picker-range', 'start_date'),
              State('date-picker-range', 'end_date'),
              State('stock-input', 'value'))
             
def stocks_graph(n_clicks,start_date,end_date,value):
    if n_clicks is None:
        raise PreventUpdate
    else:
        df = yf.download(value,start_date,end_date)
        print(df)
        df.reset_index(inplace=True)
        fig = get_stock_price_fig(df)
    return fig # plot the graph of fig using DCC function

def get_stock_price_fig(df):
    fig = px.line(df,
                  x= df['Date'],
                  y=[df['Open'],df['Close']],
                  
                  title="Closing and Opening Price vs Date")
    return fig

@app.callback(Output('indicator-plot', 'figure'),           
              Input('indicator-btn','n_clicks'),
              State('date-picker-range', 'start_date'),
              State('date-picker-range', 'end_date'),
              State('stock-input', 'value'))
             
def EMA_graph(n_clicks,start_date,end_date,value):
    if n_clicks is None:
        raise PreventUpdate
    else:
        df = yf.download(value,start_date,end_date)
        df.reset_index(inplace=True)
        fig = get_EMA_fig(df)
    return fig # plot the graph of fig using DCC function

def get_EMA_fig(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,
                   x=df['Date'],
                   y= df['EWA_20'],
                   title="Exponential Moving Average vs Date")

    fig.update_traces(mode= 'lines+markers')
    
    return fig

    
if __name__ == '__main__':
    app.run_server(debug=True)