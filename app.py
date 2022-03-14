#!/usr/bin/env python
# coding: utf-8

# In[1]:


#install Dependents
import numpy as np
import datetime as dt
import sqlalchemy 

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask , jsonify


# In[2]:


#Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[3]:


Base = automap_base()

Base.prepare(engine, reflect=True)

#Create reference for each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


# In[4]:


app = Flask(__name__)


# In[5]:


@app.route("/")
def homepage():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start>/<end>"
        f"<br>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    query = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()
    
    Precipitation = []
    for date, prcp in query:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)
          
    return jsonify(Precipitation)

    
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    query = session.query(Station.station).all()

    session.close()
    
    Station = []
    for station_nm in query:
        station_list.append(list(station_nm))
    
    return jsonify(Station)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    query_date = dt.date(2017,8,23) - dt.timedelta(days = 365)

    query = session.query(Measurement.tobs).    filter(Measurement.date >= query_date).    filter(Measurement.station == 'USC00519281').all()

    session.close()

    Tobs = list(np.ravel(results))
    
    return jsonify(Tobs)


@app.route("/api/v1.0/<start>/<end>")
def boundaries(start, end):
    Start_d = dt.datetime.strptime(f"{start}", "%Y-%m-%d")
    End_d = dt.datetime.strptime(f"{end}", "%Y-%m-%d")
    
    Stat_avg = func.avg(Measurement.tobs)
    Stat_min = func.min(Measurement.tobs)
    Stat_max = func.max(Measurement.tobs)

    query = session.query(Stat_avg, Stat_min, Stat_max).filter(Measurement.date >= Start_d).    filter(Measurement.date <= endDate).all()

    session.close()

    Bound = list(np.ravel(query))

    return jsonify(Bound)


if __name__ == "__main__":
    app.run(debug = True)


# In[ ]:




