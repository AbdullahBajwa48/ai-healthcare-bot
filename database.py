from auth import supabase

def get_user_sessions(user_id: str):
    """Get all previous chats for this user, newest first"""
    return supabase.table("chat_sessions")\
        .select("*")\
        .eq("user_id", user_id)\
        .order("created_at", desc=True)\
        .execute().data

def create_session(user_id: str, title: str):
    """Create a new chat session, title = first message truncated"""
    return supabase.table("chat_sessions")\
        .insert({"user_id": user_id, "title": title})\
        .execute().data[0]

def get_messages(session_id: str):
    """Load all messages for a specific chat session"""
    return supabase.table("messages")\
        .select("*")\
        .eq("session_id", session_id)\
        .order("created_at")\
        .execute().data

def save_message(session_id: str, role: str, content: str):
    """Save a single message to the database"""
    supabase.table("messages")\
        .insert({
            "session_id": session_id,
            "role": role,
            "content": content
        })\
        .execute()