"""CampusLearning Hub: teaching example REST API.

Run locally with:
    python app.py

This example keeps registrations in memory. It is intended for learning,
not production deployment.
"""

import json
import logging
from pathlib import Path

from flask import Flask, jsonify, request
from pydantic import ValidationError

from student_model import Student

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"


def load_config() -> dict:
    """Load and validate the presence of the JSON configuration file."""
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as file:
            config = json.load(file)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Configuration file not found: {CONFIG_PATH}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("config.json contains invalid JSON.") from exc

    required_keys = {
        "college_name",
        "max_students_per_course",
        "registration_open",
        "maintenance_mode",
    }
    missing = required_keys - config.keys()
    if missing:
        raise RuntimeError(
            f"config.json is missing required setting(s): {', '.join(sorted(missing))}"
        )
    return config


config = load_config()

courses = [
    {"course_id": 1, "name": "Python", "seats": 20},
    {"course_id": 2, "name": "Data Science", "seats": 15},
    {"course_id": 3, "name": "Cloud Computing", "seats": 10},
]

# In-memory only: registrations disappear when the server restarts.
registrations: list[dict] = []


@app.get("/")
def home():
    """Show API welcome information and registration status."""
    return jsonify(
        {
            "message": f"Welcome to {config['college_name']} API",
            "registration_open": config["registration_open"],
            "maintenance_mode": config["maintenance_mode"],
        }
    ), 200


@app.get("/health")
def health():
    """Basic health endpoint for local testing."""
    return jsonify({"status": "ok"}), 200


@app.get("/courses")
def get_courses():
    """Return all available courses."""
    return jsonify(courses), 200


@app.get("/courses/<int:course_id>")
def get_course(course_id: int):
    """Return one course by ID, or 404 if it does not exist."""
    course = next(
        (item for item in courses if item["course_id"] == course_id),
        None,
    )
    if course is None:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course), 200


@app.get("/college-info")
def college_info():
    """Return basic college information from configuration."""
    return jsonify(
        {
            "college_name": config["college_name"],
            "registration_open": config["registration_open"],
            "maintenance_mode": config["maintenance_mode"],
            "max_students_per_course": config["max_students_per_course"],
        }
    ), 200


@app.get("/registrations")
def get_registrations():
    """List registrations created during this running process.

    For teaching purposes only. A real system must protect student data.
    """
    return jsonify(registrations), 200


@app.post("/register")
def register_student():
    """Validate and accept one registration."""
    if not config["registration_open"] or config["maintenance_mode"]:
        return jsonify(
            {"error": "Registration is currently unavailable"}
        ), 503

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(
            {"error": "Please submit a valid JSON object"}
        ), 400

    try:
        student = Student(**data)
    except ValidationError as exc:
        return jsonify(
            {
                "error": "Invalid student details",
                "details": exc.errors(
                    include_input=False,
                    include_url=False,
                ),
            }
        ), 400

    known_course_names = {course["name"].casefold() for course in courses}
    if student.course.casefold() not in known_course_names:
        return jsonify(
            {
                "error": "Unknown course",
                "available_courses": [course["name"] for course in courses],
            }
        ), 400

    if any(
        item["student_id"] == student.student_id for item in registrations
    ):
        return jsonify(
            {"error": "A registration with this student_id already exists"}
        ), 409

    registrations.append(student.model_dump())
    logging.info("Registration accepted for student ID %s", student.student_id)

    return jsonify(
        {
            "message": "Registration successful",
            "student": student.model_dump(),
        }
    ), 201


if __name__ == "__main__":
    # Debug mode is appropriate only for local learning.
    app.run(host="127.0.0.1", port=5000, debug=True)
