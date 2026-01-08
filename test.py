import streamlit as st
import streamlit_authenticator as stauth

st.title("Test Login App")

# 🔑 Setup für Google OAuth
credentials = {
    "client_id": "REMOVED",
    "client_secret": "REMOVED",
    "redirect_uri": "https://pqw8l7hrekvttzngm8fz8k.streamlit.app"
}

# Authenticator initialisieren
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="login_cookie",
    key="some_random_key"
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