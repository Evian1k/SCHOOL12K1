import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from .config import get_config
from .extensions import db, migrate, ma, jwt, cors


def create_app(config_name: str | None = None) -> Flask:
    load_dotenv()
    app = Flask(__name__)
    cfg = get_config(config_name or os.getenv("ENV", "development"))
    app.config.from_object(cfg)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get("CORS_ALLOWED_ORIGINS", "*")}})
    jwt.init_app(app)

    # Register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.student_routes import students_bp
    from .routes.teacher_routes import teachers_bp
    from .routes.attendance_routes import attendance_bp
    from .routes.grades_routes import grades_bp
    from .routes.fees_routes import fees_bp
    from .routes.payment_routes import payments_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(students_bp, url_prefix="/api/students")
    app.register_blueprint(teachers_bp, url_prefix="/api/teachers")
    app.register_blueprint(attendance_bp, url_prefix="/api/attendance")
    app.register_blueprint(grades_bp, url_prefix="/api/grades")
    app.register_blueprint(fees_bp, url_prefix="/api/fees")
    app.register_blueprint(payments_bp, url_prefix="/api/payments")

    @app.get("/api/health")
    def healthcheck():
        return jsonify({"status": "ok"})

    return app