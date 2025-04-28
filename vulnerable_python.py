import os
import subprocess
import flask
from flask import request

app = flask.Flask(__name__)

# Hardcoded secret
API_KEY = "1234567890abcdef"

@app.route("/run", methods=["POST"])
def run_command():
    cmd = request.form.get("cmd")
    # 🧨 Potential command injection vulnerability
    return subprocess.check_output("echo " + cmd, shell=True)

@app.route("/eval", methods=["POST"])
def eval_code():
    code = request.form.get("code")
    # 🧨 Arbitrary code execution vulnerability
    return str(eval(code))

def insecure_hashing(password):
    import hashlib
    # 🧨 Insecure hashing algorithm (MD5)
    return hashlib.md5(password.encode()).hexdigest()

# 🧨 Unsafe YAML loading
import yaml
def load_yaml(yaml_str):
    return yaml.load(yaml_str)
