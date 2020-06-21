import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from passlib.apps import custom_app_context as pwd_context


from helpers import apology, login_required

# Configure application
app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///naturalhair.db")

@app.route("/")
@login_required
def index():
    return render_template("index.html")

    # no need to return an apology

#helps with login function
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("You must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("You must provide password", 403)
            # must provide error codes

        # Query database for username
        storeduser = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(storeduser) != 1 or not pwd_context.verify(request.form.get("password"), storeduser[0]["hash"]):
            return apology("You have entered an invalid username or password", 403)

        # Remember which user has logged in
        session["user_id"] = storeduser[0]["id"]

        # Redirect user to home page
        return index()

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



#redirects to entry page
@app.route("/entry", methods=["GET", "POST"])
@login_required
def entry():
    """Add a journal entry!"""
    if request.method == "POST":

        style = request.form.get("style")
        product = request.form.get("product")
        feelings = request.form.get("feelings")

        db.execute("INSERT INTO journal (style,product,feelings,id) VALUES(:style,:product,:feelings,:id)",
                   style=style, product=product, feelings=feelings, id=session["user_id"])

        return render_template("index.html")
    else:
        return render_template("entry.html")

#redirect to journal--> where the entry is printed
@app.route("/journal")
@login_required
def journal():
    journal = db.execute("SELECT * FROM journal WHERE id=:id", id=session["user_id"])
    journalData = []
    for row in journal:
        newRow = dict()
        newRow["style"] = row["style"]
        newRow["product"] = row["product"]
        newRow["feelings"] = row["feelings"]
        journalData.append(newRow)

    return render_template("journal.html", journalData=journalData)

#redirect to resoruces
@app.route("/resources", methods=["GET", "POST"])
@login_required
def resources():
    """Display user profile"""
    if request.method == "POST":
        return index()

    else:
        return render_template("resources.html")

#redirects to introduction page
@app.route("/introduction", methods=["GET", "POST"])
@login_required
def introduction():
    if request.method == "POST":
        return index()

    else:
        return render_template("introduction.html")

#redirects to climate page
@app.route("/climate", methods=["GET", "POST"])
@login_required
def climate():
    """Display user profile"""
    if request.method == "POST":
        return index()

    else:
        return render_template("climate.html")

#redirect to curl patterns
@app.route("/curlpatterns", methods=["GET", "POST"])
@login_required
def curlpatterns():
    """Display user profile"""
    if request.method == "POST":
        return index()

    else:
        return render_template("curlpatterns.html")

#redirects to individual page
@app.route("/individual", methods=["GET", "POST"])
@login_required
def individual():
    """Display user profile"""
    if request.method == "POST":
        return index()

    else:
        return render_template("individual.html")

#redirect to products
@app.route("/products", methods=["GET", "POST"])
@login_required
def products():
    """Display user profile"""
    if request.method == "POST":
        return index()

    else:
        return render_template("products.html")

#redirects to porosity page
@app.route("/porosity", methods=["GET", "POST"])
@login_required
def porosity():
    """Display user profile"""
    if request.method == "POST":
        return index()

    else:
        return render_template("porosity.html")

#redirects to about page
@app.route("/about", methods=["GET", "POST"])
def about():
   return render_template("about.html")


#redirects to join page
@app.route("/join", methods=["GET", "POST"])
def join():
    """Register user"""
    session.clear()
    # gets rid of the previous user

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("You must input a username!")
            # must input a username

        elif not request.form.get("password"):
            return apology("You must input a password")

       # inserting the inforamtion into a database to be accessed later.
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"), hash=pwd_context.hash(request.form.get("password")))
        # hash is now equal to the encyrpted password
        if not result:
            return apology("Someone already has this username")
            #aleritng for someone else's username

        storeduser = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
       # now accessing the speciifc user's information

        if len(storeduser) != 1 or not pwd_context.verify(request.form.get("password"), storeduser[0]["hash"]):
            return apology("Username already exists", 403)
            # must have the exit rcode

        session["user_id"] = storeduser[0]["id"]

        return render_template("index.html")
        # now redirecting them to their homepage

    else:
        return render_template("join.html")
        # or else back to the register.html page


#allows for one to post in the chat room
@app.route("/chatroom", methods=["GET", "POST"])
def chatroom():
    """Access chatroom"""
    if request.method == "GET":
        messages = db.execute("SELECT * FROM chatroom")
        messages.reverse()
        for i in range(0, len(messages)):
            messages[i]["is_self"] = (int(messages[i]["sender_id"]) == int(session["user_id"]))
            messages[i]["sender"] = db.execute("SELECT username FROM users WHERE id = :id", id=messages[i]["sender_id"])[0]["username"]
        return render_template("chatroom.html", messages=messages)
    else:
        message = request.form.get("message")
        if not message:
            return redirect("/chatroom")

        db.execute("INSERT INTO chatroom (sender_id, message) VALUES (:id, :message)", id=session["user_id"], message=message)

        return redirect("/chatroom")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

#as a disclaimer I know that my website doesn't update the buying of shares, however, I was unsure hwo to fix this problem within my database.