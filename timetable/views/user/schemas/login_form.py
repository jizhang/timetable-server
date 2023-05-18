from marshmallow import Schema, fields


class LoginFormSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


login_form_schema = LoginFormSchema()
