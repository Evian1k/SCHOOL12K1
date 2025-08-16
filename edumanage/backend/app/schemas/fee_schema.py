from marshmallow import Schema, fields


class FeeRecordSchema(Schema):
    id = fields.Int(dump_only=True)
    student_id = fields.Int(required=True)
    term = fields.Str(required=True)
    amount_due = fields.Float(required=True)
    amount_paid = fields.Float(required=True)
    status = fields.Str(dump_only=True)