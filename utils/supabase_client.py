from supabase import create_client
from dotenv import load_dotenv
import os

# ===============================
# LOAD ENV
# ===============================
load_dotenv()

# ===============================
# GET ENV VARIABLES
# ===============================
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")   # ✅ FIXED (important)

# ===============================
# DEBUG (remove later)
# ===============================
print("SUPABASE URL:", url)
print("SUPABASE KEY:", key)

# ===============================
# VALIDATION
# ===============================
if not url:
    raise ValueError("❌ SUPABASE_URL missing in .env")

if not key:
    raise ValueError("❌ SUPABASE_SERVICE_KEY missing in .env")

# ===============================
# CREATE CLIENT
# ===============================
supabase = create_client(url, key)