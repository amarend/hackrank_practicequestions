from flask import Flask, request, render_template_string, redirect, jsonify
import subprocess
import pickle
import sqlite3
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = sqlite3.connect(':memory:', check_same_thread=False)
cursor = db.cursor()

# 1. SQL Injection
#@app.route("/user")
#def get_user():
#    username = request.args.get("username")
#    #query = "SELECT * FROM users WHERE username = '%s'" % username
#    #cursor.execute(query)
#    query = "SELECT * FROM users WHERE username = ?"
#    cursor.execute(query, (username,))
#    return str(cursor.fetchall())

@app.route("/user")
def get_user():
    username = request.args.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'id': user.id, 'username': user.username})
    else:
        return jsonify({'error': 'User not found'}), 404

# 2. Command Injection
@app.route("/ping")
def ping():
    ip = request.args.get("ip")
    #Shell true can cause failures so we can use the []
    
    #return subprocess.check_output("ping -c 1 " + ip, shell=True)
    return subprocess.check_output(['ping', '-c', '1' , ip])

# 3. Insecure Deserialization
@app.route("/load", methods=["POST"])
def load_data():
    import json
    data = request.form.get("data")
    #obj = pickle.loads(data.encode())
    try:
       obj = json.loads(data)
    except json.JSONDecodeError:
        return "Invalid input"
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
    value_of_name="<h1>Hello {{ name }}</h1>"
    return render_template_string("{{ value_of_name|safe }}", name=value_of_name)


# 6. Use of eval
@app.route("/calc")
def calc():
    import ast
    expr = request.args.get("expr")
    value = ast.literal_eval(expr)
    return value

# 7. Unrestricted File Upload
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    file.save("/uploads/" + file.filename)
    return "File uploaded!"

# 8. Unvalidated Redirect
#@app.route("/go")
#def go():
#    url = request.args.get("next")
#    return redirect(url)


@app.route("/go")
def go():
    from werkzeug.urls import url_parse
    next_url = request.args.get("next", "/")
    parsed_url = url_parse(next_url)

    # Allow only internal redirects (no netloc)
    if parsed_url.netloc == "":
        return redirect(next_url)
    return redirect(url_for("home"))
    
if __name__ == "__main__":
    app.run(debug=False)

