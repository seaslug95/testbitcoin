# https://dash-bootstrap-components.opensource.faculty.ai/examples/iris/
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/form/

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
import re
import module.mymodule as mymodule

previous_days = 5
money_ini = 1000
bitcoin_ini = 0.1
prop_ini = 0.05

df = pd.read_csv('./data/bitcoin_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.rename(columns={'Close': 'Closing Price'}, inplace=True)
df.set_index('Date', inplace=True)
df = df.squeeze('columns')

date_first = df.index[0]
date_last = df.index[-1]

df_simu = mymodule.mysimu(df, previous_days, money_ini, bitcoin_ini, prop_ini)

df_simu['Relative Closing Price'] = df_simu['Closing Price']/df_simu['Closing Price'][0]
df_simu['Relative Total Worth'] = df_simu['Total Worth']/df_simu['Total Worth'][0]
df_simu['Relative Time'] = [x/(len(df_simu.index)-1) for x in [*range(len(df_simu.index))]]

fig2 = px.scatter(df_simu, 
                    x='Relative Closing Price', 
                    y='Relative Total Worth',
                    color='Relative Time', 
                    color_continuous_scale=px.colors.sequential.Viridis,
                    title='Performance against "Buy and Hold" across selected period.')
line = df_simu['Relative Closing Price'] if df_simu['Relative Closing Price'].max() < df_simu['Relative Total Worth'].max() else df_simu['Relative Total Worth']
fig2.add_scatter(x=line, y=line, mode='lines', opacity=0.5, name='Unitary reference')
fig2.update(layout_showlegend=False)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
#app = dash.Dash()

SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'right': 0,
    'bottom': 0,
    'left': 0,
    # 'width': '20%',
    'width': '18rem',
    #'padding': '20px 10px',
    #'padding': '2rem 1rem',
    'background-color': '#f8f9fa'
}

CONTENT_STYLE = {
    # 'margin-left': '20%',
    'margin-left': '18rem',
    #'margin-right': '0%',
    #'padding': '20px 10px'
    #'padding': '2rem 1rem'
}

TEXT_STYLE = {
    'textAlign': 'center',
    # 'color': '#191970'
    'color': '#A8A8A8' #https://www.w3schools.com/colors/colors_shades.asp
}

graph_ts = dcc.Graph(
    id = 'output-timeseries',
    figure = px.line(df_simu, 
                    x=df_simu.index, 
                    y='Closing Price', 
                    title='Bitcoin daily closing prices across selected period.'
    ).update_xaxes(rangeslider_visible=True)
)

graph_worth = dcc.Graph(
        id='output-simu',
        figure=px.line(df_simu,
            x=df_simu.index, 
            y='Total Worth').update_xaxes(rangeslider_visible=True)
)

graph_perf = dcc.Graph(
        id='output-simu2',
        figure=fig2
)

dropdown = dcc.Dropdown(
        id='label-simu',
        options=[
            {'label': 'Total Worth', 'value': 'Total Worth'},
            {'label': 'Money', 'value': 'Money'},
            {'label': 'Bitcoin', 'value': 'Bitcoin'}
        ],
        value='Total Worth'
)

filter_date = dcc.DatePickerRange(
                        id='my-date-picker-range',
                        min_date_allowed=date_first,
                        max_date_allowed=date_last,
                        initial_visible_month=date_last,
                        start_date=date_first,
                        end_date=date_last
)

filter_money = dbc.Input(
                        id='num-money',
                        type='number',
                        value=money_ini
)

filter_bitcoin = dbc.Input(
                    id='num-bitcoin',
                    type='number',
                    value=bitcoin_ini
)

filter_days = dbc.Input(
                        id='num-days',
                        type='number',
                        value=previous_days
)

filter_prop = dbc.Input(
                        id='prop_sellbuy',
                        type='number',
                        value=prop_ini
)

controls = dbc.FormGroup(
    [
        html.P('Dates Range:', style={
            'textAlign': 'center'
        }),
        filter_date,
        html.Br(),
        html.Br(),
        html.P('Initial Money:', style={
            'textAlign': 'center'
        }),
        filter_money,
        html.Br(),
        html.P('Initial Bitcoin:', style={
            'textAlign': 'center'
        }),
        filter_bitcoin,
        html.Br(),
        html.P('Number Days Accounted:', style={
            'textAlign': 'center'
        }),
        filter_days,
        html.Br(),
        html.P('Transaction Proportion:', style={
            'textAlign': 'center'
        }),
        filter_prop,
        html.Br(),
        # html.A('User Manual (README)', href=f'https://github.com/VicCGI/bitcoin', target="_blank"),
        # html.Div([
        #     html.A("Link to external site", href='https://plot.ly', target="_blank")
        # ]),
        # html.P('TEST', style={
        #     'textAlign': 'center'
        # }),
        dbc.Button(
            children='User Manual (README)',
            color='primary',
            href=f'https://github.com/VicCGI/bitcoin',
            target="_blank",
            block=True
        ),
    ]
)

