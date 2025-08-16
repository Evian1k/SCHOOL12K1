from ..extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    phone_number = db.Column(db.String(32), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.String(32), nullable=False, default="initiated")  # initiated, processing, success, failed
    merchant_request_id = db.Column(db.String(128), nullable=True)
    checkout_request_id = db.Column(db.String(128), nullable=True, index=True)
    mpesa_receipt_number = db.Column(db.String(64), nullable=True)
    result_code = db.Column(db.String(16), nullable=True)
    result_desc = db.Column(db.String(255), nullable=True)
    raw_callback = db.Column(db.JSON, nullable=True)

    student = db.relationship("Student", back_populates="payments")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "phone_number": self.phone_number,
            "amount": float(self.amount),
            "status": self.status,
            "merchant_request_id": self.merchant_request_id,
            "checkout_request_id": self.checkout_request_id,
            "mpesa_receipt_number": self.mpesa_receipt_number,
            "result_code": self.result_code,
            "result_desc": self.result_desc,
        }