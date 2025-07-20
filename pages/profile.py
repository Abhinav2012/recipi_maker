import streamlit as st
from llm_response import generate_simple_recipe
from personal_id import get_person_by_name
import json
from memo import add_memory

st.set_page_config(page_title="Profile Detail", layout="wide")

# CSS Styling
st.markdown("""
    <style>
        .square-box {
            width: 200px;
            height: 200px;
            border: 4px solid black;
            margin: auto;
        }
        .label {
            font-weight: bold;
            font-size: 18px;
            text-align: center;
        }
        .value {
            font-size: 16px;
            color: gray;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Layout with columns
left, mid1, mid2, right = st.columns([1, 1, 1, 1])

# Left: Square Box

name = st.session_state.get("person_name", "Unknown")
info = get_person_by_name(name)
abhi1_col,abhi2_col,joel_col = '#ffcccb','#d1ffd1','#f0e68c'

with left:
    st.markdown(f'<div class="profile-box" style="background-color:#ffcccb;">{name}</div>', unsafe_allow_html=True)
 
st.title(f"Profile: {name}")

# Middle 3 Columns: Text & Values
for col, label, val in zip([mid1, mid2, right,mid1,mid2], ["Name", "Height", "Weigth","Age","Gender"], [info['name'],info['height'],info['weight'],info['age'],info['gen']]):
    with col:
        st.markdown(f'<div class="label">{label}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="value">{val}</div>', unsafe_allow_html=True)

if st.button("Grocery List"):
    st.switch_page("pages/list.py")

key = "AIzaSyAAPYkEaq2shO3kvsfGM25AEb2VNaSwrmY"
recipi = generate_simple_recipe(key,info)
st.subheader("Quick Recipe")
st.markdown(f"""
    <div style="text-align: left; font-family: monospace; font-size: 16px;">
        {recipi}
    </div>
""", unsafe_allow_html=True)

st.markdown("### Rate this recipe (1-5)")
rating = st.slider("Your rating:", min_value=1, max_value=5, value=3)
feedback = st.text_area("Any comments or feedback?", "")

if st.button("Submit Feedback"):
    # Store feedback per profile (can be extended to memory system)
    feedback_data = {
        "profile": name,
        "rating": rating,
        "feedback": feedback,
        "recipe": recipi
    }
    add_memory([{"role": "user", "content": json.dumps(feedback_data)}], user_id=name)
st.success("Feedback submitted successfully!")
