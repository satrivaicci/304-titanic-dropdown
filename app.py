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
githublink = 'https://github.com/plotly-dash-apps/304-titanic-dropdown'


###### Import a dataframe #######
df = pd.read_csv("https://raw.git.generalassemb.ly/intuit-ds-15/05-cleaning-combining-data/master/data/drinks.csv?token=AAAK2H43E5OWLGL6F7TI2OLC7RDXQ", keep_default_na=False)
# df = pd.read_csv("https://raw.githubusercontent.com/austinlasseter/plotly_dash_tutorial/master/00%20resources/titanic.csv")
# df['Female']=df['Sex'].map({'male':0, 'female':1})
# df['Cabin Class'] = df['Pclass'].map({1:'first', 2: 'second', 3:'third'})
# variables_list=['Survived', 'Female', 'Fare', 'Age']
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
              [Input('dropdown', 'value')])
def display_value(continent):
    grouped_mean=df.groupby(['continent_name']).mean()
    results=pd.DataFrame(grouped_mean)
    # Create a stats by continent bar chart
    mydata1 = go.Bar(
        x=results.loc[continent].index,
        y=results.loc[continent],
        marker=dict(color=color1)
    )
    mylayout = go.Layout(
        title='Drinks statistics per continent bar chart',
        xaxis = dict(title = 'Servings category'), # x-axis label
        yaxis = dict(title = str(continent)), # y-axis label

    )
    fig = go.Figure(data=[mydata1], layout=mylayout)
    
    
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
    
    
    return fig, pie1


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
