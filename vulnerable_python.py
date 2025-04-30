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
    #return subprocess.check_output("echo " + cmd, shell=True)
    output = subprocess.check_output(["echo", cmd])
    return output.decode()

@app.route("/eval", methods=["POST"])
def eval_code():
    #code = request.form.get("code")
    # 🧨 Arbitrary code execution vulnerability
    #return str(eval(code))
    #The fixed code will look as below 
    code = request.form.get("code")
    try:
        result = ast.literal_eval(code)
    except (ValueError, SyntaxError):
        result = "Invalid input"
    return str(result)

def insecure_hashing(password):
    #Changing to secure hashing
    import hashlib
    import base64
    # 🧨 Insecure hashing algorithm (MD5)
    #return hashlib.md5(password.encode()).hexdigest()
    salt = os.urandom(16)

    # Hash the password using scrypt
    key = hashlib.scrypt(
        password.encode(),
        salt=salt,
        n=2**14,       # CPU/memory cost factor (16384)
        r=8,           # block size
        p=1,           # parallelization factor
        dklen=64       # desired key length
    )

    # Store salt and hash together (base64-encoded)
    return base64.b64encode(salt + key).decode()

# 🧨 Unsafe YAML loading
import yaml
def load_yaml(yaml_str):
    return yaml.load(yaml_str)
