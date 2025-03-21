from . import db

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)  # Додано поле description

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }
      
