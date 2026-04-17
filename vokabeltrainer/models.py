from . import db


class Vokabel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    franzoesisch = db.Column(db.String(100))
    deutsch = db.Column(db.String(100))
