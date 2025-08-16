from ..extensions import db


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    code = db.Column(db.String(32), nullable=True, unique=True)

    enrollments = db.relationship("Enrollment", back_populates="subject", cascade="all, delete-orphan")
    grades = db.relationship("Grade", back_populates="subject", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
        }