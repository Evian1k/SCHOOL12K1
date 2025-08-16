from marshmallow import Schema, fields


class StudentSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    admission_number = fields.Str(required=False)
    classroom_id = fields.Int(required=False, allow_none=True)
    guardian_id = fields.Int(required=False, allow_none=True)