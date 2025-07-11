from flask import Blueprint, render_template, session, redirect, url_for
from app.db import get_db_connection

recipe_bp = Blueprint("recipes", __name__)

@recipe_bp.route("/admin")
def admin_panel():
    if not session.get("logged_in"):
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT title FROM recipes WHERE user_id = %s", (session["user_id"],))
    recipes = cur.fetchall()
    conn.close()
    return render_template("pages/admin/dashboard.html", recipes=recipes)
