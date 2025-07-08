from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ ==  "__main__":
  app.run(debug = True)