from ..extensions import db


class Guardian(db.Model):
    __tablename__ = "guardians"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    relationship = db.Column(db.String(64), nullable=True)  # e.g., father, mother, aunt

    user = db.relationship("User", back_populates="guardian")
    students = db.relationship("Student", back_populates="guardian")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user": self.user.to_safe_dict() if self.user else None,
            "relationship": self.relationship,
        }