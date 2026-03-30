from flask import Flask, render_template, request, jsonify
from chatbot import get_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    domain = data.get("domain", "")

    full_query = f"{domain} {message}".strip()
    response = get_response(full_query)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
