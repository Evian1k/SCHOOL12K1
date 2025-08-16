from datetime import datetime
from ..extensions import db


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    check_in = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(16), nullable=False, default="present")  # present, absent, late
    notification_sent = db.Column(db.Boolean, default=False)

    student = db.relationship("Student", back_populates="attendance_records")

    __table_args__ = (db.UniqueConstraint("student_id", "date", name="uq_student_date"),)

    def mark_check_in(self) -> None:
        self.check_in = datetime.utcnow()
        self.status = "present"

    def mark_check_out(self) -> None:
        self.check_out = datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "date": self.date.isoformat(),
            "check_in": self.check_in.isoformat() if self.check_in else None,
            "check_out": self.check_out.isoformat() if self.check_out else None,
            "status": self.status,
            "notification_sent": self.notification_sent,
        }