from flask import jsonify, Blueprint
from src   import app


api = Blueprint("api", __name__, url_prefix="/")


# All routes are test functions at the moment, mostly for testing
# functionality and connectivity between server and Cassandra node(s).
@api.route("/",      methods=['GET'], strict_slashes=False)
@api.route("/index", methods=['GET'], strict_slashes=False)
def index() :
    return "Current funtion:<br> /createTable<br> /checkTable<br> /new/&lt;fname&gt;/&lt;lname&gt;/&lt;role&gt;<br> /newMovie/&lt;title&gt;/&lt;director&gt;/&lt;year&gt;<br> /getUsers<br> /getMovies<br>"


@api.route("/createTable", methods=['GET'], strict_slashes=False)
def create_table() :
    app.db.createTableUser()
    app.db.createTableMovie()
    return "success"


@api.route("/checkTable", methods=['GET'], strict_slashes=False)
def check_table() :
    name = "user"
    res = app.db.tableExists(name)
    return f"Table '{name}' exists: {res}"

@api.route("/new/<fname>/<lname>/<role>", methods=['GET'], strict_slashes=False)
def new_user(fname, lname, role) :
    app.db.createUser(fname, lname, role)
    return "success"

@api.route("/newMovie/<title>/<director>/<year>", methods=['GET'], strict_slashes=False)
def new_movie(title , director, year) :
    app.db.createMovie(title, director, year)
    return "success"


@api.route("/getUsers", methods=['GET'], strict_slashes=False)
def get_users() :
    def format_q(elt) :
        return f"{elt.user_id} : {elt.fname} {elt.lname}"

    res = app.db.getTable("person")

    return jsonify([format_q(i) for i in res])

@api.route("/getMovies", methods=['GET'], strict_slashes=False)
def get_movies() :
    def format_q(elt) :
        return f"{elt.title} {elt.director} {elt.year}"

    res = app.db.getTable("movie")

    return jsonify([format_q(i) for i in res])


