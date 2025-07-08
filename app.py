from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import check_password_hash
import psycopg2
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

load_dotenv()

# Flask App
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Check database config
db_url = os.getenv("DATABASE_URL")
if not db_url:
  print("⚠️ DATABASE_URL is not set!")

# Connect to PostgreSQL
def get_db_connection():
  return psycopg2.connect(db_url)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


# ==============================
# HOME PAGE
# ==============================
@app.route('/')
def index():
  buttons = [
    {"title": "Home", "url": "/"},
    {"title": "Find by Category", "url": "/category"}
  ]
  categories = [
    "Vegetarian",
    "Vegan",
    "Meat",
    "Fish",
    "Cake",
    "Breakfast",
    "Lunch",
    "Dinner",
  ]
  return render_template('index.html', buttons=buttons, categories=categories)


# ==============================
# HANDLER : LOGIN
# ==============================
@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    username = request.form["username"].strip()
    password = request.form["password"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    if user is not None and check_password_hash(user[1], password):
      session["logged_in"] = True
      session["user_id"] = user[0]
      session["username"] = username
      return redirect(url_for("admin_panel"))
    else:
      flash("Incorrect username or password")

  return render_template("login.html")


# ==============================
# LOGOUT
# ==============================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ==============================
# ADMIN
# ==============================
@app.route("/admin")
def admin_panel():
  if not session.get("logged_in"):
    return redirect(url_for("login"))
  
  conn = get_db_connection()
  cur = conn.cursor()

  user_id = session["user_id"]
  cur.execute("SELECT id, title, author, ingredients, instructions, categories, image_url FROM recipes WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
  recipes = cur.fetchall()

  return render_template("admin.html", recipes=recipes)


if __name__ ==  "__main__":
  app.run(debug = True)