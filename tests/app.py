import streamlit as st
import os

st.set_page_config(page_title="Profiles", layout="wide")

# Basic page styling
st.markdown("""
    <style>
        .stApp {
            background-color: #add8e6;
        }
        .profile-box {
            height: 200px;
            width: 200px;
            border-radius: 20px;
            border: 4px solid black;
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            font-size: 22px;
            margin: 0 auto 10px auto; /* This margin helps push the button closer */
        }
        h1, h2 {
            text-align: center;
            color: black;
        }
        /* New or modified CSS for button centering */
        .stButton>button {
            display: block; /* Make the button a block element */
            margin: 10px auto; /* Center it horizontally with auto margins and add some top margin */
            width: fit-content; /* Ensure the button only takes up necessary width */
        }
        /* Optional: Remove button-wrapper as stButton>button handles centering */
        /* .button-wrapper {
            display: flex;
            justify-content: center;
        } */
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>Welcome</h1>", unsafe_allow_html=True)
st.markdown("<h2>Choose your profile</h2>", unsafe_allow_html=True)
abhi1_col,abhi2_col,joel_col = '#ffcccb','#d1ffd1','#f0e68c'
# Create 3 perfectly spaced columns
cols = st.columns([1, 1, 1])

with cols[0]:
    st.markdown(f'<div class="profile-box" style="background-color:{abhi1_col};">Abhinav</div>', unsafe_allow_html=True)
    if st.button("Select Me", key="p1"):
        st.success("Abhinav's Profile selected")
        st.session_state.person_name = "Abhinav"
        st.switch_page("pages/profile.py")


with cols[1]:
    st.markdown(f'<div class="profile-box" style="background-color:{abhi2_col};">Abhijeet</div>', unsafe_allow_html=True)
    if st.button("Select Me", key="p2"):
        st.success("Abhijeet's Profile selected")
        st.session_state.person_name = "Abhijeet"
        st.switch_page("pages/profile.py")

with cols[2]:
    st.markdown(f'<div class="profile-box" style="background-color:{joel_col};">joel</div>', unsafe_allow_html=True)
    if st.button("Select Me", key="p3"):
        st.success("Joel's Profile selected")
        st.session_state.person_name = "Joel"
        st.switch_page("pages/profile.py")