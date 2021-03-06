# routes.py
# Here lie all the @app.route s

from functools import wraps
from flask import redirect, request

from . import app, db
from .models import *
from .queries import *

def error(message):
    return {"error": {"message": repr(message)}}
def data(data):
    return {"data": data}

# Decorator to automatically change errors into error objects.
# (and to automatically commit)
@wraps(app.route)   # error with @wrap [FIXED]
def rest_route(*args, **kwargs):
    def _outer_route(func):
        @app.route(*args, **kwargs)
        @wraps(func)
        def _inner_route(*args, **kwargs):
            try:
                return data(func(*args, **kwargs))
            except Exception as e:
                return error(e)
            else:
                pass
                # db.session.commit()    # error with db lol ignore this one
        return _inner_route
    return _outer_route


@app.route("/")
def index():
    # should give error lol
    return "lol you aint a computer..."

# GET /<type>?skip=<int>&first=<int>&<arguments>
# note: see query.py/query_search for more info
# POST: /<type>/create
@rest_route("/items", methods=["GET", "POST"])
def items():
    if request.method == "GET":
        return [
            to_dict(StoreItem, item)
            for item in query_search(StoreItem, request.args)
        ]
    else:
        print(f"Adding {request.json}")
        query_add(db.session, *from_json(StoreItem, request.json))

@rest_route("/lists", methods=["GET", "POST"])
def lists():
    if request.method == "GET":
        return [
            {**to_dict(CustomerList, obj), "items": to_json(CustomerItem, *obj.items)}
            for obj in query_search(CustomerList, request.args)
        ]
    else:
        json = request.json
        list = from_dict(CustomerList, json)
        query_add(db.session, list)
        query_add(db.session, *from_json(CustomerItem, json["items"]))

# GET: /<type>/<int:id>
@rest_route("/items/<int:id>")
def items_id(id):
    return to_dict(StoreItem, query_id(StoreItem, id))

@rest_route("/lists/<int:id>")
def lists_id(id):
    obj = query_id(CustomerList, id)
    return {**to_dict(CustomerList, obj), "items": to_json(CustomerItem, *obj.items)}

# GET: /eval?expr=<string>
@rest_route("/eval")
def expr():
    expr = request.args.get("expr", "None")
    return eval(expr)
