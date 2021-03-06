# models.py
# All the "objects" in the database

# you better have a hella good reason to change this again

from functools import partial
from . import db
from .convert import *

# makes everything 10 times easier
# (enables stuff to be factored out)
def keep(cls=None, *, fields=()):
    if isinstance(fields, str):
        fields = fields.split()
    if cls is None:
        return partial(keep, fields=fields)
    cls.fields = fields
    return cls

@keep(fields="qrCode author contact date")
class CustomerList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qrCode = db.Column(db.String(32), nullable=False)
    author = db.Column(db.String(64), nullable=False)
    contact = db.Column(db.String(64), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    items = db.relationship('CustomerItem', backref='list', lazy='dynamic')
    def __repr__(self):
        return f'<CustomerList vars={vars(self)!r}>'

@keep(fields="title rating price count storeId imageUrl")
class CustomerItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    storeId = db.Column(db.Integer, nullable=False)
    imageUrl = db.Column(db.String(256), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey(CustomerList.id))
    def __repr__(self):
        return f'<CustomerItem vars={vars(self)!r}>'

@keep(fields="title rating price storeId imageUrl")
class StoreItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    storeId = db.Column(db.Integer, nullable=False)
    imageUrl = db.Column(db.String(256), nullable=False)
    def __repr__(self):
        return f'<StoreItem vars={vars(self)!r}>'
