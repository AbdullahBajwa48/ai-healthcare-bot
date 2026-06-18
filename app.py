import streamlit as st
from bot import get_response
from auth import get_github_login_url, exchange_code_for_session, sign_out
from database import get_user_sessions, create_session, get_messages, save_message

st.set_page_config(page_title="Healthcare Bot", page_icon="💬")

# ── Step 1: initialize session state variables ──────────────────
if "user" not in st.session_state:
    st.session_state.user = None          # logged in user object

if "messages" not in st.session_state:
    st.session_state.messages = []        # current chat messages

if "session_id" not in st.session_state:
    st.session_state.session_id = None    # current chat session id

# ── Step 2: handle GitHub redirect ──────────────────────────────
# After GitHub login, Supabase redirects back with ?code=xxx in URL
# We detect it here and exchange it for a real user session
params = st.query_params

if "code" in params and st.session_state.user is None:
    user = exchange_code_for_session(params["code"])
    st.session_state.user = user
    st.query_params.clear()   # clean ?code from URL
    st.rerun()

# ── Step 3: if not logged in → show login page ──────────────────
# ── Step 3: if not logged in → show login page ──────────────────
if st.session_state.user is None:
    
    st.markdown("""
    <style>
    .login-card {
        max-width: 400px;
        margin: 4rem auto;
        padding: 2.5rem 2rem;
        border: 0.5px solid rgba(0,0,0,0.12);
        border-radius: 12px;
        background: #f0faf5
    }
    .login-title { font-size: 22px; font-weight: 500; margin-bottom: 0.4rem; }
    .login-sub { font-size: 14px; color: #666; margin-bottom: 2rem; }
    .disclaimer-box {
        background: #f5f5f5;
        border-radius: 8px;
        padding: 12px 14px;
        font-size: 12px;
        color: #666;
        margin-top: 1.5rem;
    }
    </style>
    <div class="login-card">
        <div style="font-size:2.5rem; margin-bottom:1rem">🩺</div>
        <div class="login-title">Healthcare Bot</div>
        <div class="login-sub">Sign in to save your chat history and access previous conversations.</div>
        <div class="disclaimer-box">
            ℹ️ This bot provides general health information only. 
            It does not diagnose conditions or replace professional medical advice.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Continue with GitHub 🐙", use_container_width=True):
            url = get_github_login_url()
            st.markdown(
                f'<meta http-equiv="refresh" content="0;url={url}">',
                unsafe_allow_html=True
            )
        st.caption("Secure login via GitHub OAuth")

    st.stop()

# ── Step 4: logged in → show chat page ──────────────────────────
user = st.session_state.user

# Sidebar — chat history + controls
with st.sidebar:
    st.write(f"Logged in as **{user.email}**")

    if st.button("Sign Out"):
        sign_out()
        st.session_state.user = None
        st.session_state.messages = []
        st.session_state.session_id = None
        st.rerun()

    st.divider()

    if st.button("+ New Chat"):
        st.session_state.messages = []
        st.session_state.session_id = None
        st.rerun()

    st.subheader("Previous Chats")
    # Load all past sessions for this user
    sessions = get_user_sessions(user.id)
    for s in sessions:
        if st.button(s["title"], key=s["id"]):
            # Load messages for selected session
            st.session_state.session_id = s["id"]
            history = get_messages(s["id"])
            # Convert DB rows to the format our bot expects
            st.session_state.messages = [
                {"role": m["role"], "content": m["content"]}
                for m in history
            ]
            st.rerun()

# Main chat area
st.title("💬 Healthcare Information Bot")

st.sidebar.info("""
This bot provides general health information only. 
Always consult a qualified doctor for personal medical advice.
""")

# Render existing messages
st.chat_message("assistant").markdown(
    "Hello! Ask me anything about health and wellness."
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Create a new DB session on first message
    if st.session_state.session_id is None:
        title = user_input[:50]   # first 50 chars become the chat title
        new_session = create_session(user.id, title)
        st.session_state.session_id = new_session["id"]

    # Save + display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    save_message(st.session_state.session_id, "user", user_input)

    with st.chat_message("user"):
        st.markdown(user_input)

    # Get + stream + save assistant response
    with st.chat_message("assistant"):
        response = st.write_stream(get_response(st.session_state.messages))

    st.session_state.messages.append({"role": "assistant", "content": response})
    save_message(st.session_state.session_id, "assistant", response)