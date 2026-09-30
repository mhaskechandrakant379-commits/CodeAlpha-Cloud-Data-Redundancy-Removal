from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "codealpha-secret-key"

DATABASE = "data.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    connection = get_db_connection()

    users = connection.execute(
        "SELECT * FROM users ORDER BY id DESC"
    ).fetchall()

    total_records = connection.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    connection.close()

    return render_template(
        "index.html",
        users=users,
        total_records=total_records
    )


@app.route("/add", methods=["POST"])
def add_user():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()

    if not name or not email:
        flash("Name and email are required.", "error")
        return redirect(url_for("home"))

    connection = get_db_connection()

    existing_user = connection.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if existing_user:
        connection.close()
        flash(
            "Duplicate Data Detected! This email already exists.",
            "error"
        )
        return redirect(url_for("home"))

    connection.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email)
    )

    connection.commit()
    connection.close()

    flash("Unique data added successfully!", "success")

    return redirect(url_for("home"))


@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    connection.commit()
    connection.close()

    flash("Record deleted successfully.", "success")

    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)