sidebar = html.Div(
    [
        html.H2(
            'Parameters', 
            style=TEXT_STYLE
            ),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

content_row_1 = dbc.Row(
    [
        dbc.Col(
            graph_ts
        ),
    ]
)

content_row_2 = dbc.Row(
    [
        dbc.Col(
            dropdown
        ),
    ]
)

content_row_3 = dbc.Row(
    [
        dbc.Col(
            graph_worth
        ),
    ]
)

content_row_4 = dbc.Row(
    [
        dbc.Col(
            graph_perf
        ),
    ]
)

content = html.Div(
    [
        html.H2('Bitcoin Dashboard',
            style={'textAlign': 'center'}),
        html.Hr(),
        content_row_1,
        content_row_2,
        content_row_3,
        content_row_4,
    ],
    style=CONTENT_STYLE
)

app.layout = dbc.Container(
    [
        sidebar,
        content
    ],
    fluid = True
)

@app.callback(
    dash.dependencies.Output('output-timeseries', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output_ts(start_date, end_date):
    df_upd = df.loc[start_date:end_date]

    fig = px.line(df_upd, 
                    x=df_upd.index, 
                    y='Closing Price', 
                    #color_discrete_sequence=['goldenrod'],
                    title='Bitcoin daily closing prices across selected period.').update_xaxes(rangeslider_visible=True)

    fig.update_xaxes(range=[df_upd.index.min(), df_upd.index.max()])

    fig.update_yaxes(range=[
        df_upd.min() - 0.05*df_upd.min() if df_upd.min() - 0.05*df_upd.min() >= 0 else 0, 
        df_upd.max() + 0.05*df_upd.max()])

    return fig

@app.callback(
    [dash.dependencies.Output('output-simu', 'figure'),
    dash.dependencies.Output('output-simu2', 'figure')],
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date'),
     dash.dependencies.Input('num-money', 'value'),
     dash.dependencies.Input('num-bitcoin', 'value'),
     dash.dependencies.Input('num-days', 'value'),
     dash.dependencies.Input('label-simu', 'value'),
     dash.dependencies.Input('prop_sellbuy', 'value')])
def update_output_simu(start_date, end_date, money, bitcoin, previous_days, label_simu, prop):
    start_date = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
    end_date = dt.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
    #starting_date = start_date + timedelta(days=round(previous_days))

    df_upd = df.loc[start_date:end_date]

    df_simu = mymodule.mysimu(df_upd, previous_days, money, bitcoin, prop)

    fig = px.line(df_simu, 
                    x=df_simu.index, 
                    y=label_simu, 
                    #color_discrete_sequence=['goldenrod'],
                    title=label_simu + ' across selected period.').update_xaxes(rangeslider_visible=True)
    fig.update_xaxes(range=[df_simu.index.min(), df_simu.index.max()])

    fig.update_yaxes(range=[
        df_simu[label_simu].min() - 0.05*df_simu[label_simu].min() if df_simu[label_simu].min() - 0.05*df_simu[label_simu].min() >= 0 else 0, 
        df_simu[label_simu].max() + 0.05*df_simu[label_simu].max()])

    df_simu['Relative Closing Price'] = df_simu['Closing Price']/df_simu['Closing Price'][0]
    df_simu['Relative Total Worth'] = df_simu['Total Worth']/df_simu['Total Worth'][0]
    df_simu['Relative Time'] = [x/(len(df_simu)-1) for x in [*range(len(df_simu))]]

    fig2 = px.scatter(df_simu, 
                    x='Relative Closing Price', 
                    y='Relative Total Worth',
                    color='Relative Time', 
                    color_continuous_scale=px.colors.sequential.Viridis,
                    title='Performance against "Buy and Hold" across selected period.')
    line = df_simu['Relative Closing Price'] if df_simu['Relative Closing Price'].max() < df_simu['Relative Total Worth'].max() else df_simu['Relative Total Worth']
    fig2.add_scatter(x=line, y=line, mode='lines', opacity=0.5, name='Unitary reference')
    fig2.update(layout_showlegend=False)
    #fig2.add_scatter(x=df_simu['Close_rel'], y=df_simu['Close_rel'], mode='lines')

    return fig, fig2


if __name__ == '__main__':
    app.run_server(debug=False)
