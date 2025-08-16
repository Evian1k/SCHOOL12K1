from ..extensions import db


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    staff_number = db.Column(db.String(64), unique=True, nullable=True)

    user = db.relationship("User", back_populates="teacher")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user": self.user.to_safe_dict() if self.user else None,
            "staff_number": self.staff_number,
        }