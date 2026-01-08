import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

st.title("Test Login App")

# 🔑 Secrets aus st.secrets oder lokal .env
CLIENT_ID = st.secrets.get("GOOGLE_CLIENT_ID") or os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = st.secrets.get("GOOGLE_CLIENT_SECRET") or os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = st.secrets.get("GOOGLE_REDIRECT_URI") or os.getenv("GOOGLE_REDIRECT_URI")

# 🔑 OAuth Flow einrichten
flow = Flow.from_client_config(
    {
        "web": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uris": [REDIRECT_URI],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    },
    scopes=["openid", "email", "profile"]
)

# 🔹 Wenn noch kein Code aus Google in URL, zeige Login-Link
if "code" not in st.experimental_get_query_params():
    auth_url, _ = flow.authorization_url(prompt="consent")
    st.markdown(f"[Login mit Google]({auth_url})")
else:
    # 🔹 Code aus URL holen
    code = st.experimental_get_query_params()["code"][0]
    flow.fetch_token(code=code)
    creds = flow.credentials

    # 🔹 Userinfo abrufen
    service = build("oauth2", "v2", credentials=creds)
    user_info = service.userinfo().get().execute()

    st.success(f"Erfolgreich eingeloggt als {user_info['email']}")
    st.session_state["user_id"] = user_info["email"]