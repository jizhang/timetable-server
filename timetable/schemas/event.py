from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.Integer()
    title = fields.String()
    color = fields.String()


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
