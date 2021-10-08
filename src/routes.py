from flask import jsonify, Blueprint
from src   import app


api = Blueprint("api", __name__, url_prefix="/")


# All routes are test functions at the moment, mostly for testing
# functionality and connectivity between server and Cassandra node(s).
@api.route("/",      methods=['GET'], strict_slashes=False)
@api.route("/index", methods=['GET'], strict_slashes=False)
def index() :
    return "work in progress"


@api.route("/createTable", methods=['GET'], strict_slashes=False)
def create_table() :
    app.db.createTableUser()
    return "success"


@api.route("/checkTable", methods=['GET'], strict_slashes=False)
def check_table() :
    name = "user"
    res = app.db.tableExists(name)
    return f"Table '{name}' exists: {res}"


@api.route("/new/<uname>/<fname>/<lname>", methods=['GET'], strict_slashes=False)
def new_user(uname, fname, lname) :
    app.db.createUser(uname, fname, lname)
    return "success"


@api.route("/getUsers", methods=['GET'], strict_slashes=False)
def get_users() :
    def format_q(elt) :
        return f"{elt.uname} : {elt.fname} {elt.lname}"

    res = app.db.getTable("user")

    return jsonify([format_q(i) for i in res])


