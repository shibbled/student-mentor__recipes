from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import check_password_hash
from app.db import get_db_connection

auth = Blueprint("auth", __name__)


# ==============================
# LOGIN
# ==============================
@auth.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash, forename FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    conn.close()

    if user and check_password_hash(user[1], password):
      session["user_id"] = user[0]
      session["username"] = username
      session["forename"] = user[2]
      session["logged_in"] = True
      return redirect(url_for("auth.admin_panel"))
        
    else:
      flash("Incorrect username or password")

  return render_template("pages/admin/login.html")


# ==============================
# ADMIN
# ==============================
@auth.route("/admin")
def admin_panel():
  if not session.get("logged_in"):
    return redirect(url_for("auth.login"))

  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("SELECT title FROM recipes WHERE user_id = %s", (session["user_id"],))
  recipes = cur.fetchall()
  conn.close()
  return render_template("pages/admin/dashboard.html", recipes=recipes)


# ==============================
# LOGOUT
# ==============================
@auth.route("/logout")
def logout():
  session.clear()
  return redirect(url_for("index.home"))
