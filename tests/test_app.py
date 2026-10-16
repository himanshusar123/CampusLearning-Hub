"""Basic tests for the CampusLearning Hub teaching API."""

import app as app_module


def setup_function():
    app_module.registrations.clear()
    app_module.config["registration_open"] = True
    app_module.config["maintenance_mode"] = False


def test_home_endpoint():
    client = app_module.app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.get_json()


def test_courses_endpoint():
    client = app_module.app.test_client()
    response = client.get("/courses")
    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_course_not_found():
    client = app_module.app.test_client()
    response = client.get("/courses/999")
    assert response.status_code == 404


def test_valid_registration():
    client = app_module.app.test_client()
    response = client.post(
        "/register",
        json={
            "student_id": 101,
            "name": "Aarav Sharma",
            "email": "aarav@example.com",
            "age": 20,
            "course": "Python",
        },
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "Registration successful"


def test_invalid_age_is_rejected():
    client = app_module.app.test_client()
    response = client.post(
        "/register",
        json={
            "student_id": 102,
            "name": "Meera Singh",
            "email": "meera@example.com",
            "age": 12,
            "course": "Python",
        },
    )
    assert response.status_code == 400


def test_unknown_course_is_rejected():
    client = app_module.app.test_client()
    response = client.post(
        "/register",
        json={
            "student_id": 103,
            "name": "Rohan Kumar",
            "email": "rohan@example.com",
            "age": 21,
            "course": "Astronomy",
        },
    )
    assert response.status_code == 400


def test_duplicate_student_id_is_rejected():
    client = app_module.app.test_client()
    payload = {
        "student_id": 104,
        "name": "Nisha Rao",
        "email": "nisha@example.com",
        "age": 22,
        "course": "Data Science",
    }
    first = client.post("/register", json=payload)
    second = client.post("/register", json=payload)
    assert first.status_code == 201
    assert second.status_code == 409


def test_closed_registration_returns_503():
    app_module.config["registration_open"] = False
    client = app_module.app.test_client()
    response = client.post(
        "/register",
        json={
            "student_id": 105,
            "name": "Kabir Verma",
            "email": "kabir@example.com",
            "age": 20,
            "course": "Python",
        },
    )
    assert response.status_code == 503
