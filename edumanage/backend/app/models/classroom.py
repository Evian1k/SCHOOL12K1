from ..extensions import db


class Classroom(db.Model):
    __tablename__ = "classrooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    grade_level = db.Column(db.String(32), nullable=True)

    students = db.relationship("Student", back_populates="classroom", lazy="dynamic")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "grade_level": self.grade_level,
        }