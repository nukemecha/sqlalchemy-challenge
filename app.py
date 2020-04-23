from flask import Flask
from flask import jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np

# setup db & reflect it 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

# our tables
m = Base.classes.measurement
s = Base.classes.station

session = Session(engine)

# setup flask
app = Flask(__name__)

# define flask routes
@app.route("/", methods=['GET'])
def hello():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end<br/>"        
    )

# get precipitation in json
@app.route("/api/v1.0/precipitation", methods=['GET'])
def precip():

    precip = session.query(m.date, m.prcp).filter(m.date > '2016-08-22').all()

    #print(precip)
    precip_dict = {}

    for d, p in precip:
        precip_dict[d] = p

    return jsonify(precip_dict)

@app.route("/api/v1.0/stations", methods=['GET'])
def stations():

    stations = session.query(s.station).all()

    stations_list = list(np.ravel(stations))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs", methods=['GET'])
def tobs():

    temps = session.query(m.date, m.tobs).filter(m.date > '2016-08-22').all()

    temp_dict = {}

    for d, t in temps:
        temp_dict[d] = t
    
    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>", methods=['GET'])
@app.route("/api/v1.0/<start>/<end>", methods=['GET'])
def ranged_temps(start = None, end = None):

    if not end:

        temps = session.query(\
            func.min(m.tobs),\
            func.avg(m.tobs),\
            func.max(m.tobs)).\
            filter(m.date >= start).all()
        
        temps_list = list(np.ravel(temps))

        return jsonify(temps_list)

    temps = session.query(\
        func.min(m.tobs),\
        func.avg(m.tobs),\
        func.max(m.tobs)).\
        filter(m.date >= start).filter(m.date <= end).all()
    
    temps_list = list(np.ravel(temps))

    return jsonify(temps_list)

if __name__ == '__main__':
    app.run(debug=True)
