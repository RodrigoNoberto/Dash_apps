from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),

                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                             ],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                             ),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),

                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       2500: '2500',
                                                       5000: '5000',
                                                       7500: '7500'},
                                                value=[min_payload, max_payload]),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(site_dropdown):
    filtered_py = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
    if site_dropdown == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')
        return fig

    else:
        fig = px.pie(filtered_py, names='class', title=f'Total Success Launches for Site {site_dropdown}')
        return fig


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(site_dropdown, payload_slider):
    df1 = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_slider[0]) & (spacex_df['Payload Mass (kg)'] <= payload_slider[1])]
    df2 = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
    filtered_py = df2[(df2['Payload Mass (kg)'] >= payload_slider[0]) & (df2['Payload Mass (kg)'] <= payload_slider[1])]

    if site_dropdown == 'ALL':
        scatter = px.scatter(df1, x='Payload Mass (kg)', y='class',
                             title='Correlation between Payload and Success for all Sites',
                             color='Booster Version Category')
        return scatter

    else:
        scatter = px.scatter(filtered_py, x='Payload Mass (kg)', y='class',
                             title=f'Correlation between Payload and Success for Site {site_dropdown}',
                             color='Booster Version Category')
        return scatter

if __name__ == '__main__':
    app.run_server(debug=True)