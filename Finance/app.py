import datetime
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    index = db.execute(
        "SELECT symbol, SUM(shares) AS shares, price FROM history WHERE uid = ? GROUP BY symbol", session["user_id"])

    total = 0
    for stock in index:
        stock["price"] = float(lookup(stock["symbol"])["price"])
        stock["shares"] = int(stock["shares"])
        total += stock["price"] * stock["shares"]

    # for i in index["symbol"]

    usercash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    return render_template("index.html", index=index, usercash=usercash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Ensure form is not blank
        if not request.form.get("symbol"):
            return apology("must provide a symbol")

        if not request.form.get("shares"):
            return apology("specify amount")

        # ensure symbol exists
        if not lookup(request.form.get("symbol")):
            return apology("invalid symbol")

        # ensure shares is an integer
        try:
            int(request.form.get("shares"))
        except:
            return apology("invalid shares", 400)
        # ensure shares isnt less than 1
        if int(request.form.get("shares")) < 1:
            return apology("invalid shares", 400)

        # process payment
        uid = session["user_id"]

        value = float(lookup(request.form.get("symbol"))["price"]) * int(request.form.get("shares"))

        usercash = float(db.execute("SELECT cash FROM users WHERE id = ?", uid)[0]["cash"])

        # if user money minus value of stock times amount chosen is less than zero
        if usercash - value < 0:
            return apology("too poor")

        else:
            # subtract money
            db.execute("UPDATE users SET cash = ? WHERE id = ?",
                       usercash - value, session["user_id"])
            # log
            symbol = request.form.get("symbol").upper()
            shares = request.form.get("shares")
            transacted = datetime.datetime.utcnow()
            db.execute("INSERT INTO history (uid, symbol, shares, price, transacted) VALUES (?, ?, ?, ?, ?)",
                       uid, symbol, shares, value, transacted)

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute(
        "SELECT symbol, shares, price, transacted FROM history WHERE uid = ?", session["user_id"])
    return render_template("history.html", history=history)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        # checks for any irregularities in password
        user_id = session["user_id"]
        if not request.form.get("password"):
            return apology("Must Provide Password!", 403)
        if not request.form.get("new_password"):
            return apology("Must Provide New Password!", 403)
        if not request.form.get("confirm_password"):
            return apology("Must Confirm New Password!", 403)

        # checks if new pw is the same
        newpw = request.form.get("new_password")
        new_hash = generate_password_hash(newpw, method='scrypt', salt_length=16)
        userpw = db.execute("SELECT hash FROM users WHERE id = ?", user_id)[0]["hash"]

        if not check_password_hash(userpw, request.form.get("password")):
            return apology("Incorrect Password", 400)
        if newpw != request.form.get("confirm_password"):
            return apology("passwords do not match", 403)
        if newpw == request.form.get("password"):
            return apology("New Password is same as your password", 403)

        # changes pw
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, user_id)

        return redirect("/")

    else:
        return render_template("change_password.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        key = request.form.get("symbol")

        if not lookup(key):
            return apology("invalid share")

        else:
            return render_template("quoted.html", key=lookup(key))

    # user requested get method
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # user submitted register form
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # ensure confirmation is correct
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords do not match", 400)

        # vars for password and username
        username = request.form.get("username")
        password = request.form.get("password")

        # see if username is already taken
        if db.execute("SELECT username FROM users WHERE username = ?", username):
            return apology("username already taken")

        # create user in db
        hashed = generate_password_hash(password, method='scrypt', salt_length=16)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed)

        # log user in and return to /

        # Remember which user has logged in
        session["user_id"] = db.execute(
            "SELECT id FROM users WHERE username = ? AND hash = ?", username, hashed)[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # user requested get method
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Ensure form is not blank
        if not request.form.get("symbol"):
            return apology("must provide a symbol")

        if not request.form.get("shares"):
            return apology("specify amount")

        # ensure symbol exists
        if not lookup(request.form.get("symbol")):
            return apology("invalid symbol")

        # ensure shares is an integer
        try:
            int(request.form.get("shares"))
        except:
            return apology("invalid shares", 400)
        # ensure shares isnt less than 1
        if int(request.form.get("shares")) < 1:
            return apology("invalid shares", 400)
        # ensures user has shares
        share = db.execute("SELECT SUM(shares) AS shares, price FROM history WHERE uid = ? AND symbol = ?",
                           session["user_id"], request.form.get("symbol"))

        if int(request.form.get("shares")) > share[0]["shares"]:
            return apology("Too many shares!", 400)

        # calculate transaction
        cash = int(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])
        # add share value to acc
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + (lookup(request.form.get("symbol"))
                   ["price"] * int(request.form.get("shares"))), session["user_id"])
        # remove amount of shares from acc
        uid = session["user_id"]
        symbol = request.form.get("symbol").upper()
        shares = 0
        shares = - int(request.form.get("shares"))
        value = lookup(request.form.get("symbol"))["price"] * int(request.form.get("shares"))
        transacted = datetime.datetime.utcnow()
        db.execute("INSERT INTO history (uid, symbol, shares, price, transacted) VALUES (?, ?, ?, ?, ?)",
                   uid, symbol, shares, value, transacted)

        return redirect("/")

    else:
        return render_template("sell.html", symbol=db.execute("SELECT symbol FROM history WHERE uid = ? GROUP by symbol", session["user_id"])[0]["symbol"])
