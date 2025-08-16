from marshmallow import Schema, fields


class PaymentSchema(Schema):
    id = fields.Int(dump_only=True)
    student_id = fields.Int(required=True)
    phone_number = fields.Str(required=True)
    amount = fields.Float(required=True)
    status = fields.Str(dump_only=True)
    merchant_request_id = fields.Str(dump_only=True)
    checkout_request_id = fields.Str(dump_only=True)
    mpesa_receipt_number = fields.Str(dump_only=True)
    result_code = fields.Str(dump_only=True)
    result_desc = fields.Str(dump_only=True)