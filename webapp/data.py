# This file reads data from the SQL database, and converts it into pandas dataframes for visualisation
import pandas as pd
import sqlite3
import os
import geopandas as gpd
from markupsafe import Markup

# Plotting libraries
import plotly.graph_objects as go
import plotly.express as px
import plotly.offline as pyo
import plotly.io as pio



PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

DATABASE = os.path.join(PROJECT_ROOT, 'static', 'countryDatabase.db')


def getTables(tableNames):
    conn = sqlite3.connect(DATABASE)
    dataframes = []
    for tableName in tableNames:
        query = f"SELECT * FROM {tableName}"
        df = pd.read_sql_query(query, conn)
        dataframes.append(df)
    return dataframes


# Mapping function for landing page map

def weaponTransfersMap(df, width, year, max):
    fig = go.Figure()
    
    # filtering
    df = df[df['Year'] == year]
    df.sort_values(by='Value (millions)', ascending=False, inplace=False)
    df = df.head(max)

    df_zip = zip(df['ISO_Supplier'], df['ISO_Recipient'], df['Value (millions)'])

    for iso_supplier, iso_recipient, value in df_zip:
        fig.add_trace(go.Scattergeo(
                            locations=[iso_supplier, iso_recipient],
                            locationmode='ISO-3',
                            mode='lines',
                            line=dict(width=width, color="red")
                            ))

    fig.update_layout(margin={"t": 0, "b": 0, "l": 0, "r": 0, "pad": 0},
                    showlegend=False,
                    template="plotly_dark")  # Set the template to plotly_dark
    
    chart = pyo.offline.plot(fig, include_plotlyjs=False, output_type='div', config={"displayModeBar": False})
    chart_markup = Markup(chart)
    return chart_markup