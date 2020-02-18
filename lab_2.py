from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index1():
    return "hello"


@app.route("/hello1")
def index2():
    return render_template("index.html")


@app.route("/andriy")
def index3():
    return "<h1>Andriy <span style=\'color: red\'>❤<span></h1>"


if __name__ == "__main__":
    app.run(debug=True)

    index2()
    index3()
