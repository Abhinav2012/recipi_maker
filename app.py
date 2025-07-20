import streamlit as st
import pandas as pd
import os

PROFILE_FILE = "personal_profile/personal_info.csv"

# --- Load/save user profiles ---
def load_profiles():
    if os.path.exists(PROFILE_FILE):
        return pd.read_csv(PROFILE_FILE)
    return pd.DataFrame(columns=["name", "age", "weight", "height", "gen"])

def save_profiles(df):
    df.to_csv(PROFILE_FILE, index=False)

# --- Session state ---
if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = None

# --- Page 1: Login/Register ---
def login_page():
    st.title("🔐 Login or Register")
    profiles = load_profiles()
    usernames = profiles["name"].tolist()

    selected = st.selectbox("Choose existing profile or create new", ["-- New User --"] + usernames)

    if selected == "-- New User --":
        st.subheader("Create Profile")

        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        wt = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
        ht = st.number_input("Height (cm)", min_value=0.0, step=0.1)
        gen = st.selectbox("Gender", ["Male", "Female", "Other"])

        if st.button("Create Profile"):
            if name.strip():
                if name in usernames:
                    st.warning("Name already exists. Choose another.")
                else:
                    new_row = pd.DataFrame([[name.strip(), age, wt, ht, gen]],
                                           columns=["name", "age", "weight", "height", "gen"])
                    updated_profiles = pd.concat([profiles, new_row], ignore_index=True)
                    save_profiles(updated_profiles)
                    st.session_state.person_name = name
                    st.session_state.page = "grocery"
                    st.switch_page("pages/profile.py")
    else:
        if st.button("Login"):
            st.session_state.person_name = selected
            st.session_state.page = "grocery"
            st.switch_page("pages/profile.py")

login_page()