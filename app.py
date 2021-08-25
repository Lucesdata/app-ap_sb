import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.4) pip install plotly==4.5.4
import plotly.express as px
import numpy as np

import dash             #(version 1.9.1) pip install dash==1.9.1
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output



df = pd.read_csv("aguatratadalasirena.csv")
pd.to_datetime(df['Time'],errors='ignore')
pd.to_datetime(df['Date'],errors='ignore')

dff = df.groupby('Date', as_index=False)[['AP03AT9002PH','AP03AT9002TURB']].max()


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Avocado Analytics: Understand Your Avocados!"

app.layout = html.Div([
    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=dff.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns
            ],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 20,
            style_table={'height': '300px', 'overflowY': 'auto'},
            fixed_rows={'headers': True},
            # page_action='none',
            # style_cell={
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows={ 'headers': True, 'data': 0 },
            # virtualization=False,
            style_cell_conditional=[
                {'if': {'column_id': 'Date'},
                 'width': '40%', 'textAlign': 'left'},
                {'if': {'column_id': 'AP03AT9002PH'},
                 'width': '30%', 'textAlign': 'left'},
                {'if': {'column_id': 'AP03AT9002TURB'},
                 'width': '30%', 'textAlign': 'left'},
            ],
        ),
    ],className='row'),
    
    html.Div([
        html.Div([
        dcc.Dropdown(id='linedropdown',
            options=[
                     {'label': 'AP03AT9002PH', 'value': 'AP03AT9002PH'},
                     {'label': 'AP03AT9002TURB', 'value': 'AP03AT9002TURB'}
            ],
            value='AP03AT9002TURB',
            multi=False,
            clearable=False
        ),
        ], className='row'),

        html.Div([
        dcc.Dropdown(id='piedropdown',
            options=[
                     {'label': 'AP03AT9002PH', 'value': 'AP03AT9002PH'},
                     {'label': 'AP03AT9002TURB', 'value': 'AP03AT9002TURB'}
            ],
            value='AP03AT9002TURB',
            multi=False,
            clearable=False
        ),
        ],className='six columns'),

    ],className='row'),

    html.Div([
        html.Div([
            dcc.Graph(id='linechart'),
        ],className='six columns'),

        html.Div([
            dcc.Graph(id='piechart'),
        ],className='six columns'),

    ],className='row'),


])

@app.callback(
    [Output('piechart', 'figure'),
     Output('linechart', 'figure')],
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value'),
     Input('linedropdown', 'value')]
)
def update_data(chosen_rows,piedropval,linedropval):
    if len(chosen_rows)==0:
        df_filterd = dff[dff['Date'].isin(['2021-03-01','2021-03-02'])]
    else:
        print(chosen_rows)
        df_filterd = dff[dff.index.isin(chosen_rows)]

    pie_chart=px.pie(
            data_frame=df_filterd,
            names='Date',
            values=piedropval,
            hole=.3,
            labels={'Date':'Date'}
            )


    #extract list of chosen countries
    list_chosen_countries=df_filterd['Date'].tolist()
    #filter original df according to chosen countries
    #because original df has all the complete dates
    df_line = df[df['Date'].isin(list_chosen_countries)]

    line_chart = px.line(
            data_frame=df_line,
            x='Time',
            y=linedropval,
            color='Date',
            labels={'Date':'Date', 'Time':'Time21'},
            )
    line_chart.update_layout(uirevision='foo')

    return (pie_chart,line_chart)


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)


