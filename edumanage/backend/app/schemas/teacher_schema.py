from marshmallow import Schema, fields


class TeacherSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    staff_number = fields.Str(required=False)