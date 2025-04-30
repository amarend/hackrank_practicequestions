from flask import Flask, request, render_template_string, redirect
import subprocess
import pickle
import sqlite3
import os

app = Flask(__name__)
db = sqlite3.connect(':memory:', check_same_thread=False)
cursor = db.cursor()

# 1. SQL Injection
@app.route("/user")
def get_user():
    username = request.args.get("username")
    query = "SELECT * FROM users WHERE username = '%s'" % username
    cursor.execute(query)
    return str(cursor.fetchall())

# 2. Command Injection
@app.route("/ping")
def ping():
    ip = request.args.get("ip")
    return subprocess.check_output("ping -c 1 " + ip, shell=True)

# 3. Insecure Deserialization
@app.route("/load", methods=["POST"])
def load_data():
    data = request.form.get("data")
    obj = pickle.loads(data.encode())
    return str(obj)

# 4. Hardcoded Credentials
def connect():
    username = "admin"
    password = "123456"
    return login(username, password)

def login(user, pwd):
    return f"Logging in {user} with password {pwd}"

# 5. XSS via render_template_string
@app.route("/greet")
def greet():
    name = request.args.get("name")
    return render_template_string("<h1>Hello {{ name }}</h1>", name=name)

# 6. Use of eval
@app.route("/calc")
def calc():
    expr = request.args.get("expr")
    return str(eval(expr))

# 7. Unrestricted File Upload
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    file.save("/uploads/" + file.filename)
    return "File uploaded!"

# 8. Unvalidated Redirect
@app.route("/go")
def go():
    url = request.args.get("next")
    return redirect(url)

if __name__ == "__main__":
    app.run(debug=True)

