from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import FeeRecord
from ..schemas import FeeRecordSchema
from ..utils.roles import roles_required


fees_bp = Blueprint("fees", __name__)
fee_schema = FeeRecordSchema()


@fees_bp.post("")
@jwt_required()
@roles_required("admin")
def create_or_update_fee():
    payload = fee_schema.load(request.json)
    record = FeeRecord.query.filter_by(student_id=payload["student_id"], term=payload["term"]).first()
    if not record:
        record = FeeRecord(**payload)
        record.update_status()
        db.session.add(record)
    else:
        record.amount_due = payload.get("amount_due", record.amount_due)
        record.amount_paid = payload.get("amount_paid", record.amount_paid)
        record.update_status()
    db.session.commit()
    return jsonify({"fee_record": record.to_dict()})


@fees_bp.get("/student/<int:student_id>")
@jwt_required()
@roles_required("admin", "teacher", "parent")
def get_student_fees(student_id: int):
    records = FeeRecord.query.filter_by(student_id=student_id).all()
    return jsonify({"fee_records": [r.to_dict() for r in records]})