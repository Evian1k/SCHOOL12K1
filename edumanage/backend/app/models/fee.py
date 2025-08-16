from ..extensions import db


class FeeRecord(db.Model):
    __tablename__ = "fee_records"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    term = db.Column(db.String(32), nullable=False)  # e.g., 2025-T1
    amount_due = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    amount_paid = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    status = db.Column(db.String(16), nullable=False, default="unpaid")  # unpaid, partial, paid

    student = db.relationship("Student", back_populates="fee_records")

    __table_args__ = (db.UniqueConstraint("student_id", "term", name="uq_student_term"),)

    def update_status(self) -> None:
        if self.amount_paid >= self.amount_due:
            self.status = "paid"
        elif self.amount_paid > 0:
            self.status = "partial"
        else:
            self.status = "unpaid"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "term": self.term,
            "amount_due": float(self.amount_due),
            "amount_paid": float(self.amount_paid),
            "status": self.status,
        }