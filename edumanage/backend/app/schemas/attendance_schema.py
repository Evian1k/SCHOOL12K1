from marshmallow import Schema, fields


class AttendanceSchema(Schema):
    id = fields.Int(dump_only=True)
    student_id = fields.Int(required=True)
    date = fields.Date(required=True)
    check_in = fields.DateTime(required=False, allow_none=True)
    check_out = fields.DateTime(required=False, allow_none=True)
    status = fields.Str(required=False)
    notification_sent = fields.Bool(dump_only=True)