from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import Student, User
from ..schemas import StudentSchema, UserSchema
from ..utils.roles import roles_required


students_bp = Blueprint("students", __name__)
student_schema = StudentSchema()
user_schema = UserSchema()


@students_bp.post("")
@jwt_required()
@roles_required("admin")
def create_student():
    data = student_schema.load(request.json)
    student = Student(**data)
    db.session.add(student)
    db.session.commit()
    return jsonify({"student": student.to_dict()}), 201


@students_bp.get("")
@jwt_required()
@roles_required("admin", "teacher")
def list_students():
    students = Student.query.all()
    return jsonify({"students": [s.to_dict() for s in students]})


@students_bp.get("/<int:student_id>")
@jwt_required()
@roles_required("admin", "teacher", "parent")
def get_student(student_id: int):
    student = Student.query.get_or_404(student_id)
    return jsonify({"student": student.to_dict()})


@students_bp.put("/<int:student_id>")
@jwt_required()
@roles_required("admin")
def update_student(student_id: int):
    student = Student.query.get_or_404(student_id)
    data = request.json or {}
    for key in ["admission_number", "classroom_id", "guardian_id"]:
        if key in data:
            setattr(student, key, data[key])
    db.session.commit()
    return jsonify({"student": student.to_dict()})


@students_bp.delete("/<int:student_id>")
@jwt_required()
@roles_required("admin")
def delete_student(student_id: int):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "deleted"})