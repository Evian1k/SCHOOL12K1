from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..extensions import db
from ..models import User, Student, Teacher, Guardian
from ..schemas import RegisterSchema, LoginSchema, UserSchema


auth_bp = Blueprint("auth", __name__)
register_schema = RegisterSchema()
login_schema = LoginSchema()
user_schema = UserSchema()


@auth_bp.post("/register")
def register():
    data = register_schema.load(request.json)
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already registered"}), 400

    user = User(
        email=data["email"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        phone=data.get("phone"),
        role=data["role"],
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.flush()

    if user.role == "student":
        student = Student(user_id=user.id)
        db.session.add(student)
    elif user.role == "teacher":
        teacher = Teacher(user_id=user.id)
        db.session.add(teacher)
    elif user.role == "parent":
        guardian = Guardian(user_id=user.id)
        db.session.add(guardian)

    db.session.commit()
    return jsonify({"user": user_schema.dump(user)}), 201


@auth_bp.post("/login")
def login():
    data = login_schema.load(request.json)
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    return jsonify({"access_token": token, "user": user_schema.dump(user)})


@auth_bp.get("/me")
@jwt_required()
def me():
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        user_id = identity
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Not found"}), 404
    return jsonify({"user": user_schema.dump(user)})