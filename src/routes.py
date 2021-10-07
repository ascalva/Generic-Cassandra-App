from flask import jsonify, Blueprint
from src   import app


api = Blueprint("api", __name__, url_prefix="/")


@api.route("/",      methods=['GET'], strict_slashes=False)
@api.route("/index", methods=['GET'], strict_slashes=False)
def index() :
    return "hello world"


@api.route("/createTable", methods=['GET'], strict_slashes=False)
def create_table() :
    app.db.createTableUser()
    return "maybe"


@api.route("/new", methods=['GET'], strict_slashes=False)
def new_user() :
    app.db.createUser("ascalva", "alberto", "serrano")
    return "maybe"


@api.route("/check", methods=['GET'], strict_slashes=False)
def check() :
    def format_q(elt) :
        return f"{elt.uname} : {elt.fname} {elt.lname}"

    res = app.db.getTable("user")

    return jsonify([format_q(i) for i in res])


@api.route("/checkT", methods=['GET'], strict_slashes=False)
def check_table() :
    name = "user"
    res = app.db.tableExists(name)
    return f"Table '{name}' exists: {res}"

