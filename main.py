import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

# Create DataFrames from .csv files
df = pd.read_csv('tacoma.csv')
first_gen = pd.read_csv('first.csv')
second_gen = pd.read_csv('second.csv')
third_gen = pd.read_csv('third.csv')
PAGE_SIZE = 10


app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/amyoshino/pen/jzXypZ.css'])
server = app.server

# Layout of the app
app.layout = html.Div(children=[
    html.H1(
        children='''
            Data Visualizations
            ''',
        style={
            'textAlign': 'center',
            'color':'#1200AE'
        }
    ),

    html.H3(
        children='''
                Scatter Plot of Vehicle Prices in different States
                ''',
        style={
            'textAlign': 'center',
            'color': '#1200AE'
        }
    ),

    html.Div([
        dcc.Dropdown(
            id='option',
            options=[{'label': 'First Generation (1995-2004)', 'value': 'First Generation (1995-2004)'},
                     {'label': 'Second Generation (2005-2015)', 'value': 'Second Generation (2005-2015)'},
                     {'label': 'Third Generation (2016-Present)', 'value': 'Third Generation (2016-Present)'}],
            value='First Generation (1995-2004)'
        )
        ], style={'width': '48%', 'display': 'inline-block'}
    ),

    dcc.Graph(id='scatter_graph'),

    html.H3(
        children='''
                Relationship Between Vehicle Prices and Odometer
                ''',
        style={
            'textAlign': 'center',
            'color': '#1200AE'
        }
    ),

    html.Div([
            dcc.Dropdown(
                id='option_2',
                options=[{'label': 'First Generation (1995-2004)', 'value': 'First Generation (1995-2004)'},
                         {'label': 'Second Generation (2005-2015)', 'value': 'Second Generation (2005-2015)'},
                         {'label': 'Third Generation (2016-Present)', 'value': 'Third Generation (2016-Present)'}],
                value='First Generation (1995-2004)'
            )
            ], style={'width': '48%', 'display': 'inline-block'}
        ),

    dcc.Graph(id='scatter_graph_2'),

    html.H3(
        children='''
            Histogram of Vehicle Distribution in Each State
            ''',
        style={
            'textAlign': 'center',
            'color': '#1200AE'
        }
    ),

    html.Div([
            dcc.Dropdown(
                id='option_hist',
                options=[{'label': 'First Generation (1995-2004)', 'value': 'First Generation (1995-2004)'},
                         {'label': 'Second Generation (2005-2015)', 'value': 'Second Generation (2005-2015)'},
                         {'label': 'Third Generation (2016-Present)', 'value': 'Third Generation (2016-Present)'}],
                value='First Generation (1995-2004)'
            ),
            dcc.RadioItems(
                id='radio_hist',
                options=[{'label': 'Title Status', 'value': 'title_status'},
                         {'label': 'Transmission', 'value': 'transmission'},
                         {'label': 'Drive', 'value': 'drive'}],
                value='title_status'
            )
            ], style={'width': '48%', 'display': 'inline-block'}
        ),

    dcc.Graph(id='hist_graph'),

    html.H3(
        children='''
        Raw DataSet
        ''',
        style={
            'textAlign': 'center',
            'color': '#1200AE'
        }
    ),

    dash_table.DataTable(
        id='table-paging-and-sorting',
        columns=[
            {'name': i, 'id': i, 'deletable': True} for i in df.columns
        ],
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        },
        page_current=0,
        page_size=PAGE_SIZE,
        page_action='custom',

        sort_action='custom',
        sort_mode='single',
        sort_by=[]
    )

])


@app.callback(
    Output('scatter_graph', 'figure'),
    [Input('option', 'value')]
)
def update_graph(option):
    if option == 'First Generation (1995-2004)':
        fig = px.scatter(first_gen, x="state", y="price", color="title_status",
                         size='odometer', hover_data=['drive'])
    elif option == 'Second Generation (2005-2015)':
        fig = px.scatter(second_gen, x="state", y="price", color="title_status",
                         size='odometer', hover_data=['drive'])
    elif option == 'Third Generation (2016-Present)':
        fig = px.scatter(third_gen, x="state", y="price", color="title_status",
                         size='odometer', hover_data=['drive'])
    else:
        fig = px.scatter(df, x="state", y="price", color="title_status",
                         size='odometer', hover_data=['drive'])

    return fig


@app.callback(
    Output('scatter_graph_2', 'figure'),
    [Input('option_2', 'value')]
)
def update_graph(option_2):
    if option_2 == 'First Generation (1995-2004)':
        fig_2 = px.scatter(first_gen, x="odometer", y="price", color="title_status",
                           size='year', hover_data=['drive'])
    elif option_2 == 'Second Generation (2005-2015)':
        fig_2 = px.scatter(second_gen, x="odometer", y="price", color="title_status",
                           size='year', hover_data=['drive'])
    elif option_2 == 'Third Generation (2016-Present)':
        fig_2 = px.scatter(third_gen, x="odometer", y="price", color="title_status",
                           size='year', hover_data=['drive'])
    else:
        fig_2 = px.scatter(df, x="odometer", y="price", color="title_status",
                           size='year', hover_data=['drive'])

    return fig_2


@app.callback(
    Output('hist_graph', 'figure'),
    [Input('option_hist', 'value'),
     Input('radio_hist', 'value')]
)
def update_graph(option_hist, radio_hist):
    if option_hist == 'First Generation (1995-2004)':
        fig_3 = px.histogram(first_gen, x="state", color=radio_hist, hover_data=first_gen.columns)
    elif option_hist == 'Second Generation (2005-2015)':
        fig_3 = px.histogram(second_gen, x="state", color=radio_hist, hover_data=second_gen.columns)
    elif option_hist == 'Third Generation (2016-Present)':
        fig_3 = px.histogram(third_gen, x="state", color=radio_hist, hover_data=third_gen.columns)
    else:
        fig_3 = px.histogram(df, x="state", color=radio_hist, hover_data=df.columns)

    return fig_3


@app.callback(
    Output('table-paging-and-sorting', 'data'),
    [Input('table-paging-and-sorting', "page_current"),
     Input('table-paging-and-sorting', "page_size"),
     Input('table-paging-and-sorting', 'sort_by')])
def update_table(page_current, page_size, sort_by):
    if len(sort_by):
        dff = df.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = df

    return dff.iloc[
        page_current*page_size:(page_current + 1)*page_size
    ].to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)

