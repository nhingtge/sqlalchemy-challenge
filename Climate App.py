import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    precipitation = []
    for result in results:
        dictionary = {}
        dictionary[result[0]] = result[1]
        precipitation.append(dictionary)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Station.station, Station.name).all()
    session.close()

    stations = []
    for result in results:
        dictionary = {}
        dictionary['station'] = result[0]
        dictionary['name'] = result[1]
        stations.append(dictionary)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs(gen):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= query_date).all()
    session.close()

    tobs = []
    for result in results:
        dictionary = {}
        dictionary['temperature'] = result[0]
        dictionary['date'] = result[1]
        tobs.append(dictionary)

    return jsonify(tobs)

@app.route("/api/v1.0/start")
def temp_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start = dt.datetime.strptime(start, '%Y-%m-%d')
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    temps = []
    for result in results:
        dictionary = {}
        dictionary['Start'] = start
        dictionary['tmin'] = result[0]
        dictionary['tavg'] = result[1]
        dictionary['tmax'] = result[2]
        temps.append(dictionary)

    return jsonify(temps)

@app.route("/api/v1.0/start/end")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start = dt.datetime.strptime(start, '%Y-%m-%d')
    end = dt.datetime.strptime(end, "%Y-%m-%d")
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end)

    temps = []
    for result in results:
        dictionary = {}
        dictionary['Start'] = start
        dictionary['End'] = end
        dictionary['tmin'] = result[0]
        dictionary['tavg'] = result[1]
        dictionary['tmax'] = result[2]
        temps.append(dictionary)

if __name__ == '__main__':
    app.run(debug=True)