from flask import Flask

app = Flask(__name__)

@app.route("/")
def login_form():
    return "home"

if __name__ == "main":
    app.run()