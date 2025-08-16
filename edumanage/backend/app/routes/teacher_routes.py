from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import Teacher
from ..schemas import TeacherSchema
from ..utils.roles import roles_required


teachers_bp = Blueprint("teachers", __name__)
teacher_schema = TeacherSchema()


@teachers_bp.post("")
@jwt_required()
@roles_required("admin")
def create_teacher():
    data = teacher_schema.load(request.json)
    teacher = Teacher(**data)
    db.session.add(teacher)
    db.session.commit()
    return jsonify({"teacher": teacher.to_dict()}), 201


@teachers_bp.get("")
@jwt_required()
@roles_required("admin")
def list_teachers():
    teachers = Teacher.query.all()
    return jsonify({"teachers": [t.to_dict() for t in teachers]})


@teachers_bp.put("/<int:teacher_id>")
@jwt_required()
@roles_required("admin")
def update_teacher(teacher_id: int):
    teacher = Teacher.query.get_or_404(teacher_id)
    data = request.json or {}
    if "staff_number" in data:
        teacher.staff_number = data["staff_number"]
    db.session.commit()
    return jsonify({"teacher": teacher.to_dict()})


@teachers_bp.delete("/<int:teacher_id>")
@jwt_required()
@roles_required("admin")
def delete_teacher(teacher_id: int):
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    return jsonify({"message": "deleted"})