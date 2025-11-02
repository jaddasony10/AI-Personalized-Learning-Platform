from flask import Flask, request, jsonify
import quiz
import generativeResources
import translate
from flask_cors import CORS

api = Flask(__name__)
CORS(api)

@api.route("/api/v1/roadmap", methods=["POST"])
def get_roadmap():
    req = request.get_json()
    print("Received request for /api/roadmap with data:", req)

    # Lazy import roadmap to avoid raising on module import (e.g., missing GEMINI_API_KEY)
    try:
        import roadmap
    except Exception as imp_err:
        return jsonify({"error": "roadmap module import failed", "exception": str(imp_err)}), 500

    response_body = roadmap.create_roadmap(
        topic=req.get("topic", "Machine Learning"),
        time=req.get("time", "16 weeks"),
        knowledge_level=req.get("knowledge_level", "Absolute Beginner"),
    )

    # Return a stable envelope so clients always find response.roadmap
    return jsonify({"roadmap": response_body})


@api.route("/api/v1/quiz", methods=["POST"])
def get_quiz():
    req = request.get_json()
    print("Received request for /api/quiz with data:", req)

    course = req.get("course")
    topic = req.get("topic")
    subtopic = req.get("subtopic")
    description = req.get("description")

    if not (course and topic and subtopic and description):
        return jsonify({"error": "Required Fields not provided"}), 400

    print("Generating quiz...")
    response_body = quiz.get_quiz(course, topic, subtopic, description)
    return jsonify(response_body)


@api.route("/api/v1/translate", methods=["POST"])
def get_translations():
    req = request.get_json()
    print("Received request for /api/translate with data:", req)

    text = req.get("textArr")
    toLang = req.get("toLang")

    if not text or not toLang:
        return jsonify({"error": "Required Fields not provided"}), 400

    print(f"Translating to {toLang}: {text}")
    translated_text = translate.translate_text_arr(text_arr=text, target=toLang)
    return jsonify(translated_text)


@api.route("/api/v1/generate-resource", methods=["POST"])
def generative_resource():
    req = request.get_json()
    print("Received request for /api/generate-resource with data:", req)

    required_fields = ["course", "knowledge_level", "description", "time"]
    req_data = {key: req.get(key) for key in required_fields}

    if not all(req_data.values()):
        return jsonify({"error": "Required Fields not provided"}), 400

    print(f"Generating resources for {req_data['course']}")
    resources = generativeResources.generate_resources(**req_data)
    return jsonify(resources)


@api.route("/api/v1/roadmap/local", methods=["POST"])
def get_local_roadmap():
    """
    Explicit endpoint to return the deterministic local roadmap fallback.
    Useful when AI returns no usable steps.
    """
    req = request.get_json() or {}
    topic = req.get("topic", "Machine Learning")
    time = req.get("time", "8")
    knowledge_level = req.get("knowledge_level", "Absolute Beginner")

    try:
        import roadmap
    except Exception as imp_err:
        return jsonify({"error": "roadmap module import failed", "exception": str(imp_err)}), 500

    local = roadmap.generate_local_roadmap(topic, time, knowledge_level)
    return jsonify({"roadmap": local})


if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=5001)
