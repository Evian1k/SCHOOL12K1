from marshmallow import Schema, fields


class GradeSchema(Schema):
    id = fields.Int(dump_only=True)
    student_id = fields.Int(required=True)
    subject_id = fields.Int(required=True)
    term = fields.Str(required=True)
    marks = fields.Float(required=True)
    grade = fields.Str(dump_only=True)
    remarks = fields.Str(required=False, allow_none=True)