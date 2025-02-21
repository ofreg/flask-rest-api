class BookSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    year = fields.Int(required=True)

book_schema = BookSchema()
book_list_schema = BookSchema(many=True)