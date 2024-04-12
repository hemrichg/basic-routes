# TODO: import flask, send_file, request, make_response
from flask import Flask, send_file, request, make_response

# TODO: declare app, if __main__ run()
app = Flask(__name__)


# TODO: @app.get("/"), post, return GET/POST
@app.get("/")
def get_root():
    return "Content for GET"

@app.post("/")
def post_root():
    return "Content for POST"

# TODO: "/<path_param>", return path_param - cast?
@app.get("/param/<path_param>")
def get_path_param(path_param):
    return path_param

# TODO: request.args.get("queryparam") - cast?
@app.get("/param/query")
def get_query_param():
    return request.args.get("q")

# TODO: request.form["form-param"] - cast?
@app.post("/param/form")
def get_form_param():
    return request.form["password"]

# TODO: res = make_resp, res.set_cookie("key", "value")
@app.get("/set_cookie")
def get_scookie():
    response = make_response("Content for cookies")
    response.set_cookie("token", "Session")
    
    return response

# TODO: request.cookies.get("key")
@app.get("/get_cookie")
def get_gcookie():
    return request.cookies.get("token")


@app.get("/test")
def get_test():
    return send_file("test.html")


if __name__ == "__main__":
    app.run(debug=True)