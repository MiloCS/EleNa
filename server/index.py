from flask import Flask, request

app = Flask(__name__)


@app.route('/max_route')
def min_route():
    source = request.args["source"]
    dest = request.args["dest"]
    dist = request.args["percent"]

    return []


@app.route('min_route')
def max_route():
    source = request.args["source"]
    dest = request.args["dest"]
    dist = request.args["percent"]

    return []

if __name__ == "__main__":
    app.run(port=8080)