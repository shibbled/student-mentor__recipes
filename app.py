from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    buttons = [
        {"title": "Home", "url": "/"},
        {"title": "Find by Category", "url": "/category"}
    ]
    return render_template('index.html', buttons=buttons)

if __name__ ==  "__main__":
    app.run(debug = True)