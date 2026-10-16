# CampusLearning Hub — Day 11 Hands-on

A beginner-friendly Flask REST API for a college course-registration scenario. This project demonstrates JSON configuration, Pydantic validation, logging, exception handling, and REST endpoints.

## Features

- Reads settings from `config.json`.
- Validates student registration data with Pydantic.
- Lists all courses and retrieves a course by ID.
- Accepts student registrations through a POST endpoint.
- Rejects invalid student details, unknown course names, and duplicate student IDs.
- Uses basic logging and clear HTTP status codes.

> **Learning project only:** registrations are stored in memory and disappear when the app stops. This app has no authentication, authorization, persistent database, or production hardening. Do not put real student information into it.

## 1. Requirements

- Python 3.10 or later
- Terminal / command prompt
- Postman or another HTTP client for POST requests (optional)

## 2. Set up

Open a terminal in this repository directory.

### Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install libraries:

```bash
python -m pip install -r requirements.txt
```

## 3. Run the API

```bash
python app.py
```

The API runs at `http://127.0.0.1:5000`. Keep the terminal open while testing.

## 4. Try the endpoints

| Method | URL | What it does |
|---|---|---|
| GET | `/` | Welcome message and registration status |
| GET | `/health` | Simple health check |
| GET | `/courses` | List all courses |
| GET | `/courses/1` | Retrieve a course by ID |
| GET | `/college-info` | Show settings from config.json |
| GET | `/registrations` | List registrations for this running process |
| POST | `/register` | Validate and accept a student registration |

Try GET endpoints in your browser. To test POST, open Postman and set:
- Method: `POST`
- URL: `http://127.0.0.1:5000/register`
- Body: **raw** → **JSON**

Valid example:

```json
{
  "student_id": 101,
  "name": "Aarav Sharma",
  "email": "aarav@example.com",
  "age": 20,
  "course": "Python"
}
```

Expected status: `201 Created`.

Invalid age example (should return `400 Bad Request`):

```json
{
  "student_id": 102,
  "name": "Meera Singh",
  "email": "meera@example.com",
  "age": 12,
  "course": "Python"
}
```

A duplicate `student_id` returns `409 Conflict`. An unknown course returns `400 Bad Request`. If registration is closed or maintenance mode is enabled, POST returns `503 Service Unavailable`.

## 5. Configuration exercise

Edit `config.json`:

- Set `registration_open` to `false` to stop new registrations.
- Set `maintenance_mode` to `true` to simulate maintenance.
- Change `college_name` and inspect `/` or `/college-info`.

Restart the Flask process after changing configuration because settings are loaded when the app starts.

## 6. Run tests

```bash
python -m pytest
```

## Concepts covered

- **JSON configuration:** settings separate from Python logic.
- **Pydantic:** validates types and constraints.
- **Exception handling:** reports config-loading problems clearly.
- **Logging:** records accepted registrations without logging email addresses.
- **REST:** HTTP routes expose JSON data to other applications.
- **Status codes:** 200 success, 201 created, 400 invalid input, 404 not found, 409 conflict, and 503 temporarily unavailable.
