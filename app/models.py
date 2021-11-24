from app import db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class URLStore(db.Model):
    """ORM for urls DB table."""
    __tablename__ = 'urls'
    original_url = db.Column(db.String(2048), index=True)
    shortened = db.Column(db.String(16), primary_key=True, index=True)


class Logs(db.Model):
    """ORM for logs DB table"""
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.TIMESTAMP(), default=db.func.current_timestamp())
    ip_address = db.Column(db.String(45))
    endpoint = db.Column(db.String(200))
