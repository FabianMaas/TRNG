"""
This file defines the Randbyte model and initializes the SQLAlchemy database.

Attributes:
- db (SQLAlchemy): The SQLAlchemy object used for database operations.

Classes:
- Randbyte: Represents a model for storing random byte values.
"""


from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Randbyte(db.Model):
    """
    Represents a model for storing random byte values.\n
    Attributes:
    - id (int): The primary key of the Randbyte model.
    - value (str): The random byte value, limited to 8 characters.
    """
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(8), nullable=False)