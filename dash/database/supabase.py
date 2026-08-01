import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
TOKEN = os.getenv("BOT_TOKEN")

supabase: Client = create_client(url, key)