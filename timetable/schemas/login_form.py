from marshmallow import Schema, fields, validate

not_blank = validate.Length(min=1)


class LoginFormSchema(Schema):
    username = fields.Str(required=True, validate=[not_blank])
    password = fields.Str(required=True, validate=[not_blank])


login_form_schema = LoginFormSchema()
