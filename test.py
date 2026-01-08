import streamlit as st
import streamlit_authenticator as stauth
from dotenv import load_dotenv
import os

st.title("Test Login App")

# 🔑 Lokal: .env laden (nur für lokale Tests)
load_dotenv()

# 🔑 Credentials aus st.secrets oder .env holen
credentials = {
    "client_id": st.secrets.get("GOOGLE_CLIENT_ID") or os.getenv("GOOGLE_CLIENT_ID"),
    "client_secret": st.secrets.get("GOOGLE_CLIENT_SECRET") or os.getenv("GOOGLE_CLIENT_SECRET"),
    "redirect_uri": st.secrets.get("GOOGLE_REDIRECT_URI") or os.getenv("GOOGLE_REDIRECT_URI")
}

# Authenticator initialisieren
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="login_cookie",
    key=st.secrets.get("COOKIE_KEY") or os.getenv("COOKIE_KEY")
)

# Login Button
name, user_email, auth_status = authenticator.login('Login', 'main')

if auth_status:
    st.success(f"Erfolgreich eingeloggt als {user_email}")
    st.session_state['user_id'] = user_email  # persistente ID für diese Session
elif auth_status == False:
    st.error("Login fehlgeschlagen")
else:
    st.warning("Bitte einloggen")