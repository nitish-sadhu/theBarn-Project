from dash import Dash, html, Output, Input, callback, dash_table, dcc
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import dash_mantine_components as dmc
import plotly.express as px


# creating connection to server

conn = psycopg2.connect(
        database = 'barn-database',
        user = 'postgres',
        password = 'Hemanthkumar#1',
        host = 'localhost',
        port = '5432'
)

# creating a cursor object
curs = conn.cursor()

# fetching the data
curs.execute("SELECT * FROM barn_reviews")
reviews = curs.fetchall()
reviews_df = pd.DataFrame(reviews)

# setting the index and the columns of the dataframe
col_names = [desc[0] for desc in curs.description]
reviews_df.columns = col_names
reviews_df.set_index('index', inplace=True)

#print(reviews_df.head())

external_stylesheet = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__)

# app layout
app.layout = dmc.Container([
                dmc.Title("barn reviews dashboard", color='blue', size='h3', align='center'),
                dmc.RadioGroup(
                        [dmc.Radio(i, value=i) for i in ['vader score', 'textblob score', 'stars']],
                        id = 'radio-item',
                        value = 'stars',
                        size = 'sm'
                ),
                dmc.Grid([
                        dmc.Col([
                                dcc.Graph(figure={}, id='graph-placeholder')
                        ], span=6)
                ])]
)

@callback(
        Output(component_id = 'graph-placeholder', component_property = 'figure'),
        Input(component_id = 'radio-item', component_property = 'value')
)

def update_plot(col_chosen):
                if col_chosen == 'stars':
                        fig = px.histogram(reviews_df, x='stars', width=700, height=500)
                elif col_chosen == 'textblob score':
                        fig = px.histogram(reviews_df, x='stars', color="texblob_sentiment", width=700, height=500,
                                           color_discrete_map = {
                                                   "Positive":"#1CCAE3", "Neutral":"Gray", "Negative":"#E3351C"
                                           },
                                           category_orders = {
                                                   'textblob_sentiment' : ['Positive', 'Neutral', 'Negative']
                                           })
                elif col_chosen == 'vader score':
                        fig = px.histogram(reviews_df, x='stars', color="vader_sentiment",
                                           color_discrete_map = {
                                                   "Positive":"Green", "Neutral":"Gray", "Negative":"Red"
                                           },
                                           category_orders = {
                                                   'vader_sentiment' : ['Positive', 'Neutral', 'Negative']
                                           })

                return fig

if __name__ == '__main__':
        app.run(debug=True)

