from datetime import date
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import Attendance, Student
from ..schemas import AttendanceSchema
from ..utils.roles import roles_required
from ..services.notification_service import NotificationService


attendance_bp = Blueprint("attendance", __name__)
attendance_schema = AttendanceSchema()


@attendance_bp.post("/check-in")
@jwt_required()
@roles_required("admin", "teacher")
def check_in():
    payload = attendance_schema.load(request.json)
    today = payload.get("date") or date.today()
    student_id = payload["student_id"]
    record = Attendance.query.filter_by(student_id=student_id, date=today).first()
    if not record:
        record = Attendance(student_id=student_id, date=today, status="present")
        db.session.add(record)
    record.mark_check_in()
    db.session.commit()

    # notify guardian
    student = Student.query.get(student_id)
    if student and student.guardian and student.guardian.user and student.guardian.user.phone:
        NotificationService().send_sms(
            student.guardian.user.phone,
            f"{student.user.full_name()} checked in on {today}",
        )
    return jsonify({"attendance": record.to_dict()})


@attendance_bp.post("/check-out")
@jwt_required()
@roles_required("admin", "teacher")
def check_out():
    payload = attendance_schema.load(request.json)
    today = payload.get("date") or date.today()
    student_id = payload["student_id"]
    record = Attendance.query.filter_by(student_id=student_id, date=today).first()
    if not record:
        return jsonify({"message": "No check-in record"}), 400
    record.mark_check_out()
    db.session.commit()

    # notify guardian
    student = Student.query.get(student_id)
    if student and student.guardian and student.guardian.user and student.guardian.user.phone:
        NotificationService().send_sms(
            student.guardian.user.phone,
            f"{student.user.full_name()} checked out on {today}",
        )
    return jsonify({"attendance": record.to_dict()})


@attendance_bp.get("/student/<int:student_id>")
@jwt_required()
@roles_required("admin", "teacher", "parent")
def get_attendance(student_id: int):
    records = Attendance.query.filter_by(student_id=student_id).order_by(Attendance.date.desc()).all()
    return jsonify({"records": [r.to_dict() for r in records]})