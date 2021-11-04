from flask import jsonify, Blueprint, render_template, request
from src   import app


api = Blueprint("api", __name__, url_prefix="/")


# All routes are test functions at the moment, mostly for testing
# functionality and connectivity between server and Cassandra node(s).
@api.route("/",      methods=['GET'], strict_slashes=False)
@api.route("/index", methods=['GET'], strict_slashes=False)
def index() :
    return render_template("home.html")
    # return "Current funtion:<br> /createTable<br> /checkTable<br> /new/&lt;fname&gt;/&lt;lname&gt;/&lt;role&gt;<br> /newMovie/&lt;title&gt;/&lt;director&gt;/&lt;year&gt;<br> /getUsers<br> /getMovies<br>"


@api.route("/getUsers", methods=['GET'], strict_slashes=False)
def getUsers() :
    out_dic = {}

    for p in app.db.getTable("person") :
        out_dic[str(p.user_id)] = {"name" : f"{p.fname} {p.lname}", "role" : p.role}

    return jsonify(out_dic)


@api.route("/getMovies", methods=['GET'], strict_slashes=False)
def getMovies() :
    out_dic = {}
    for m in app.db.getTable("movie") :
        out_dic[m.title] = {"year" : m.year, "director" : m.director}

    return jsonify(out_dic)


@api.route("/createPerson", methods=['GET', 'POST'], strict_slashes=False)
def createPerson() :
    if request.method == "POST" :
        fname = request.form['fname']
        lname = request.form['lname']
        role  = request.form['role']

        app.db.createPerson(fname, lname, role)
        return "success"

    return render_template("create_person.html")


@api.route("/createMovie", methods=['GET', 'POST'], strict_slashes=False)
def createMovie() :
    if request.method == "POST" :
        movie_name = request.form['movie_name']
        director   = request.form['director']
        year       = int(request.form['year'])

        app.db.createMovie(movie_name, director, year)
        return "success"

    return render_template("create_movie.html")

