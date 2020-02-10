import pandas as pd
import numpy as np
import mysql.connector
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import seaborn as sns
import dash_table
from dash.dependencies import Input, Output, State

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="98978789",
  database="hoki",
  use_pure=True
)

def generate_table(dataframe, page_size=10):
    return dash_table.DataTable(
        id='dataTable',
        columns=[{
            "name": i,
            "id": i
        } for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_action="native",
        page_current=0,
        page_size=page_size,
    )

mycursor = mydb.cursor()
tsa = pd.read_csv('C:/Users/Fikriem/Documents/Module 2 Purwadhika/tsa.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1('Ujian Modul 2 Dashboard TSA'),
        html.Div(children='''
        Created by: Fikrie
    '''),
        
        dcc.Tabs(
            children=[
                dcc.Tab(
                    value='Tab1',
                    label='Graph Example',

                    children=[
                        html.Div([html.Div([
                            dcc.Graph(id='example-graph',
                                      figure={
                                          'data': [{
                                              'x': tsa['Claim Type'],
                                              'y': tsa['Close Amount'],
                                              'type': 'bar',
                                              'name': 'smoker'
                                          }, {
                                              'x': tsa['Claim Type'],
                                              'y': tsa['Claim Amount'],
                                              'type': 'bar',
                                              'name': 'sex'
                                          }],
                                          'layout': {
                                              'title':
                                              'Claim Dash Data Visualization'
                                          }
                                      })
                        ],className="col-6")
                        ],className='row')  
                    ]),

                dcc.Tab(
                    value='Tab2',
                    label='Scatter chart',

                    children=[
                        html.Div(children=dcc.Graph(
                            id='graph-scatter',
                            figure={
                                'data': [
                                    go.Scatter(x=tsa["Claim Amount"],
                                               y=tsa['Close Amount'],
                                               mode='markers',
                                               color='Claim Type'
                                ],
                                'layout':
                                go.Layout(
                                    xaxis={'title': 'Claim Amount'},
                                    yaxis={'title': 'Close Amount'},
                                    title='TSA Dash Scatter Visualization',
                                    hovermode='closest')
                            }))
                    ]),

                dcc.Tab(value='Tab3',
                        label='Data Frame TSA',
                        
                        children=[
                            html.Div(children=[
                                html.Div([
                                    html.P('TSA'),
                                    dcc.Dropdown(value='',
                                                 id='Claim Site',
                                                 options=[{'label': 'Checkpoint','value': 'Checkpoint'}, 
                                                 {'label': 'Other','value': 'Other'},
                                                 {'label': 'Checked Baggage','value': 'Checked Baggage'},
                                                 {'label': 'Motor Vehicle','value': 'Motor Vehicle'},
                                                 {'label': 'Bus Station','value': 'Bus Station'},
                                                 ])
                                ],
                                         className='col-3'),
                                
                                html.Div([
                                    html.P('Sex'),
                                    dcc.Dropdown(value='',
                                                 id='filter-sex',
                                                 options=[{'label': 'Female','value': 'Female'}, 
                                                 {'label': 'Male','value': 'Male'},
                                                 {'label': 'None','value': ''}])
                                ],
                                         className='col-3'),
                                
                                html.Div([
                                    html.P('Day'),
                                    dcc.Dropdown(value='',
                                                 id='filter-day',
                                                 options=[{'label': 'Thur','value': 'Thur'}, 
                                                 {'label': 'Fri','value': 'Fri'},                     
                                                 {'label': 'Sat','value': 'Sat'},
                                                 {'label': 'Sun','value': 'Sun'},
                                                 {'label': 'None','value': ''}])
                                ],
                                         className='col-3'),
                                html.Div([
                                    html.P('Time'),
                                    dcc.Dropdown(value='',
                                                 id='filter-time',
                                                 options=[{'label': 'Lunch','value': 'Lunch'}, 
                                                 {'label': 'Dinner','value': 'Dinner'},
                                                 {'label': 'None','value': ''}])
                                ],
                                         className='col-3')

                            ],
                                     className='row'),
                            html.Br(),
                            html.Div([
                                html.P('Max Rows:'),
                                dcc.Input(id ='filter-row',
                                          type = 'number', 
                                          value = 10)
                            ], className = 'row col-3'),

                            html.Div(children =[
                                    html.Button('search',id = 'filter')
                             ],className = 'row col-4'),
                             
                            html.Div(id='div-table',
                                     children=[generate_table(tips)])
                        ])
            ],
            ## Tabs Content Style
            content_style={
                'fontFamily': 'Arial',
                'borderBottom': '1px solid #d6d6d6',
                'borderLeft': '1px solid #d6d6d6',
                'borderRight': '1px solid #d6d6d6',
                'padding': '44px'
            })
    ],
    #Div Paling luar Style
    style={
        'maxWidth': '1200px',
        'margin': '0 auto'
    })

@app.callback(
    Output(component_id = 'div-table', component_property = 'children'),
    [Input(component_id = 'filter', component_property = 'n_clicks')],
    [State(component_id = 'filter-row', component_property = 'value'), 
    State(component_id = 'filter-smoker', component_property = 'value'),
    State(component_id = 'filter-sex', component_property = 'value'),
    State(component_id = 'filter-day', component_property = 'value'),
    State(component_id = 'filter-time', component_property = 'value')]
)
def update_table(n_clicks,row, smoker, sex, day, time):
    tips = sns.load_dataset('tips')
    # if smoker == '' and sex == '' and day == '' and time == '':
    #     children = [generate_table(tips, page_size = row)]
    # elif smoker == '' and sex == '' and day == '' and time != '':
    #     children = [generate_table(tips[tips['time'] == time], page_size = row)]
    # elif smoker == '' and sex == '' and day != '' and time == '':
    #     children = [generate_table(tips[tips['day'] == day], page_size = row)]
    # elif smoker == '' and sex != '' and day == '' and time == '':
    #     children = [generate_table(tips[tips['sex'] == sex], page_size = row)]
    # elif smoker != '' and sex == '' and day == '' and time == '':
    #     children = [generate_table(tips[tips['smoker'] == smoker], page_size = row)]              
    # elif smoker == '' and sex == '' and day != '' and time != '':
    #     children = [generate_table(tips[(tips['time'] == time) & (tips['day'] == day)], page_size = row)]
    # elif smoker == '' and sex != '' and day == '' and time != '':
    #     children = [generate_table(tips[(tips['time'] == time) & (tips['sex'] == sex)], page_size = row)]
    # elif smoker != '' and sex == '' and day == '' and time != '':
    #     children = [generate_table(tips[(tips['time'] == time) & (tips['smoker'] == smoker)], page_size = row)]
    # elif smoker == '' and sex != '' and day != '' and time== '':
    #     children = [generate_table(tips[(tips['day'] == day) & (tips['sex'] == sex)], page_size = row)]
    # elif smoker != '' and sex == '' and day != '' and time== '':
    #     children = [generate_table(tips[(tips['day'] == day) & (tips['smoker'] == smoker)], page_size = row)]
    # elif smoker != '' and sex != '' and day == '' and time == '':
    #     children = [generate_table(tips[(tips['smoker'] == smoker) & (tips['sex'] == sex)], page_size = row)]                  
    # elif smoker == '' and sex != '' and day != '' and time != '':
    #     children = [generate_table(tips[(tips['time'] == time) & (tips['day'] == day) & (tips['sex'] == sex)], page_size = row)]
    # elif smoker != '' and sex == '' and day != '' and time != '':
    #     children = [generate_table(tips[(tips['time'] == time) & (tips['day'] == day) & (tips['smoker'] == smoker)], page_size = row)]
    # elif smoker != '' and sex != '' and day == '' and time != '':
    #     children = [generate_table(tips[(tips['time'] == time) & (tips['sex'] == sex) & (tips['smoker'] == smoker)], page_size = row)]
    # elif smoker != '' and sex != '' and day != '' and time == '':
    #     children = [generate_table(tips[(tips['sex'] == sex) & (tips['day'] == day) & (tips['smoker'] == smoker)], page_size = row)]                               
    # else:
    #     children = [generate_table(tips[(tips['sex'] == sex) & (tips['day'] == day) & (tips['smoker'] == smoker) & (tips['time'] == time)], page_size = row)]               
    # return children 
    if smoker != '':
        tips = tips[tips['smoker'] == smoker]
    if sex != '':
        tips = tips[tips['sex'] == sex]
    if day != '':
        tips = tips[tips['day'] == day]
    if time != '':
        tips = tips[tips['time'] == time]
    children = [generate_table(tips, page_size = row)]
    return children
    
if __name__ == '__main__':
    app.run_server(debug=True)