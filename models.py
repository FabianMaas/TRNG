from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Randbyte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(8), nullable=False)