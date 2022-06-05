from flask import request
from flask.views import MethodView

from todo_api import db

from .models import Notes, notes_schema

from .db_utilities import add_obj, update_obj, delete_obj


class NotesList(MethodView):
    def get(self):
        notes = Notes.query.all()
        return notes_schema.jsonify(notes, many=True)

    def post(self):
        body = request.json

        title = body.get('title')
        content = body.get('content')

        if title and content:
            note = Notes(
                title=title,
                content=content,
            )

            error = add_obj(db, note)

            if not error:
                return notes_schema.jsonify(note)

            return {'status': error.message}, 500

        return {'status': 'INVALID DATA'}, 400


class NoteDetail(MethodView):
    def delete(self, id):
        note = Notes.query.get(id)

        error = delete_obj(db, note)

        if not error:
            return {'status': 'OK'}

        return {'status': error.message}, 500

    def put(self, id):
        body = request.json

        note = Notes.query.get(id)

        title = body.get('title', note.title)
        content = body.get('content', note.content)

        if title and content:
            error = update_obj(db, note, title=title, content=content)

            if not error:
                return notes_schema.jsonify(note)

            return {'status': error.message}, 500

        return {'status': 'INVALID DATA'}, 400

    def patch(self, id):
        return self.put(id)
