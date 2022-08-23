######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Drinks!'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
sourceurl = 'https://www.kaggle.com/c/titanic'
githublink = 'https://github.com/satrivaicci/304-titanic-dropdown'


###### Import a dataframe #######
df = pd.read_csv("assets/drinks.csv", keep_default_na=False) # keep_default_na=False solves the problem of NA continent being read as NaN
df['continent_name'] = df['continent'].map({ 'NA':'North America', 'SA':'South America', 'EU':'Europe', 'AF':'Africa', 'OC': 'Oceania', 'AS': 'Asia' })
variables_list=pd.unique(df['continent_name'])

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose the continent you want to see drinks statistics for:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    dcc.Graph(id='pie1-value'),
    dcc.Graph(id='pie2-value'),
    dcc.Graph(id='pie3-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              Output('pie1-value', 'figure'),
              Output('pie2-value', 'figure'),
              Output('pie3-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continent):
    grouped_mean=df.groupby(['continent_name']).mean()
    results=pd.DataFrame(grouped_mean)
    results=results.drop(columns=['total_litres_of_pure_alcohol'])
    # Create a stats by continent bar chart
    mydata1 = go.Bar(
        x=results.loc[continent].index,
        y=results.loc[continent],
        marker=dict(color=color1)
    )
    mylayout = go.Layout(
        title='Servings per category',
        xaxis = dict(title = 'Drink category'), # x-axis label
        yaxis = dict(title = 'Servings qty. (Mean)'), # y-axis label

    )
    fig = go.Figure(data=[mydata1], layout=mylayout)
    
    
    # Pie 1 - Beer
    pie1Data = go.Pie(
        labels=df.loc[df['continent_name'] == continent]['country'],
        values=df.loc[df['continent_name'] == continent]['beer_servings']
    )

    pie1Layout = go.Layout(
        title='Beer servings per country',
        xaxis = dict(title = 'Country'), # x-axis label
        yaxis = dict(title = 'Beer servings qty. (Mean)'), # y-axis label

    )

    pie1 = go.Figure(data=[pie1Data], layout=pie1Layout)
    pie1.update_traces(textposition='inside', textinfo='percent+label')
    
    
    # Pie 2 - Wine
    pie2Data = go.Pie(
        labels=df.loc[df['continent_name'] == continent]['country'],
        values=df.loc[df['continent_name'] == continent]['wine_servings']
    )

    pie2Layout = go.Layout(
        title='Wine servings per country',
        xaxis = dict(title = 'Country'), # x-axis label
        yaxis = dict(title = 'Wine servings qty. (Mean)'), # y-axis label

    )

    pie2 = go.Figure(data=[pie2Data], layout=pie2Layout)
    pie2.update_traces(textposition='inside', textinfo='percent+label')
    
    
    # Pie 3 - Spirit
    pie3Data = go.Pie(
        labels=df.loc[df['continent_name'] == continent]['country'],
        values=df.loc[df['continent_name'] == continent]['spirit_servings']
    )

    pie3Layout = go.Layout(
        title='Spirit servings per country',
        xaxis = dict(title = 'Country'), # x-axis label
        yaxis = dict(title = 'Spirit servings qty. (Mean)'), # y-axis label

    )

    pie3 = go.Figure(data=[pie3Data], layout=pie3Layout)
    pie3.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig, pie1, pie2, pie3


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
