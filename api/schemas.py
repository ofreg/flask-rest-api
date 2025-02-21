from marshmallow import Schema, fields, validate, ValidationError

class BookSchema(Schema):
    id = fields.Int(dump_only=True)  
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))  
    author = fields.Str(required=True, validate=validate.Length(min=1, max=255))  
    year = fields.Int(required=True, validate=validate.Range(min=1, max=2025)) 

book_schema = BookSchema()
book_list_schema = BookSchema(many=True)
