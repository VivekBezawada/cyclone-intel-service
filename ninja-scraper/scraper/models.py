from scraper import db
from datetime import datetime


class CycloneInfo(db.Model):
    cyclone_id = db.Column(db.String(20), unique=True,
                           primary_key=True, nullable=False)
    cyclone_name = db.Column(db.String(40), nullable=False)
    region = db.Column(db.String(30), nullable=False)
    cyclone_status = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<CycloneInfo %r>' % self.cyclone_id

    def toJSON(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TrackData(db.Model):
    cyclone_id = db.Column(db.String(20), db.ForeignKey(
        'cycloneinfo.cyclone_id'), primary_key=True)
    synoptic_time = db.Column(db.BigInteger, nullable=False,  primary_key=True)
    latitude = db.Column(db.Float, default=0, nullable=False)
    longitude = db.Column(db.Float, default=0, nullable=False)
    intensity = db.Column(db.Integer, default=0, nullable=False)
    #time_stamp = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<TrackData %r>' % self.cyclone_id

    def toJSON(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ForecastData(db.Model):
    cyclone_id = db.Column(db.String(20), db.ForeignKey(
        'cycloneinfo.cyclone_id'), primary_key=True)
    forecast_time = db.Column(db.BigInteger, nullable=False, primary_key=True)
    #predicted_time= db.Column(db.BigInteger, default=0, nullable=False)
    latitude = db.Column(db.Float, default=0, nullable=False)
    longitude = db.Column(db.Float, default=0, nullable=False)
    intensity = db.Column(db.Integer, default=0, nullable=False)
    #time_stamp = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<ForecastData %r>' % self.cyclone_id

    def toJSON(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}
