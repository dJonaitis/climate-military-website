# flask libraries
from flask import Flask, render_template, request
from markupsafe import Markup
#other libraries
import random
import pandas as pd
# plotting libraries
import plotly.express as px
import plotly.offline as pyo
# custom code
import data 


dataframes = data.getTables(['tradeRegister', 'militaryEmissions'])
transfersDf = dataframes[0]
milEmissionsDf = dataframes[1]
milEmissionsDf['Data accessibility score'] = milEmissionsDf['Data accessibility score'].replace({
    'Very poor - no data reported through the UNFCCC.': 'Very Poor',
    'Poor - disaggregated data not reported through the UNFCCC.': 'Poor',
    'Fair - data reported through the UNFCCC.': 'Fair',
    'Poor - submitted data through the UNFCCC includes civilian sources.': 'Poor',
    'Poor - submitted data through the UNFCCC includes other civilian sources.': 'Poor',
    'Poor - submitted data includes civilian sources.': 'Poor',
    'Poor - data submitted under 1.A.5 includes civilian sources and overall military fuel data reported through the UNFCCC is not clearly disaggregated.': 'Poor',
})
accessibilityDf = milEmissionsDf['Data accessibility score'].value_counts()
accessibilityDf.loc['Good'] = 0
accessibilityDf['No data'] = 198 - accessibilityDf.sum()
accessibilityDf = accessibilityDf.reindex(index=['Very Poor', 'Poor', 'Fair', 'Good', 'No data'])


app = Flask(__name__)



@app.route("/")
# HOMEPAGE function
def index():
    return render_template("landing.html", chart=data.weaponTransfersMap(transfersDf, 1, 2000, 100000))
    
# MAP FUNCTION
@app.route("/weaponsTransfers")
def weaponsTransfers():
    try:
        yearEntered = int(request.args.get("year"))
    except:
        yearEntered = random.randint(1950, 2023) # if a year is not passed, for example when a user goes to the page from outside the navbar or the page itself, a random year is generated
    transferAmount, sipriTIV, sipriTIV_comps = data.getYearData(transfersDf, yearEntered)
    return render_template("weaponsTransfers.html", chart=data.weaponTransfersMap(transfersDf, 1, yearEntered, 100000), year = yearEntered, transferAmount = transferAmount, sipriTIV = round(sipriTIV), humveeTIV = sipriTIV_comps['Humvee'], hellfireTIV=sipriTIV_comps['Hellfire Missile'], AH1ZTIV=sipriTIV_comps['AH-1Z'], reaperTIV=sipriTIV_comps['Reaper drone']);

@app.route("/climate-crisis")
def pageClimateCrisis():
    return render_template("climateCrisis.html")

@app.route("/gap")
def pageGap():
    bar, barNoData = data.dataAccessibilityBar(accessibilityDf)
    return render_template("gap.html", barAcc=bar, barAccNoData=barNoData, mapAcc=data.dataAccessibilityMap(milEmissionsDf))

@app.route("/about")
def pageAbout():
    return render_template("about.html")


