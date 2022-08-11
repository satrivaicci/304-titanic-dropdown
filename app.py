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
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    grouped_mean=df.groupby(['continent_name'])[continuous_var].mean()
    results=pd.DataFrame(grouped_mean)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['beer_servings'].index,
        y=results.loc['beer_servings'][continuous_var],
        name='Beer servings',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['spirit_servings'].index,
        y=results.loc['spirit_servings'][continuous_var],
        name='Spirit servings',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        x=results.loc['wine_servings'].index,
        y=results.loc['wine_servings'][continuous_var],
        name='Wine servings',
        marker=dict(color=color3)
    )

    mylayout = go.Layout(
        title='Drinks statistics per continent bar chart',
        xaxis = dict(title = 'Servings category'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
