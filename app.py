import os
import sqlite3
from flask import Flask, g, render_template_string, request, redirect, url_for
from datetime import datetime, timezone

# -------------------------------------------------------------------
# Config
# -------------------------------------------------------------------
APP_TITLE = "MAB Media – Recipe Generator"
DATABASE = "recipes.db"

app = Flask(__name__)

# -------------------------------------------------------------------
# Database helpers
# -------------------------------------------------------------------
def get_db():
    if "_db" not in g:
        g._db = sqlite3.connect(DATABASE)
        g._db.row_factory = sqlite3.Row
    return g._db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("_db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            recipe TEXT NOT NULL,
            image_url TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    db.commit()

# -------------------------------------------------------------------
# Image fetcher (loremflickr)
# -------------------------------------------------------------------
def image_for_query(query: str) -> tuple[str, str]:
    query_safe = query.replace(" ", "+")
    img_url = f"https://loremflickr.com/640/480/{query_safe}"
    return img_url, query

# -------------------------------------------------------------------
# Fake recipe generator
# -------------------------------------------------------------------
def generate_recipe(dish: str) -> str:
    return f"""
Ingredients:
- 2 cups {dish}
- 1 tsp salt
- 1 tbsp olive oil
- Herbs to taste

Instructions:
1. Preheat oven to 180°C.
2. Mix {dish} with salt and herbs.
3. Drizzle olive oil.
4. Bake for 20 minutes.
5. Serve hot and enjoy!
"""

# -------------------------------------------------------------------
# Combined HTML Template
# -------------------------------------------------------------------
# Combine the base and content templates into one for single-pass rendering.
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #F5B027;
        }
        h1, h2 {
            text-align: center;
        }
        form {
            text-align: center;
            margin-bottom: 20px;
        }
        input[type=text] {
            width: 300px;
            padding: 10px;
            margin-right: 10px;
        }
        input[type=submit] {
            padding: 10px 20px;
        }
        .recipe {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 20px auto;
            max-width: 600px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        img {
            max-width: 100%;
            border-radius: 8px;
            margin-top: 10px;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    <form method="post">
        <input type="text" name="dish" placeholder="Enter a dish..." required>
        <input type="submit" value="Generate Recipe">
    </form>

    {% for r in recipes %}
    <div class="recipe">
        <h2>{{ r['query'] }}</h2>
        <pre>{{ r['recipe'] }}</pre>
        {% if r['image_url'] %}
        <img src="{{ r['image_url'] }}" alt="{{ r['query'] }}">
        {% endif %}
        <p><small>Created at: {{ r['created_at'] }}</small></p>
    </div>
    {% endfor %}

    <div class="footer">
        <p>Powered by {{ title }}</p>
    </div>
</body>
</html>
"""

# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    init_db()
    db = get_db()

    if request.method == "POST":
        dish = request.form["dish"].strip()
        if dish:
            recipe = generate_recipe(dish)
            image_url, _ = image_for_query(dish)
            db.execute(
                "INSERT INTO recipes (query, recipe, image_url, created_at) VALUES (?, ?, ?, ?)",
                (dish, recipe, image_url, datetime.now(timezone.utc).isoformat())
            )
            db.commit()
            return redirect(url_for("index"))

    # fetch latest recipes
    cur = db.execute("SELECT * FROM recipes ORDER BY id DESC")
    recipes = cur.fetchall()

    return render_template_string(
        TEMPLATE,
        title=APP_TITLE,
        recipes=recipes
    )

# -------------------------------------------------------------------
# Run app
# -------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)