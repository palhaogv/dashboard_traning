import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

"""Starting the app"""
app = dash.Dash(__name__)


"""Importing and cleaning the data"""
df = pd.read_csv('intro_bees.csv')
df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)

"""App layout"""
app.layout = html.Div([
    #Header
    html.H1('Web Application Dashboards with Dash', style={'text-align': 'center'}),

    dcc.Dropdown(id='slct_year',
                options=[
                    {'label': '2015', 'value': 2015}, #values come from the dataframe
                    {'label': '2016', 'value': 2016},
                    {'label': '2017', 'value': 2017},
                    {'label': '2018', 'value': 2018,}],
                multi=False,
                value=2015,
                style={'width': '40%'}
                ),

    html.Div(id='output_container', children=[]),
    #Space
    html.Br(),
    #Graph
    dcc.Graph(id='my_bee_map', figure={})

])

"""The call back: connecting the app components with the Plotly graphics"""
#A callback has an output and an input. 
@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)

def update_graph(option_slctd):  
    """function definition for callback (callback function),
    which argument is connect to one input and always refer to the input
    component_property"""

    #Container
    container = f'The year chosen by user was: {option_slctd}'

    dff = df.copy()
    dff = dff[dff['Year'] == option_slctd]
    dff = dff[dff['Affected by'] == 'Varroa_mites']

#Plotly Express
#    fig = px.choropleth(
#        data_frame=dff,
#        locationmode='USA-states',
#        locations='state_code',
#        scope='usa',
#        color='Pct of Colonies Impacted',
#        hover_data=['State', 'Pct of Colonies Impacted'],
#        color_continuous_scale=px.colors.sequential.YlOrRd,
#        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
#        template='plotly_dark'
#    )

    #Plotly Graph Objects (GO)
    fig = go.Figure(
        data=[go.Choropleth(
            locationmode='USA-states',
            locations=dff['state_code'],
            z=dff['Pct of Colonies Impacted'].astype(float),
            colorscale='Reds',
        )]
    )

    fig.update_layout(
        title_text='Bees Affected my Mites in the USA',
        title_xanchor='center',
        title_x=0.5,
        title_font=dict(size=24),
        geo=dict(scope='usa'),
    )
    

    """the return means what are going to be returned on the outputs, 
    so as it has 2 outputs it is needed 2 return (one of each)"""
    return container, fig

"""Run server"""
if __name__ == '__main__':
    app.run_server(debug=True)



