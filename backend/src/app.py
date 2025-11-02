from flask import Flask, request, jsonify
import roadmap
import quiz
import generativeResources
import translate
from flask_cors import CORS

# Initialize Flask app
api = Flask(__name__)
CORS(api)

# Home Route to Check API Status
@api.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Internal API is running!"})

# Route for Generating Roadmap
@api.route("/api/v1/roadmap", methods=["POST"])
def get_roadmap():
    try:
        req = request.get_json()
        print("Received request for /api/v1/roadmap with data:", req)

        if not req:
            return jsonify({"error": "Invalid JSON request"}), 400

        topic = req.get("topic", "Machine Learning")
        time = req.get("time", "4 weeks")
        knowledge_level = req.get("knowledge_level", "Absolute Beginner")

        response_body = roadmap.create_roadmap(topic=topic, time=time, knowledge_level=knowledge_level)
        return jsonify(response_body)

    except Exception as e:
        print(f"Error in /api/v1/roadmap: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Route for Quiz Generation
@api.route("/api/v1/quiz", methods=["POST"])
def get_quiz():
    try:
        req = request.get_json()
        print("Received request for /api/v1/quiz with data:", req)

        course = req.get("course")
        topic = req.get("topic")
        subtopic = req.get("subtopic")
        description = req.get("description")

        if not (course and topic and subtopic and description):
            return jsonify({"error": "Required Fields not provided"}), 400

        response_body = quiz.get_quiz(course, topic, subtopic, description)
        return jsonify(response_body)

    except Exception as e:
        print(f"Error in /api/v1/quiz: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Route for Translation
@api.route("/api/v1/translate", methods=["POST"])
def get_translations():
    try:
        req = request.get_json()
        print("Received request for /api/v1/translate with data:", req)

        text = req.get("textArr")
        toLang = req.get("toLang")

        if not text or not toLang:
            return jsonify({"error": "Required Fields not provided"}), 400

        translated_text = translate.translate_text_arr(text_arr=text, target=toLang)
        return jsonify(translated_text)

    except Exception as e:
        print(f"Error in /api/v1/translate: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Route for Generative Learning Resources
@api.route("/api/v1/generate-resource", methods=["POST"])
def generative_resource():
    try:
        req = request.get_json()
        print("Received request for /api/v1/generate-resource with data:", req)

        required_fields = ["course", "knowledge_level", "description", "time"]
        req_data = {key: req.get(key) for key in required_fields}

        if not all(req_data.values()):
            return jsonify({"error": "Required Fields not provided"}), 400

        resources = generativeResources.generate_resources(**req_data)
        return jsonify(resources)

    except Exception as e:
        print(f"Error in /api/v1/generate-resource: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Run Flask App
if __name__ == "__main__":
    print("🚀 Starting Internal Flask Server...")
    api.run(debug=True, host="0.0.0.0", port=5003)
