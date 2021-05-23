
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


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
        f"Welcome to Hawaii climate analysis<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
       f"/api/v1.0/temp/start/end<br />"
        
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    one_year_ago = dt.date(2017,8,23)-dt.timedelta(days=365)
    pcrp_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >=one_year_ago).\
    order_by(Measurement.date).all()

    session.close()
    all_prcp = dict(pcrp_data)
    

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    station_list = session.query(Measurement.station).group_by(Measurement.station).all()

    session.close()
    all_stations = list(np.ravel(station_list))
    

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    one_year_ago = dt.date(2017,8,23)-dt.timedelta(days=365)
    temp_data = session.query(Measurement.tobs).\
    filter(Measurement.date >=one_year_ago).\
    filter(Measurement.station=='USC00519281').all()
    session.close()
    all_tobs = list(np.ravel(temp_data))
    

    return jsonify(all_tobs)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/start/end")
def calc_temps(start, end):
    """TMIN, TAVG, and TMAX for a list of dates.
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """

    if end != "":
        temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
            func.max(Measurement.tobs)).filter(Measurement.date.between(year_from_last, last_data_point)).all()
        t_stats = list(np.ravel(temp_stats))
        return jsonify(temp_stats)

    else:
        temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
            func.max(Measurement.tobs)).filter(Measurement.date > last_data_point).all()
        t_stats = list(np.ravel(temp_stats))
        return jsonify(temp_stats)

    return jsonify(all_tobs)


if __name__ == '__main__':
    app.run(debug=True)

