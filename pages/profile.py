import streamlit as st
from llm_response import generate_simple_recipe, get_chat_response
from personal_id import get_person_by_name
import json
import os
from memo import add_memory
import time

from dotenv import load_dotenv
load_dotenv()

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
        /* Custom styling for the profile box for better visual appeal */
        .profile-box {
            background-color: #ffcccb;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            font-size: 24px;
            color: #333;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
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
        /* Style for text inputs/select boxes */
        .stTextInput>div>div>input, .stSelectbox>div>div>div>div {
            border-radius: 8px;
            border: 1px solid #ccc;
            padding: 15px; /* Increased padding for visual size */
            font-size: 22px; /* Increased font size */
            height: auto; /* Allow height to adjust based on padding/font size */
            min-height: 45px; /* Ensure a minimum height */
        }
        /* Ensure the dropdown text itself is also larger */
        .stSelectbox>div>div>div>span {
            font-size: 22px; /* Increased font size */
        }
        /* Style for the options within the selectbox dropdown list */
        .stSelectbox div[role="listbox"] div span {
            font-size: 20px; /* Adjust font size for dropdown options */
            padding: 10px; /* Adjust padding for dropdown options */
        }
    </style>
""", unsafe_allow_html=True)

# Layout with columns for main content
left_col, right_col = st.columns([1, 3])

# Profile Info
name = st.session_state.get("person_name", "Unknown")
info = get_person_by_name(name)

with left_col:
    st.markdown(f'<div class="profile-box">{name}</div>', unsafe_allow_html=True)
    st.title(f"Profile: {name}")

    # Display Attributes
    st.subheader("Personal Details")
    st.write(f"**Name:** {info.get('name', 'N/A')}")
    st.write(f"**Height:** {info.get('height', 'N/A')}")
    st.write(f"**Weight:** {info.get('weight', 'N/A')}")
    st.write(f"**Age:** {info.get('age', 'N/A')}")
    st.write(f"**Gender:** {info.get('gen', 'N/A')}")

    st.markdown("---") # Separator

    # New options for recipe generation criteria
    st.subheader("Recipe Preferences 🍽️")

    # Cooking Time Preference (Slider)
    cooking_time = st.slider(
        "Max Cooking Time (minutes)",
        min_value=15,
        max_value=120,
        value=30,
        step=15,
        help="Specify the maximum time you'd like to spend cooking."
    )
    # Store in info dictionary for LLM
    info['cooking_time_pref'] = cooking_time

    # Activity Level (Selectbox)
    activity_level = st.selectbox(
        "Your Activity Level",
        ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"],
        index=2, # Default to Moderately Active
        help="How active are you normally? This helps determine calorie needs."
    )
    # Store in info dictionary for LLM
    info['activity_level'] = activity_level

    # Dietary Preferences/Restrictions (Multiselect)
    dietary_preferences = st.multiselect(
        "Dietary Preferences/Restrictions",
        ["Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo", "Dairy-Free", "Nut-Free", "Pescatarian"],
        help="Select any dietary preferences or restrictions you have."
    )
    # Store in info dictionary for LLM
    info['dietary_preferences'] = dietary_preferences

    # Number of Servings (Number Input)
    num_servings = st.number_input(
        "Number of Servings",
        min_value=1,
        max_value=10,
        value=2,
        step=1,
        help="How many people will this recipe serve?"
    )
    # Store in info dictionary for LLM
    info['num_servings'] = num_servings

    # Meal Type (Selectbox)
    meal_type = st.selectbox(
        "Meal Type",
        ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"],
        help="What type of meal are you looking for?"
    )
    # Store in info dictionary for LLM
    info['meal_type'] = meal_type

    # Grocery List Navigation
    if st.button("Grocery List"):
        st.switch_page("pages/list.py")

with right_col:
    st.subheader("Recipe Generator")
    # Button to trigger recipe generation
    if st.button("Give Recipe"):
        st.session_state["recipe_generated"] = True
        key = os.getenv("GEMINI_API_KEY")
        # Display a loading message while the API call is in progress
        with st.spinner("Generating recipe..."):
            # Pass the updated 'info' dictionary and the chat history to the recipe generation function
            st.session_state["generated_recipe"] = generate_simple_recipe(key, info, st.session_state.messages)
            # Store the current profile name to pass to the feedback page
            st.session_state["feedback_profile_name"] = name
        st.success("Recipe generated!")

    # Display Recipe only if it has been generated
    if st.session_state.get("recipe_generated"):
        recipi = st.session_state.get("generated_recipe", "No recipe generated yet.")
        st.subheader("Quick Recipe")
        st.markdown(f"""
            <div style="text-align: left; font-family: monospace; font-size: 16px; border: 1px solid #ddd; padding: 15px; border-radius: 8px; background-color: #f9f9f9;">
                {recipi}
            </div>
        """, unsafe_allow_html=True)

        # Button to navigate to the feedback page
        if st.button("Give Feedback on this Recipe"):
            st.switch_page("pages/feedback_page.py") # Navigate to the new feedback page
    else:
        st.info("Click 'Give Recipe' to generate a recipe based on your preferences!")

    st.markdown("---")
    
    # --- Chatbox Functionality ---
    st.subheader("Chat with the Recipe Bot 🤖")
    st.info("Ask about the recipe or for a different suggestion!")

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What's your question?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Call get_chat_response to get the conversational reply
                chat_response = get_chat_response(os.getenv("GEMINI_API_KEY"), st.session_state.messages, info)
                
                # If no flag, just display the chat response as usual
                st.markdown(chat_response)
                st.session_state.messages.append({"role": "assistant", "content": chat_response})