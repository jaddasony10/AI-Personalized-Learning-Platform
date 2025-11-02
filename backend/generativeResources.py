"""
Install the Google AI Python SDK

$ pip install google-generativeai python-dotenv

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def setup_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY environment variable is not set. Please set it using the following command:\n"
            "export GEMINI_API_KEY='AIzaSyB-p9BkM7oLfm2HI_Q8dd8zpUI8SdrHPxM'\n"
            "You can add this line to your shell profile (e.g., ~/.bashrc or ~/.zshrc) to set it permanently."
        )
    return api_key

api_key = setup_api_key()
genai.configure(api_key=api_key)


def generate_resources(course, knowledge_level, description, time):
    # Create the model
    # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        # safety_settings = Adjust safety settings
        # See https://ai.google.dev/gemini-api/docs/safety-settings
        system_instruction="You are an AI tutor. Maintain a modest and calm language suitable for learning. You need to provide content to user to learn in given time.",
    )

    chat_session = model.start_chat(history=[])

    response = chat_session.send_message(
        f"I am learning {course}. My knowledge level in this topic is {knowledge_level}. i want to {description}. I want to learn it in {time}. Teach me.",
        stream=False,
    )

    print(response.text)
    return response.text
