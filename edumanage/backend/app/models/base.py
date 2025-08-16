from datetime import datetime
from ..extensions import db


class PrimaryKeyMixin:
    id = db.Column(db.Integer, primary_key=True)


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)