from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    email = fields.Email(required=True)
    name = fields.String(required=True)
    mobile = fields.String(required=True)
    password = fields.String(required=True)

class ExpenseSchema(Schema):
    description = fields.String(required=True)
    amount = fields.Float(required=True)
    split_type = fields.String(validate=lambda s: s in ["Equal", "Exact", "Percentage"])
    payer_id = fields.Integer(required=True)
    participants = fields.List(fields.Dict(keys=fields.Str(), values=fields.Float()))
