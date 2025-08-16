from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone = fields.Str(required=False, allow_none=True)
    role = fields.Str(required=True, validate=validate.OneOf(["admin", "teacher", "parent", "student"]))


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone = fields.Str(required=False)
    role = fields.Str(required=True, validate=validate.OneOf(["admin", "teacher", "parent", "student"]))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)