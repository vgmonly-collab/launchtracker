# lib/auth.py
import streamlit as st
import streamlit_authenticator as stauth
from typing import Tuple

class Auth:
    def __init__(self):
        conf = st.secrets.get("auth", {})
        names, usernames, passwords, roles = [], [], [], []
        for u, blob in st.secrets.get("users", {}).items():
            name, role, hashed = blob.split(",", 2)
            names.append(name)
            usernames.append(u)
            passwords.append(hashed)
            roles.append(role)
        self.roles = dict(zip(usernames, roles))
        self.authenticator = stauth.Authenticate(
            dict(zip(usernames, names)),
            dict(zip(usernames, passwords)),
            conf.get("cookie_name"),
            conf.get("cookie_key"),
            conf.get("cookie_expiry_days", 30),
        )

    def login(self) -> Tuple[str,str]:
        name, auth_status, username = self.authenticator.login("Login", "main")
        if auth_status:
            st.session_state["role"] = self.roles.get(username, "viewer")
            st.session_state["username"] = username
            return username, self.roles.get(username, "viewer")
        elif auth_status is False:
            st.error("Username/password incorrect")
        return "","viewer"

    def logout(self):
        self.authenticator.logout("Logout", "sidebar")
