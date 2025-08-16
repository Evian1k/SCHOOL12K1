from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import Grade
from ..schemas import GradeSchema
from ..utils.roles import roles_required


grades_bp = Blueprint("grades", __name__)
grade_schema = GradeSchema()


@grades_bp.post("")
@jwt_required()
@roles_required("admin", "teacher")
def upsert_grade():
    payload = grade_schema.load(request.json)
    grade = Grade.query.filter_by(
        student_id=payload["student_id"],
        subject_id=payload["subject_id"],
        term=payload["term"],
    ).first()
    if not grade:
        grade = Grade(**payload)
        grade.compute_grade()
        db.session.add(grade)
    else:
        grade.marks = payload["marks"]
        grade.remarks = payload.get("remarks")
        grade.compute_grade()
    db.session.commit()
    return jsonify({"grade": grade_schema.dump(grade)})


@grades_bp.get("/student/<int:student_id>")
@jwt_required()
@roles_required("admin", "teacher", "parent")
def list_student_grades(student_id: int):
    results = Grade.query.filter_by(student_id=student_id).all()
    return jsonify({"grades": [grade_schema.dump(g) for g in results]})