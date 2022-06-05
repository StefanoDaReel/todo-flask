from sqlalchemy.exc import SQLAlchemyError


ERROR_MESSAGE = "DATABASE ERROR"


def add_obj(db, obj):
    try:
        db.session.add(obj)
        db.session.commit()
    except SQLAlchemyError as error:
        error.message = ERROR_MESSAGE
        return error


def update_obj(db, obj, **data):
    obj.update(**data)
    try:
        db.session.commit()
    except SQLAlchemyError as error:
        error.message = ERROR_MESSAGE
        return error


def delete_obj(db, obj):
    try:
        db.session.delete(obj)
        db.session.commit()
    except SQLAlchemyError as error:
        error.message = ERROR_MESSAGE
        return error
