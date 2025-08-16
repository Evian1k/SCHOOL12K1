from ..extensions import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    admission_number = db.Column(db.String(64), unique=True, index=True, nullable=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey("classrooms.id"), nullable=True)
    guardian_id = db.Column(db.Integer, db.ForeignKey("guardians.id"), nullable=True)

    user = db.relationship("User", back_populates="student")
    classroom = db.relationship("Classroom", back_populates="students")
    guardian = db.relationship("Guardian", back_populates="students")

    enrollments = db.relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    attendance_records = db.relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    fee_records = db.relationship("FeeRecord", back_populates="student", cascade="all, delete-orphan")
    payments = db.relationship("Payment", back_populates="student", cascade="all, delete-orphan")
    grades = db.relationship("Grade", back_populates="student", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user": self.user.to_safe_dict() if self.user else None,
            "admission_number": self.admission_number,
            "classroom": self.classroom.to_dict() if self.classroom else None,
            "guardian": self.guardian.to_dict() if self.guardian else None,
        }