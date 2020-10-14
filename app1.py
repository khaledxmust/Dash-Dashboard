import os
import dash
import dash_auth
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State

# Credintials
USERNAME_PASSWORD_PAIRS = [
    ['JamesBond', '007'],['FEPS', '123']
]

# Main Dataframe
DF = pd.read_csv('app/data/pseudo_facebook.csv')
labels=['10-20','21-30','31-40','41-50','51-60','61-70','71-80','81-90','91-100','Over 100']
DF['age_group'] = pd.cut(DF.age,bins=np.arange(10,DF.age.max(),10),labels=labels,right=True)
groups = DF.age_group.value_counts()

# Other Dataframes
CDF  = pd.DataFrame(data= [DF['age_group'],DF['friend_count']]).T.groupby('age_group').sum().reset_index()
PDF = DF.pivot_table(values=['likes','mobile_likes','www_likes'],index='age_group').sort_index(ascending=False)

# Tenure
DF["tenure_yearly"]=DF["tenure"].apply(lambda x:x/365)
labels=['0-1 year','1-2 years','2-3 years','3-4 years','4-5 years','5-6 years','over 6 years']
#Note that the maximum tenure_yearly is 8.6.Thefore we set the upper limit to 9.
DF['tenure_group']=pd.cut(DF["tenure_yearly"],bins=[0,1,2,3,4,5,6,9],labels=labels,include_lowest=True)

#1. CSS Styling
# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f9f9f9'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#1c1c1c'
}

CARD_TEXT_STYLE = {
    'textAlign': 'left',
    'color': '#1c1c1c'
}

CARD_CONTAINER_STYLE = {
    'border-radius': '5px',
    'background-color': '#f9f9f9',
    'position': 'relative',
    'box-shadow': '2px 2px 2px lightgrey'
}
#2. Side bar
controls = dbc.FormGroup(
    [
        html.P('Dropdown', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            }, {
                'label': 'Value Two',
                'value': 'value2'
            },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value=['value1'],  # default value
            multi=True
        ),
        html.Br(),
        html.P('Range Slider', style={
            'textAlign': 'center'
        }),
        dcc.RangeSlider(
            id='range_slider',
            min=0,
            max=20,
            step=0.5,
            value=[5, 15]
        ),
        html.P('Check Box', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.Checklist(
            id='check_list',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            },
                {
                    'label': 'Value Two',
                    'value': 'value2'
                },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value=['value1', 'value2'],
            inline=True
        )]),
        html.Br(),
        html.P('Radio Items', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.RadioItems(
            id='radio_items',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            },
                {
                    'label': 'Value Two',
                    'value': 'value2'
                },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value='value1',
            style={
                'margin': 'auto'
            }
        )]),
        html.Br(),
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True
        ),
    ]
)

sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

#3. The 4 Cards
content_first_row = dbc.Row([
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_title_1', children=['Card tile 1'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_1', children=['Sample text.'], style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        , style=CARD_CONTAINER_STYLE),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(id='card_title_2', children=['Card tile 2'], className='card-title',
                                 style=CARD_TEXT_STYLE),
                        html.P(id='card_text_2', children=['Sample text.'], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        , style=CARD_CONTAINER_STYLE),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_title_3', children=['Card tile 3'], className='card-title',
                                 style=CARD_TEXT_STYLE),
                        html.P(id='card_text_3', children=['Sample text.'], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        , style=CARD_CONTAINER_STYLE),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_title_4', children=['Card tile 4'], className='card-title',
                                 style=CARD_TEXT_STYLE),
                        html.P(id='card_text_4', children=['Sample text.'], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]
        , style=CARD_CONTAINER_STYLE),
        md=3
    )
], style={'padding-bottom': '1%'})

content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_3'), md=12
        )
    ]
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_6', figure= make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])), md=12
        )
    ]
)

content_fourth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_1'), md=12
        )
    ]
)

content_fifth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_4', figure=go.Figure()), md=12
        )
    ]
)

#4. The Layout
content = html.Div(
    [
        html.H2('Neurocks Dashboard Demo', style={'textAlign': 'center', 'font-family': 'sans-serif', 'color': '#1c1c1c', 'padding-top': '5%'}),
        html.H4('Content Overview', style={'textAlign': 'center', 'font-family': 'sans-serif', 'color': '#1c1c1c', 'padding-bottom': '2%'}),
        #html.Hr(),
        content_first_row,
        content_second_row,
        content_third_row,
        content_fourth_row,
        content_fifth_row
    ],
    style=CONTENT_STYLE
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server

@app.callback(
    Output('graph_1', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    fig = {
        'data': [{
            'x': CDF['age_group'],
            'y': CDF['friend_count'],
            'type': 'bar'
        }], 'layout': {'title':'SegmentFriends Count'}
    }
    return fig

@app.callback(
    Output('graph_3', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])

def update_graph_3(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=PDF.index, y=PDF.likes,
                        mode='lines+markers',
                        name='Total Likes'))
    fig.add_trace(go.Scatter(x=PDF.index, y=PDF.mobile_likes,
                        mode='lines+markers',
                        name='Total Mobile Likes'))
    fig.add_trace(go.Scatter(x=PDF.index, y=PDF.www_likes,
                        mode='lines+markers',
                        name='Total Link Likes'))
    fig.update_layout(title_text='Likes Channels')
    return fig

@app.callback(
    Output('graph_4', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])

def update_graph_4(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    TDF =DF.groupby("tenure_group")["tenure_yearly"].count()
    Sum = TDF/TDF.sum()*100
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Sum.index, y=Sum,
                        mode='lines',
                        name='Tenure'))
    fig.update_layout(title_text='Tenure rate')
    return fig

@app.callback(
    Output('graph_6', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])

def update_graph_6(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    TDF = DF.groupby("tenure_group")["tenure_yearly"].count()
    Sum = TDF/TDF.sum()*100
    Cnt = DF.gender.value_counts()
    fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])

    fig.add_trace(go.Pie(labels=groups.keys().tolist(), values=groups.tolist(), name="Audience Segments"), 1, 1)
    fig.add_trace(go.Pie(labels=Sum.index, values=Sum, name="Tenure Rate"), 1, 2)
    fig.add_trace(go.Pie(labels=['Males', 'Females'], values=[(Cnt[0]/(Cnt[0]+Cnt[1]))*100,(Cnt[1]/(Cnt[0]+Cnt[1]))*100], name="Males vs Females Audience"), 1, 3)
    fig.update_layout(title_text='Further Insights')
    return fig

@app.callback(
    Output('card_title_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])

def update_card_title_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    return 'Total Users'

@app.callback(
    Output('card_text_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])

def update_card_text_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    users   = DF['gender'].count()
    return str(users)+' Fan Users'

@app.callback(
    Output('card_title_2', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])

def update_card_title_2(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    return 'Average age'

@app.callback(
    Output('card_text_2', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])

def update_card_text_2(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    x, y = groups.keys()[0], groups[1]
    return str(x) + ' : '+ str(y) + ' Users'

@app.callback(
    Output('card_title_3', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])

def update_card_title_3(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    return 'Gender'

@app.callback(
    Output('card_text_3', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])

def update_card_text_3(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    male   = int((DF['gender'].value_counts()[0]/DF['gender'].count())*100)
    return str(male)+'% Male Users'

@app.callback(
    Output('card_title_4', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])

def update_card_title_4(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    return 'Reactions'

@app.callback(
    Output('card_text_4', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])

def update_card_text_4(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    No   = int(DF['likes'].mean())
    return str(No)+' Likes Per Person'


if __name__ == '__main__':
    app.run_server()