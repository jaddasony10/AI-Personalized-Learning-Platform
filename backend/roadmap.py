import google.generativeai as genai
import os
import json

# Load .env automatically if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Set up Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_KEY = GEMINI_API_KEY.strip().strip('"\'')
if not GEMINI_API_KEY:
    raise ValueError("Gemini API Key is not set! Set GEMINI_API_KEY in your environment or in a .env file.")

genai.configure(api_key=GEMINI_API_KEY)

# move/keep fallback generator at module level so it can be reused
def generate_local_roadmap(topic, time_weeks, knowledge_level):
    """
    Build a deterministic week-by-week roadmap tailored to the topic.
    """
    # normalize weeks
    weeks = 0
    try:
        weeks = int(str(time_weeks).strip().split()[0])
    except Exception:
        import re
        m = re.search(r"\d+", str(time_weeks))
        if m:
            weeks = int(m.group())
    if weeks <= 0:
        weeks = 8

    # determine category from topic string
    t = (topic or "").lower()
    def contains(*keys):
        return any(k in t for k in keys)

    if contains("python"):
        focuses = [
            "Python Syntax & Basics",
            "Data Structures & Collections",
            "Functions & Modules",
            "File I/O & Error Handling",
            "Virtual Environments & Packaging",
            "Working with Libraries (requests, BeautifulSoup)",
            "Data Manipulation with pandas",
            "Testing & Debugging",
            "Object-Oriented Programming",
            "Asynchronous Programming",
            "Web Basics with Flask",
            "APIs & Data Serialization",
            "Performance & Profiling",
            "Deployment to Heroku / Vercel",
            "Capstone: Small Python Project"
        ]
        yt = "https://www.youtube.com/watch?v=rfscVS0vtbw"  # freeCodeCamp Python for Beginners
        web = "https://docs.python.org/3/"
    elif contains("java"):
        focuses = [
            "Java Syntax & Tooling",
            "Primitive Types & Operators",
            "Control Flow & Collections",
            "OOP: Classes & Inheritance",
            "Exception Handling & I/O",
            "Generics & Collections Framework",
            "Concurrency Basics",
            "Building with Maven/Gradle",
            "Unit Testing with JUnit",
            "Spring Boot Introduction",
            "REST APIs with Spring",
            "Persistence with JPA/Hibernate",
            "Deployment & Packaging",
            "Performance Tuning",
            "Capstone: Java Application"
        ]
        yt = "https://www.youtube.com/watch?v=grEKMHGYyns"  # Java Tutorial - Java Brains / core tutorial
        web = "https://docs.oracle.com/javase/tutorial/"
    elif contains("machine", "ml", "deep", "ai", "artificial"):
        focuses = [
            "Math Foundations (Linear Algebra, Probability)",
            "Python for ML & Tooling (numpy/pandas)",
            "Data Cleaning & Visualization",
            "Supervised Learning Basics",
            "Regression & Classification",
            "Model Evaluation & Validation",
            "Unsupervised Learning & Clustering",
            "Neural Network Basics",
            "Deep Learning with TensorFlow/PyTorch",
            "CNNs & RNNs Overview",
            "Model Deployment Basics",
            "Transfer Learning & Pretrained Models",
            "Interpretability & Ethics",
            "Project: End-to-end ML Pipeline",
            "Revision & Interview Prep"
        ]
        yt = "https://www.youtube.com/watch?v=aircAruvnKk"  # ML Crash Course style
        web = "https://www.coursera.org/learn/machine-learning"  # high-level course
    elif contains("web", "frontend", "react", "javascript", "html", "css"):
        focuses = [
            "Web Fundamentals (HTML/CSS)",
            "JavaScript Basics & DOM",
            "Modern JavaScript (ES6+)",
            "Responsive Design & CSS Tools",
            "Version Control & Tooling",
            "Frontend Framework Intro (React/Vue)",
            "State Management & Routing",
            "Styling Systems & Component Libraries",
            "APIs & Fetching Data",
            "Testing & Accessibility",
            "Build & Deployment",
            "Performance Optimization",
            "Progressive Web Apps & Offline",
            "Security Basics",
            "Capstone: Small Web App"
        ]
        yt = "https://www.youtube.com/watch?v=4UZrsTqkcW4"  # Traversy - Modern JS/React crash
        web = "https://developer.mozilla.org/en-US/docs/Web"
    elif contains("data", "data science", "pandas", "sql"):
        focuses = [
            "SQL & Relational Databases",
            "Data Cleaning with pandas",
            "Exploratory Data Analysis",
            "Data Visualization (matplotlib/seaborn)",
            "Statistics for Data Science",
            "Feature Engineering",
            "Supervised Learning Overview",
            "Model Validation & Selection",
            "Unsupervised Techniques",
            "Time Series Basics",
            "Putting Models into Production",
            "Big Data Tools Overview",
            "Model Monitoring & Ethics",
            "Capstone: Data Analysis Project",
            "Presentation & Storytelling"
        ]
        yt = "https://www.youtube.com/watch?v=6cFfFh2F2mk"  # data tutorials
        web = "https://pandas.pydata.org/"
    elif contains("devops", "docker", "kubernetes", "ci/cd"):
        focuses = [
            "Linux & Shell Basics",
            "Version Control & Git Workflows",
            "CI/CD Concepts",
            "Containers with Docker",
            "Docker Compose & Images",
            "Introduction to Kubernetes",
            "Configuration & Secrets Management",
            "Observability & Logging",
            "Infrastructure as Code (Terraform)",
            "Cloud Fundamentals (AWS/GCP/Azure)",
            "Deployment Strategies",
            "Security & Hardening",
            "Scaling & Load Balancing",
            "Monitoring & Alerts",
            "Capstone: Deploy an App"
        ]
        yt = "https://www.youtube.com/watch?v=pTFZFxd4hOI"  # Docker tutorial
        web = "https://kubernetes.io/docs/home/"
    else:
        # generic fallback focuses tuned by topic name
        focuses = [
            f"Foundations of {topic}",
            f"{topic} Tooling & Setup",
            f"Core Concepts of {topic}",
            f"Practical Tutorials for {topic}",
            f"Intermediate {topic} Techniques",
            f"Advanced {topic} Topics",
            f"Testing & Best Practices",
            f"Project Work on {topic}",
            f"Optimization & Performance",
            f"Deployment & Real-world Use",
            f"Security & Ethics in {topic}",
            f"Revision & Further Reading",
            f"Capstone Project Planning",
            "Revision & Interview Prep",
            "Final Project"
        ]
        yt = "https://www.youtube.com/@freecodecamp"
        web = "https://en.wikipedia.org/wiki/" + topic.replace(" ", "_")

    steps = []
    for i in range(1, weeks + 1):
        focus = focuses[(i - 1) % len(focuses)]
        points = [
            f"Understand core concepts for: {focus}.",
            "Follow a short hands-on tutorial to apply the concepts.",
            "Complete a small exercise or notebook related to this week's focus.",
            "Review key terminology and take notes for retention."
        ]
        # add a project consolidation every 4th week
        if i % 4 == 0:
            points.append("Work on a small project or notebook to consolidate learning.")

        # choose resources tailored to category
        resources = [
            {"type": "YouTube", "link": yt},
            {"type": "Website", "link": web}
        ]

        step = {
            "duration": "1 week",
            "title": f"Week {i}: {focus}",
            "description": f"Week {i} plan focused on {focus}. Follow the points to progress.",
            "points": points,
            "resources": resources
        }
        steps.append(step)

    return {
        "knowledge_level": knowledge_level,
        "topic": topic,
        "time": f"{weeks} weeks",
        "steps": steps
    }

