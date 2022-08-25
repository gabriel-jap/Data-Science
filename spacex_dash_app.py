#pip3 install pandas dash
#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"
# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

dict_site={"All sites":"ALL"}
sites=spacex_df["Launch Site"].unique()
for x,y in enumerate(sites):
    dict_site[y]=y

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=dict_site,
                                value='All sites',
                                placeholder="Select Launch Site",
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == "All sites":
        filtered_df = filtered_df[["Launch Site","class"]]
        filtered_df=filtered_df.groupby("Launch Site",as_index=False).sum()
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Succes Lunches by Site')
        return fig
    else:
        filtered_df=filtered_df[spacex_df["Launch Site"] ==entered_site]
        fig = px.pie(filtered_df["class"].value_counts().reset_index(), values='class', 
        names='index', 
        title='Total Success Lunches in {}'.format(entered_site))
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site,payloadSlider):
    filtered_df = spacex_df
    if entered_site == "All sites":
        filtered_df=filtered_df[filtered_df["Payload Mass (kg)"].between(payloadSlider[0],payloadSlider[1])]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",
        color="Booster Version Category",
        title="Success in landings by it Payload")
        return fig
    else:
        filtered_df=filtered_df[spacex_df["Launch Site"] ==entered_site]
        filtered_df=filtered_df[filtered_df["Payload Mass (kg)"].between(payloadSlider[0],payloadSlider[1])]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",
        color="Booster Version Category",
        title="Success in landings by it Payload")
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
