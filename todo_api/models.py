from todo_api import db, ma


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300), nullable=False)

    def __str__(self):
        return self.title

    def update(self, **data):
        title = data.get('title', self.title)
        content = data.get('content', self.content)

        self.title = title if title != "" else self.title
        self.content = content if content != "" else self.content


class NotesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notes


notes_schema = NotesSchema()
