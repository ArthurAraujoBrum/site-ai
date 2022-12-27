from website import db
from sqlalchemy.sql import func

class Ideas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(5000), unique=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    generated = db.Column(db.Boolean, default=False)
    generated_by = db.Column(db.Integer)
    like_counter = db.Column(db.Integer)
