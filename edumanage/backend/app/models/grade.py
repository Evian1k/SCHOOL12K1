from ..extensions import db


class Grade(db.Model):
    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    term = db.Column(db.String(32), nullable=False)
    marks = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(2), nullable=True)
    remarks = db.Column(db.String(255), nullable=True)

    student = db.relationship("Student", back_populates="grades")
    subject = db.relationship("Subject", back_populates="grades")

    __table_args__ = (db.UniqueConstraint("student_id", "subject_id", "term", name="uq_student_subject_term"),)

    def compute_grade(self) -> None:
        if self.marks >= 80:
            self.grade = "A"
        elif self.marks >= 70:
            self.grade = "B"
        elif self.marks >= 60:
            self.grade = "C"
        elif self.marks >= 50:
            self.grade = "D"
        else:
            self.grade = "E"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "subject_id": self.subject_id,
            "term": self.term,
            "marks": self.marks,
            "grade": self.grade,
            "remarks": self.remarks,
        }