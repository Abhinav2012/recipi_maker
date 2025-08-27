import streamlit as st
import json
from memo import add_memory # Keep this import here as it's used for submitting feedback

st.set_page_config(page_title="Recipe Feedback", layout="wide")

# CSS Styling (re-include relevant styles for consistency)
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50; /* Green */
            color: white;
            padding: 10px 24px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            font-size: 18px;
            margin-top: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        /* Style for text areas */
        .stTextArea>div>div>textarea {
            border-radius: 8px;
            border: 1px solid #ccc;
            padding: 10px;
            font-size: 18px;
            min-height: 150px; /* Make the text area larger */
        }
        .stSlider .st-fx { /* Target the slider label */
            font-weight: bold;
            font-size: 18px;
        }
        /* Ensure the main content div for the recipe has similar styling for consistency */
        .recipe-display-box {
            text-align: left;
            font-family: monospace;
            font-size: 16px;
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 8px;
            background-color: #f9f9f9;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Provide Recipe Feedback 📝")

# Retrieve generated recipe and profile name from session state
recipi = st.session_state.get("generated_recipe", "No recipe was generated. Please go back to the profile page to generate one.")
name = st.session_state.get("feedback_profile_name", "Unknown Profile")

st.subheader(f"Feedback for Recipe generated for: {name}")

# Display the recipe for context
st.markdown("---")
st.markdown("**Recipe you are reviewing:**")
st.markdown(f'<div class="recipe-display-box">{recipi}</div>', unsafe_allow_html=True)
st.markdown("---")

# --- Rating Sliders ---
st.markdown("### Rate this recipe on:")

col1, col2, col3 = st.columns(3)

with col1:
    taste = st.slider("Taste", 1, 5, 3, key="feedback_taste")
    st.caption("🍽️ Taste")

with col2:
    simplicity = st.slider("Simplicity", 1, 5, 3, key="feedback_simplicity")
    st.caption("🛠️ Simplicity")

with col3:
    healthiness = st.slider("Healthiness", 1, 5, 3, key="feedback_healthiness")
    st.caption("💪 Healthiness")

# Feedback Box
feedback = st.text_area("Any comments or feedback?", "")

if st.button("Submit Feedback"):
    if recipi == "No recipe was generated. Please go back to the profile page to generate one.":
        st.warning("Please generate a recipe on the profile page before submitting feedback.")
    else:
        feedback_data = {
            "profile": name,
            "ratings": {
                "taste": taste,
                "simplicity": simplicity,
                "healthiness": healthiness
            },
            "feedback": feedback,
            "recipe": recipi # Include the recipe in the feedback data
        }
        add_memory([{"role": "user", "content": json.dumps(feedback_data)}], user_id=name)
        st.success("Feedback submitted successfully!")
        st.info("You can now go back to the profile page or submit more feedback.")

st.markdown("---")
if st.button("Go back to Profile"):
    st.switch_page("pages/profile.py") # Assuming the main app is named streamlit_app.py
