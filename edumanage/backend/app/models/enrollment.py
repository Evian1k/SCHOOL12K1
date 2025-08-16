from ..extensions import db


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=True)

    student = db.relationship("Student", back_populates="enrollments")
    subject = db.relationship("Subject", back_populates="enrollments")
    teacher = db.relationship("Teacher")

    __table_args__ = (db.UniqueConstraint("student_id", "subject_id", name="uq_student_subject"),)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "subject_id": self.subject_id,
            "teacher_id": self.teacher_id,
        }