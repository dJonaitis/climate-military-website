from flask import Flask, render_template, request
from markupsafe import Markup


import pandas as pd
# plotting libraries
import plotly.express as px
import plotly.offline as pyo


# custom code
import data 
# functionality:
# - getTables(tableNames) returns a list of pandas dataframes from SQL database, takes a list of table names as input

app = Flask(__name__)

@app.route("/")
# HOMEPAGE function
def index():
    df = data.getTables(['tradeRegister'])[0]
    return render_template("page1.html", chart=data.weaponTransfersMap(df, 1, 2000, 100000))
    

    

# FLASK ROUTING
@app.route("/process-exit")
def page2():
    return render_template("page2.html")

@app.route("/impacts")
def pageImpacts():
    return render_template("impacts.html")

@app.route("/resources")
def pageResources():
    return render_template("resources.html")

@app.route("/news")
def pageNews():
    return render_template("news.html")


