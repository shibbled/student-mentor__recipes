from flask import Blueprint, render_template, session, redirect, url_for
from app.db import get_db_connection

recipe = Blueprint("recipe", __name__)

@recipe.route("/user-recipes")
def user_recipes():
    
  user_id = session.get("user_id")

  # if not user_id:
  #     return redirect(url_for("main.login"))

  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("SELECT id, title FROM recipes WHERE user_id = %s", (user_id,))

  recipes = cur.fetchall()
  cur.close()
  conn.close()

  return render_template("pages/recipes/list.html", recipes=recipes)