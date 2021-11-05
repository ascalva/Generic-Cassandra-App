from flask import jsonify, Blueprint, render_template, request
from src   import app


api = Blueprint("api", __name__, url_prefix="/")


# All routes are test functions at the moment, mostly for testing
# functionality and connectivity between server and Cassandra node(s).
@api.route("/",      methods=['GET'], strict_slashes=False)
@api.route("/index", methods=['GET'], strict_slashes=False)
def index() :
    return render_template("home.html")


@api.route("/getUsers", methods=['GET'], strict_slashes=False)
def getUsers() :
    out_dic = {}

    for p in app.db.getTable("person") :
        out_dic[str(p.user_id)] = {"name" : f"{p.fname} {p.lname}", "role" : p.role}

    return jsonify(out_dic)


@api.route("/getMovie", methods=['GET', 'POST'], strict_slashes=False)
def getMovie() :
    out_dic = {}
    if request.method == "POST" :
        movie_name = request.form['movie_name']
        for m in app.db.getMovie(movie_name):
            out_dic[m.title] = {"year": m.year, "director": m.director}
        return jsonify(out_dic)

    return render_template("get_movie.html")

@api.route("/getPerson", methods=['GET', 'POST'], strict_slashes=False)
def getPerson() :
    out_dic = {}
    if request.method == "POST" :
        fname = request.form['fname']
        lname = request.form['lname']
        for p in app.db.getPerson(fname,lname):
            out_dic[str(p.user_id)] = {"name" : f"{p.fname} {p.lname}", "role" : p.role}
        return jsonify(out_dic)

    return render_template("get_person.html")

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
        return render_template("home.html")

    return render_template("create_person.html")


@api.route("/createMovie", methods=['GET', 'POST'], strict_slashes=False)
def createMovie() :
    if request.method == "POST" :
        movie_name = request.form['movie_name']
        director   = request.form['director']
        year       = int(request.form['year'])

        app.db.createMovie(movie_name, director, year)
        return render_template("home.html")

    return render_template("create_movie.html")

@api.route("/removePerson", methods=['GET', 'POST'], strict_slashes=False)
def removePerson() :
    out_dic = {}
    if request.method == "POST" :
        fname = request.form['fname']
        lname = request.form['lname']
        app.db.removePerson(fname,lname)
        return render_template("home.html")

    return render_template("remove_person.html")

@api.route("/removeMovie", methods=['GET', 'POST'], strict_slashes=False)
def removeMovie() :
    out_dic = {}
    if request.method == "POST" :
        movie_name = request.form['movie_name']
        app.db.removeMovie(movie_name)
        return render_template("home.html")

    return render_template("remove_movie.html")
