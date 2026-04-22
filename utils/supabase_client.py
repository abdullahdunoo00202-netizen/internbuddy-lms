from supabase import create_client
import os

# ===============================
# GET ENV VARIABLES (RENDER SAFE)
# ===============================
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# ===============================
# SAFE INIT (NO CRASH)
# ===============================
supabase = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase Connected")
    except Exception as e:
        print("❌ Supabase init error:", e)
else:
    print("⚠️ Supabase ENV missing (App will still run)")
