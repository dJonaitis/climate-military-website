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

transfersDf = data.getTables(['tradeRegister'])[0]

app = Flask(__name__)



@app.route("/")
# HOMEPAGE function
def index():
    return render_template("landing.html", chart=data.weaponTransfersMap(transfersDf, 1, 2000, 100000))
    
# MAP FUNCTION
@app.route("/weaponsTransfers")
def weaponsTransfers():
    yearEntered = int(request.args.get("year"))
    transferAmount, sipriTIV, sipriTIV_comps = data.getYearData(transfersDf, yearEntered)
    return render_template("weaponsTransfers.html", chart=data.weaponTransfersMap(transfersDf, 1, yearEntered, 100000), year = yearEntered, transferAmount = transferAmount, sipriTIV = round(sipriTIV), humveeTIV = sipriTIV_comps['Humvee'], hellfireTIV=sipriTIV_comps['Hellfire Missile'], AH1ZTIV=sipriTIV_comps['AH-1Z'], reaperTIV=sipriTIV_comps['Reaper drone']);

@app.route("/impacts")
def pageImpacts():
    return render_template("impacts.html")

@app.route("/resources")
def pageResources():
    return render_template("resources.html")

@app.route("/news")
def pageNews():
    return render_template("news.html")


