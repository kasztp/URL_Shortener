from app import db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class URLStore(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048))
    shortened = db.Column(db.String(512))


class Logs(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.TIMESTAMP(), default=db.func.current_timestamp())
    ip_address = db.Column(db.String(45))
    endpoint = db.Column(db.String(200))
