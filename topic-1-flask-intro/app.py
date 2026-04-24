from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    text = "This is a note!!!!!"
    return render_template("index.html",message=text)

@app.route("/hello/<name>")
@app.route("/hello")
def hello(name="World"):
    text = f"Hello, {name}!"
    return render_template("index.html",message=text)

if __name__ == "__main__":
    app.run(debug=True)
