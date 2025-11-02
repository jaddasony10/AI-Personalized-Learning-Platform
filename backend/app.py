import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from jinja2 import TemplateNotFound

# Initialize Flask app
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "src"))
CORS(app)

@app.route("/")
def home():
    """Serve the frontend (index.html)"""
    try:
        return render_template("index.html")
    except TemplateNotFound:
        # Attempt to serve a static index.html from the src folder if it exists
        src_dir = app.template_folder
        index_path = os.path.join(src_dir, "index.html")
        if os.path.isfile(index_path):
            return send_from_directory(src_dir, "index.html")
        # Fallback simple HTML response to avoid TemplateNotFound crash
        return (
            "<!doctype html><html><head><title>App</title></head>"
            "<body><h1>Frontend not found</h1><p>Place index.html in the 'src' folder "
            "or check your template_folder configuration.</p></body></html>"
        )

@app.route("/api/v1/roadmap", methods=["POST"])
def roadmap():
    """
    API Endpoint to generate a learning roadmap using Gemini API.
    """
    try:
        # Lazy import to avoid import-time failures if GEMINI_API_KEY is missing
        from roadmap import generate_learning_path

        data = request.get_json()
        topic = data.get("topic")
        time = data.get("time")
        knowledge_level = data.get("knowledge_level")

        if not topic or not time or not knowledge_level:
            return jsonify({"error": "Missing required fields"}), 400

        # Generate roadmap using Gemini API (or fallback)
        learning_path = generate_learning_path(topic, time, knowledge_level)

        # Return consistent envelope to match base.py responses
        return jsonify({"roadmap": learning_path})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/v1/roadmap/local", methods=["POST"])
def roadmap_local():
    """
    Explicit endpoint to return the deterministic local roadmap fallback.
    Matches the envelope returned by base.py so the frontend can always render.
    """
    try:
        from roadmap import generate_local_roadmap
    except Exception as imp_err:
        return jsonify({"error": "roadmap module import failed", "exception": str(imp_err)}), 500

    data = request.get_json() or {}
    topic = data.get("topic", "Machine Learning")
    time = data.get("time", "8")
    knowledge_level = data.get("knowledge_level", "Absolute Beginner")

    try:
        local = generate_local_roadmap(topic, time, knowledge_level)
        return jsonify({"roadmap": local})
    except Exception as e:
        return jsonify({"error": "Failed to generate local roadmap", "exception": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)