from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")
    if username == "admin" and password == "password":
        return jsonify({"success": True, "message": f"Welcome, {username}!"})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401


@app.route("/api/greet", methods=["POST"])
def api_greet():
    data = request.get_json()
    name = data.get("name", "World")
    return jsonify({"greeting": f"Hello, {name}!"})


@app.route("/api/search", methods=["GET"])
def api_search():
    query = request.args.get("q", "")
    items = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape"]
    results = [i for i in items if query.lower() in i.lower()] if query else items
    return jsonify({"results": results, "query": query})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
