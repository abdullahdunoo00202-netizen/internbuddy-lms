from flask import Blueprint, render_template, request, session, redirect, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from utils.supabase_client import supabase
import os
import uuid

load_dotenv()

lms = Blueprint("lms", __name__)

# SAME DB (IMPORTANT)
client = MongoClient(os.getenv("MONGO_URI"))
db = client["internbuddy"]

# LOGIN PAGE
@lms.route("/")
def lms_login_page():
    return render_template("lms_login.html")

@lms.route("/dashboard")
def dashboard():
    if "student_email" not in session:
        return redirect("/lms")

    # ✅ GET STUDENT
    student = db.offers.find_one({
        "lms_email": session["student_email"]
    })

    if not student:
        session.clear()
        return redirect("/lms")

    # ✅ GET TASKS
    tasks = list(db.lms_tasks.find())

    # ✅ GET SUBMISSIONS
    submissions = list(db.lms_submissions.find({
        "student_id": str(student["_id"])
    }))

    # ✅ SUBMITTED TASK IDS
    submitted_task_ids = [str(s["task_id"]) for s in submissions]

    # ✅ MARKS CALCULATION
    obtained_marks = sum([s.get("marks", 0) for s in submissions])
    total_marks = len(tasks) * 5

    progress = int((obtained_marks / total_marks) * 100) if total_marks else 0
    all_completed = len(submissions) == len(tasks)

    # ✅ RETURN TEMPLATE (THIS WAS MISSING 🔥)
    return render_template(
        "lms_dashboard.html",
        student=student,
        tasks=tasks,
        submitted_task_ids=submitted_task_ids,
        obtained_marks=obtained_marks,
        total_marks=total_marks,
        progress=progress,
        all_completed=all_completed
    )


@lms.route("/certificate")
def certificate():
    if "student_email" not in session:
        return redirect("/lms")

    student = db.offers.find_one({
        "lms_email": session["student_email"]
    })

    return render_template("certificate.html", student=student)

# LOGOUT
@lms.route("/logout")
def logout():
    session.clear()
    return redirect("/lms")

# SUBMIT TASK
from datetime import datetime

from datetime import datetime

@lms.route("/submit-task", methods=["POST"])
def submit_task():
    if "student_email" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    file = request.files.get("file")
    task_id = request.form.get("task_id")

    if not file or not task_id:
        return jsonify({"error": "Missing data"}), 400

    # ✅ GET STUDENT
    student = db.offers.find_one({
        "lms_email": session["student_email"]
    })

    if not student:
        return jsonify({"error": "User not found"}), 404

    # ✅ PREVENT DUPLICATE SUBMISSION
    existing = db.lms_submissions.find_one({
        "student_id": str(student["_id"]),
        "task_id": task_id
    })

    if existing:
        return jsonify({"error": "Already submitted"}), 400

    try:
        # ✅ UNIQUE FILE NAME
        file_name = f"{uuid.uuid4()}_{file.filename}"

        # ✅ CONVERT FILE → BYTES
        file_bytes = file.read()

        # ✅ UPLOAD TO SUPABASE (USE CORRECT BUCKET NAME)
        supabase.storage.from_("task").upload(
            path=file_name,
            file=file_bytes
        )

        # ✅ GET PUBLIC URL
        file_url = supabase.storage.from_("task").get_public_url(file_name)

        # ✅ SAVE IN DB
        db.lms_submissions.insert_one({
            "student_id": str(student["_id"]),
            "task_id": task_id,
            "file_url": file_url,
            "marks": 5,
            "submitted_at": datetime.utcnow()
        })

        return jsonify({"message": "Submitted successfully"})

    except Exception as e:
        print("UPLOAD ERROR:", e)
        return jsonify({"error": "Upload failed"}), 500