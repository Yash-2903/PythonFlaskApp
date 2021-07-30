from flask import Markup, make_response, request, jsonify
from flask import current_app as app
from flask import render_template
from .logic import square_of_number_plus_nine


@app.route("/logic")
def logic():
    value = square_of_number_plus_nine(5)
    return str(value)


@app.route("/markup")
def markup():
    return Markup("<h1>Hello World!</h1>")


@app.route("/template")
def hello_template():
    return render_template("index.html")


@app.route("/response")
def response():
    headers = {"Content-Type": "application/json"}
    return make_response('it worked!', 200, headers)


@app.route("/get", methods=['GET'])
def get_hello():
    if request.method != 'GET':
        return make_response('Malformed request', 400)
    headers = {"Content-Type": "application/json"}
    return make_response('it worked!', 200, headers)


@app.route("/Initial", methods=['GET'])
def hello():
    if request.method != 'GET':
        return make_response('Malformed request', 400)
    my_dict = {'key': 'dictionary value'}
    headers = {"Content-Type": "application/json"}
    return make_response(jsonify(my_dict), 200, headers)