def generate_learning_path(topic, time, knowledge_level):
    """
    Generates a personalized learning roadmap using Gemini API.
    """
    prompt = f"""
    You are an AI that generates a structured, in-depth learning roadmap for "{topic}" based on a learning duration of {time} weeks.
    The user's knowledge level is "{knowledge_level}". 
    Provide a step-by-step roadmap with detailed descriptions, useful online resources, and **real working YouTube links**.

    Structure the response in JSON format:
    {{
      "knowledge_level": "{knowledge_level}",
      "topic": "{topic}",
      "time": "{time} weeks",
      "steps": [
        {{
          "duration": "<number of weeks>",
          "title": "<Step title>",
          "description": "<Detailed explanation>",
          "resources": [
            {{
              "type": "YouTube",
              "link": "<Working YouTube link>"
            }},
            {{
              "type": "Website",
              "link": "<High-quality learning resource>"
            }}
          ]
        }},
        ...
      ]
    }}

    Example:
    - If the topic is "Python for Beginners," include structured steps like:
      1. Introduction to Python (Week 1) - Learn syntax, variables, and data types.
      2. Control Structures (Week 2) - Master loops and conditionals.
      3. Functions and Modules (Week 3) - Learn how to write reusable code.
      4. Advanced Python Concepts (Week 4) - Explore OOP, file handling, and debugging.

    Each step **must** include:
    - A short but **clear title**.
    - A **detailed description** covering key learning objectives.
    - A duration in **weeks**.
    - At least **one working YouTube link** (from reputable sources like Traversy Media, freeCodeCamp, etc.).
    - A **website or article** to reinforce learning.

    Make sure **YouTube links are real and relevant**. Avoid placeholder links.
    """

    # helper to try common invocation shapes
    def _try_invoke(fn, prompt_text):
        if not callable(fn):
            return None
        shapes = [
            {"prompt": prompt_text},
            {"input": prompt_text},
            {"text": prompt_text},
            {"messages": [{"content": prompt_text}]},
            (prompt_text,),
        ]
        for s in shapes:
            try:
                if isinstance(s, dict):
                    return fn(**s)
                else:
                    return fn(*s)
            except TypeError:
                # signature mismatch — try next
                continue
        return None

    # search given object for candidate callables and attempt invocation
    def _search_and_call(obj, prompt_text):
        if obj is None:
            return None
        # direct callable
        if callable(obj):
            try:
                res = _try_invoke(obj, prompt_text)
                if res is not None:
                    return res
            except Exception:
                raise
        # inspect members for likely generation methods
        for name in dir(obj):
            if name.startswith("_"):
                continue
            lname = name.lower()
            if any(k in lname for k in ("generate", "create", "call", "respond", "predict", "complete", "chat")):
                fn = getattr(obj, name, None)
                if fn and callable(fn):
                    try:
                        res = _try_invoke(fn, prompt_text)
                        if res is not None:
                            return res
                    except Exception:
                        # propagate non-TypeErrors so caller can see meaningful exceptions
                        raise
        return None

    def _call_genai(prompt_text):
        # 1) top-level generate_text if present
        if hasattr(genai, "generate_text") and callable(genai.generate_text):
            return genai.generate_text(model="text-bison-001", prompt=prompt_text)

        # 2) try genai.get_model / get_base_model
        for getter_name in ("get_model", "get_base_model", "getModel"):
            getter = getattr(genai, getter_name, None)
            if callable(getter):
                for model_name in ("text-bison-001", "models/text-bison-001", "text-bison"):
                    try:
                        model_obj = getter(model_name)
                    except Exception:
                        continue
                    # try on returned model object
                    called = _search_and_call(model_obj, prompt_text)
                    if called is not None:
                        return called
                    # also try calling the model object itself if callable
                    if callable(model_obj):
                        called = _try_invoke(model_obj, prompt_text)
                        if called is not None:
                            return called

        # 3) try genai.responder or similar top-level helpers
        for candidate_name in ("responder", "respond", "response", "generative", "GenerativeModel"):
            candidate = getattr(genai, candidate_name, None)
            called = _search_and_call(candidate, prompt_text)
            if called is not None:
                return called

        # 4) client-style API
        Client = getattr(genai, "Client", None)
        if Client:
            try:
                client = Client()
                called = _search_and_call(client, prompt_text)
                if called is not None:
                    return called
            except Exception:
                pass

        # 5) REST fallback: call Generative Language REST endpoint directly using API key
        try:
            import requests
            # Use v1beta2 generate endpoint for the text-bison model
            url = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generate"
            params = {"key": GEMINI_API_KEY}
            body = {"prompt": {"text": prompt_text}}
            headers = {"Content-Type": "application/json"}
            resp = requests.post(url, params=params, json=body, headers=headers, timeout=30)
            # If successful, return parsed JSON so downstream extraction logic can find 'candidates'
            if resp.ok:
                return resp.json()
            # include status text for easier debugging
            return {"error": "REST request failed", "status_code": resp.status_code, "text": resp.text}
        except Exception as e:
            # ignore here and raise an informative AttributeError below
            rest_err = str(e)

        # no entrypoint found — raise informative error
        available = ", ".join(sorted([a for a in dir(genai) if not a.startswith("_")]))
        raise AttributeError(
            "No supported generate_text entrypoint found on google.generativeai. "
            "Available attributes: " + available + f". REST fallback error: {locals().get('rest_err', '')}"
        )

    def _extract_json_from_string(s: str):
        # Try to locate a valid JSON object substring inside s by trying
        # different { ... } spans. Return parsed JSON or None.
        if not isinstance(s, str):
            return None
        start_indices = [i for i, ch in enumerate(s) if ch == "{"] 
        end_indices = [i for i, ch in enumerate(s) if ch == "}"]
        # Try plausible spans (start from earliest '{' and try later '}' positions)
        for i in start_indices:
            for j in reversed(end_indices):
                if j <= i:
                    continue
                sub = s[i : j + 1]
                try:
                    return json.loads(sub)
                except Exception:
                    continue
        # final attempt: whole string
        try:
            return json.loads(s)
        except Exception:
            return None

    def _find_json_in_obj(obj):
        # Recursively search dicts, lists and strings for JSON content
        if obj is None:
            return None
        if isinstance(obj, str):
            return _extract_json_from_string(obj)
        if isinstance(obj, dict):
            # if dict already looks like roadmap, return it
            if {"knowledge_level", "topic", "time", "steps"}.issubset(set(obj.keys())):
                return obj
            for v in obj.values():
                found = _find_json_in_obj(v)
                if found is not None:
                    return found
        if isinstance(obj, list):
            for item in obj:
                found = _find_json_in_obj(item)
                if found is not None:
                    return found
        # fallback
        return None

    def _is_placeholder_roadmap(obj):
        """
        Return True if obj looks like a placeholder roadmap produced by the prompt template
        (contains tags like <Step title> or <Working YouTube link>).
        """
        if not isinstance(obj, dict):
            return False
        steps = obj.get("steps")
        if not isinstance(steps, list) or not steps:
            return False
        for s in steps:
            if not isinstance(s, dict):
                continue
            title = s.get("title", "")
            duration = s.get("duration", "")
            resources = s.get("resources", [])
            if any(tag in title for tag in ("<Step title>", "<Step")):
                return True
            if "<number of weeks>" in str(duration):
                return True
            for r in resources:
                if isinstance(r, dict) and "<Working YouTube link>" in str(r.get("link", "")):
                    return True
        return False

    try:
        response = _call_genai(prompt)

        # Ensure response is JSON formatted
        if not response:
            # fallback to module-level local generator
            return generate_local_roadmap(topic, time, knowledge_level)

        # genai response shapes may vary; check possible attributes
        text_output = None
        # Newer SDKs place candidates as a list-like object with 'output' string
        try:
            if hasattr(response, 'candidates') and response.candidates:
                first = response.candidates[0]
                if isinstance(first, dict):
                    text_output = first.get("output") or first.get("content") or first.get("text")
                else:
                    text_output = getattr(first, "output", None) or getattr(first, "content", None) or getattr(first, "text", None)
        except Exception:
            text_output = None

        # Fallback: some SDKs set 'content' or 'text' or return dicts
        if not text_output:
            if hasattr(response, 'content'):
                text_output = response.content
            elif hasattr(response, 'text'):
                text_output = response.text
            elif isinstance(response, dict):
                text_output = response.get("output") or response.get("text") or response.get("content") or response.get("response")

        # If we still don't have a string, try to find JSON anywhere inside the response object
        if not text_output:
            found_json = _find_json_in_obj(response)
            if found_json is not None:
                # if the found JSON is placeholder-like, use local fallback
                if _is_placeholder_roadmap(found_json):
                    return generate_local_roadmap(topic, time, knowledge_level)
                return found_json

        # If text_output is a dict-like or contains JSON, try to parse directly
        if isinstance(text_output, (dict, list)):
            # Already structured; check placeholders
            if isinstance(text_output, dict) and _is_placeholder_roadmap(text_output):
                return generate_local_roadmap(topic, time, knowledge_level)
            return text_output

        if not text_output:
            # If the SDK simply echoed the prompt (common when wrong method used), include it for debugging
            if isinstance(response, dict) and "prompt" in response:
                return {"error": "API returned structure without generated text; echoed prompt included", "prompt": response.get("prompt")}
            # fallback to module-level local generator
            return generate_local_roadmap(topic, time, knowledge_level)

        try:
            roadmap_json = json.loads(text_output)
            # if parsed JSON contains placeholders, switch to local generator
            if _is_placeholder_roadmap(roadmap_json):
                return generate_local_roadmap(topic, time, knowledge_level)
            # if parsed JSON missing steps or empty steps -> fallback
            if not isinstance(roadmap_json, dict) or not roadmap_json.get("steps"):
                return generate_local_roadmap(topic, time, knowledge_level)
            return roadmap_json
        except json.JSONDecodeError as jde:
            # As a last attempt, search inside the string for embedded JSON
            found_json = _extract_json_from_string(text_output)
            if found_json is not None:
                if _is_placeholder_roadmap(found_json):
                    return generate_local_roadmap(topic, time, knowledge_level)
                if not isinstance(found_json, dict) or not found_json.get("steps"):
                    return generate_local_roadmap(topic, time, knowledge_level)
                return found_json
            # Fallback to local roadmap instead of failing
            return generate_local_roadmap(topic, time, knowledge_level)

    except Exception as e:
        # Provide more context for unexpected errors, but return a usable local roadmap
        try:
            return generate_local_roadmap(topic, time, knowledge_level)
        except Exception:
            return {"error": "Failed to generate roadmap", "exception": str(e)}

# Compatibility wrapper used by base.py
def create_roadmap(topic, time, knowledge_level):
    # prefer AI-generated result but ensure we always return valid steps
    result = generate_learning_path(topic, time, knowledge_level)
    if not isinstance(result, dict):
        return generate_local_roadmap(topic, time, knowledge_level)
    if result.get("error") or not result.get("steps"):
        return generate_local_roadmap(topic, time, knowledge_level)
    return result