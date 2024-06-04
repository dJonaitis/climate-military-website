# flask libraries
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from markupsafe import Markup
#other libraries
import random
import pandas as pd
import sqlite3
from datetime import datetime
# plotting libraries
import plotly.express as px
import plotly.offline as pyo
# custom code
import data 

#reading dataframes
dataframes = data.getTables(['tradeRegister', 'militaryEmissions', 'greenhouseGas', 'population'])
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
ccDf = dataframes[2]
popDf = dataframes[3]


#USER TRACKING INIT
conn = sqlite3.connect("user_tracking/userTracking.db", check_same_thread=False)
cur = conn.cursor()

#FLASK APP
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# FLASK ROUTING
# HOMEPAGE function
@app.route("/")
def index():
    return render_template("landing.html", chart=data.weaponTransfersMap(transfersDf, 1, 2000, 100000))
    
# MAP FUNCTION
@app.route("/weaponsTransfers")
def weaponsTransfers(yearEntered):
    try:
        yearEntered = int(request.args.get("year"))
    except:
        yearEntered = random.randint(1950, 2023) # if a year is not passed, for example when a user goes to the page from outside the navbar or the page itself, a random year is generated
    transferAmount, sipriTIV, sipriTIV_comps = data.getYearData(transfersDf, yearEntered)
    return render_template("weaponsTransfers.html", chart=data.weaponTransfersMap(transfersDf, 1, yearEntered, 100000), year = yearEntered, transferAmount = transferAmount, sipriTIV = round(sipriTIV), humveeTIV = sipriTIV_comps['Humvee'], hellfireTIV=sipriTIV_comps['Hellfire Missile'], AH1ZTIV=sipriTIV_comps['AH-1Z'], reaperTIV=sipriTIV_comps['Reaper drone']);

@app.route("/climate-crisis")
def pageClimateCrisis():
    return render_template("climateCrisis.html", totalEmissionsGraph = data.emissionsLineChart(ccDf), capitaEmissionsGraph = data.capitaEmissionsLineChart(ccDf, popDf))

@app.route("/gap")
def pageGap():
    bar, barNoData = data.dataAccessibilityBar(accessibilityDf)
    return render_template("gap.html", barAcc=bar, barAccNoData=barNoData, mapAcc=data.dataAccessibilityMap(milEmissionsDf))

@app.route("/about")
def pageAbout():
    return render_template("about.html")

# USER TRACKING
@app.before_request
def assign_id():
    if "id" not in session:
        session["id"] = random.randint(1_000_000, 9_999_999)

# logs amount of time spent on page
def log_data():
    if not all([key in session for key in ("id", "start_time", "previous_path")]):
        return

    session_id = session.get("id")
    start_time = session.get("start_time")
    previous_path = session.get("previous_path")

    time_spent = (datetime.now() - start_time).total_seconds()
    cur.execute(
        "INSERT INTO PageView (session_id, page, time_spent, start_time) VALUES (?, ?, ?, ?)",
        (session_id, previous_path, time_spent, start_time),
    )
    conn.commit()

@app.after_request
def track_time(response):
    # Every time the user requests default route (/), time spent in the previous path is recorded in the database with log_data().
    if request.path == "/":
        log_data()
        # Update start_time and previous_path
        session["start_time"] = datetime.now()
        session["previous_path"] = "HomePage"

    # Every time the user requests /learn_more route, time spent in the previous path is recorded in the database with log_data().
    if request.path == "/learn_more":
        log_data()
        # Update start_time and previous_path
        session["start_time"] = datetime.now()
        session["previous_path"] = "LearnMore"

    # Every time the user requests  /confirmation route, time spent in the previous path is recorded in the database with log_data().
    if request.path == "/confirmation":
        log_data()
        # We are not interested in the time spent in the "/confirmation" website, so we don't add it to the session
        del session["start_time"]
        del session["previous_path"]

    return response



if __name__ == "__main__":
    app.run(port=3000, debug=True)