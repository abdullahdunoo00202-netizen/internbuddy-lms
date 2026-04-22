from dotenv import load_dotenv
import os
from pymongo import MongoClient
from datetime import datetime, timedelta

# ===============================
# LOAD ENV
# ===============================
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file")

# ===============================
# CONNECT DB (FINAL FIX)
# ===============================
client = MongoClient(MONGO_URI)

# 🔥 CHANGE HERE → internbuddy
db = client["internbuddy"]

# ===============================
# CLEAR OLD TASKS (OPTIONAL)
# ===============================
db.lms_tasks.delete_many({})

# ===============================
# CREATE TASKS
# ===============================
tasks = []
start_date = datetime.now()

for i in range(5):
    tasks.append({
        "title": f"Project {i+1}",
        "description": f"Complete project {i+1}",
        "week": i + 1,
        "deadline": start_date + timedelta(days=(i+1)*18),
        "marks": 5
    })

# ===============================
# INSERT
# ===============================
db.lms_tasks.insert_many(tasks)

print("✅ 5 Tasks Inserted into INTERNBUDDY DB")