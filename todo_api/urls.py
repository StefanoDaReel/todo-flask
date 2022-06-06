from flask import Blueprint

from .views import NotesList, NoteDetail


bp = Blueprint('note', __name__, url_prefix='/todo-api')


bp.add_url_rule('/notes', view_func=NotesList.as_view('list'))
bp.add_url_rule('/notes/<int:id>', view_func=NoteDetail.as_view('detail'))
