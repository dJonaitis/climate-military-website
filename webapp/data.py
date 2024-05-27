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
    df.sort_values(by='sipri_TIV', ascending=False, inplace=False)
    df = df.head(max)

    df_zip = zip(df['ISO_Supplier'], df['ISO_Recipient'], df['sipri_TIV'])

    for iso_supplier, iso_recipient, value in df_zip:
        hover_text = f"Recipient: {df[df['ISO_Recipient'] == iso_recipient]['Recipient'].values[0]}<br>" \
                 f"Supplier: {df[df['ISO_Supplier'] == iso_supplier]['Supplier'].values[0]}<br>" \
                 f"SIPRI TIV: {value}"
        fig.add_trace(go.Scattergeo(
                            locations=[iso_supplier, iso_recipient],
                            locationmode='ISO-3',
                            mode='lines',
                            line=dict(width=width, color="red"),
                            hovertext=hover_text
                            ))

    fig.update_layout(margin={"t": 0, "b": 0, "l": 0, "r": 0, "pad": 0},
                    showlegend=False,
                    template="plotly_dark",# Set the template to plotly_dark
                    autosize=False)  
                    
    # fig.update_geos(projection_type="orthographic")
    chart = pyo.offline.plot(fig, include_plotlyjs=False, output_type='div', config={"displayModeBar": False})
    chart_markup = Markup(chart)
    return chart_markup

def getYearData(df, year):
    year = int(year)
    df = df[df['Year'] == year]
    sipriTIV_sum = sum(df['sipri_TIV'])
    sipriTIV_comps = {
        'Humvee': round(sipriTIV_sum / 0.04),
        'Hellfire Missile': round(sipriTIV_sum / 0.05),
        'AH-1Z': round(sipriTIV_sum / 14.5),
        'Reaper drone': round(sipriTIV_sum / 7.5)
    }
    return len(df['Recipient']), sipriTIV_sum, sipriTIV_comps