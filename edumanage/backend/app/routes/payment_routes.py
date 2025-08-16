from decimal import Decimal
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import Payment, FeeRecord, Student
from ..schemas import PaymentSchema
from ..utils.roles import roles_required
from ..services.daraja_service import DarajaService


payments_bp = Blueprint("payments", __name__)
payment_schema = PaymentSchema()


@payments_bp.post("/stk-push")
@jwt_required()
@roles_required("admin", "parent")
def initiate_stk_push():
    payload = payment_schema.load(request.json)
    student = Student.query.get_or_404(payload["student_id"]) 

    # create payment record
    payment = Payment(
        student_id=payload["student_id"],
        phone_number=payload["phone_number"],
        amount=Decimal(str(payload["amount"]))
    )
    db.session.add(payment)
    db.session.commit()

    service = DarajaService()
    resp = service.initiate_stk_push(
        amount=float(payment.amount),
        phone_number=payment.phone_number,
        account_reference=student.admission_number or str(student.id),
        description=f"Fees for {student.user.full_name()}",
    )

    payment.merchant_request_id = resp.get("MerchantRequestID")
    payment.checkout_request_id = resp.get("CheckoutRequestID")
    payment.status = "processing"
    db.session.commit()

    return jsonify({"payment": payment.to_dict(), "daraja": resp})


@payments_bp.post("/callback")
def daraja_callback():
    data = request.json or {}
    merchant_request_id, checkout_request_id, mpesa_receipt, result_desc, result_code, final_status = DarajaService.parse_callback(data)

    payment = None
    if checkout_request_id:
        payment = Payment.query.filter_by(checkout_request_id=checkout_request_id).first()
    if not payment and merchant_request_id:
        payment = Payment.query.filter_by(merchant_request_id=merchant_request_id).first()

    if not payment:
        return jsonify({"message": "Payment not found"}), 404

    payment.result_code = str(result_code) if result_code is not None else None
    payment.result_desc = result_desc
    payment.mpesa_receipt_number = mpesa_receipt
    payment.status = "success" if final_status == "success" else "failed"
    payment.raw_callback = data
    db.session.commit()

    if payment.status == "success":
        # update student's latest fee record (the one with non-paid status)
        record = FeeRecord.query.filter_by(student_id=payment.student_id).order_by(FeeRecord.id.desc()).first()
        if record:
            record.amount_paid = Decimal(str(record.amount_paid)) + Decimal(str(payment.amount))
            record.update_status()
            db.session.commit()

    return jsonify({"message": "ok"})