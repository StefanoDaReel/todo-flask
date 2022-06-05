#! /bin/bash


fuser 5000/tcp --kill


source venv/todo/bin/activate


export FLASK_APP=todo_api
export FLASK_ENV=development


python set_db.py


flask run
