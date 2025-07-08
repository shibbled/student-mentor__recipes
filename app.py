from flask import Flask, render_template, request, redirect
import os
import psycopg2
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

load_dotenv()

# Flask App
app = Flask(__name__)

# Connect to PostgreSQL
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Home page
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

# Upload handler
@app.route("/upload", methods=["POST"])
def upload_recipe():
    title = request.form["title"]
    author = request.form["author"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]
    categories = request.form["categories"]
    file = request.files["image"]

    # Upload to Cloudinary
    result = cloudinary.uploader.upload(file)
    image_url = result["secure_url"]

    # Store in PostgreSQL
    cur.execute(
        "INSERT INTO recipes (title, author, ingredients, instructions, categories, image_url) VALUES (%s, %s, %s, %s, %s, %s)",
        (title, author, ingredients, instructions, categories, image_url)
    )
    conn.commit()

    return redirect("/")


if __name__ ==  "__main__":
  app.run(debug = True)