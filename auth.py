from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

def get_github_login_url() -> str:
    """Ask Supabase to give us the GitHub OAuth URL to redirect user to"""
    data = supabase.auth.sign_in_with_oauth({
        "provider": "github",
        "options": {
            "redirect_to": "http://localhost:8501"
        }
    })
    return data.url

def exchange_code_for_session(code: str):
    """When GitHub redirects back with ?code=xxx, exchange it for a real session"""
    session = supabase.auth.exchange_code_for_session({"auth_code": code})
    return session.user

def sign_out():
    supabase.auth.sign_out()