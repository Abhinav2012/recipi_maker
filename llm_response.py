import google.generativeai as genai
import pandas as pd
import json
from memo import get_all_memories 

def generate_simple_recipe(api_key, user_info, chat_history):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    csv_path = 'grocery_list/grocery_list.csv'
    df_groceries = pd.read_csv(csv_path)
    groceries_md = df_groceries.to_markdown(index=False)

    user_memory = get_all_memories(user_id=user_info['name'])
    
    prompt = (
        f"Generate a simple recipe tailored for a user with the following preferences:\n"
        f"- Profile: {user_info.get('name', 'N/A')}\n"
        f"- Max Cooking Time: {user_info.get('cooking_time_pref', 'N/A')} minutes\n"
        f"- Activity Level: {user_info.get('activity_level', 'N/A')}\n"
        f"- Dietary Preferences: {', '.join(user_info.get('dietary_preferences', []))}\n"
        f"- Servings: {user_info.get('num_servings', 'N/A')}\n"
        f"- Meal Type: {user_info.get('meal_type', 'N/A')}\n\n"
        f"Available groceries:\n{groceries_md}\n\n"
        f"User's memories:\n{user_memory}\n\n"
        "Here is the user's recent conversation that might provide additional context:\n"
    )

    # Append chat history to the prompt
    for message in chat_history:
        prompt += f"{message['role']}: {message['content']}\n"
        
    prompt += "\n"
    
    prompt += "The recipe should include a brief description, a list of ingredients, and step-by-step instructions. "
    prompt += "Provide calorie estimation and nutritional information at the end of the recipe."

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

def get_chat_response(api_key, chat_history, user_info):
    """
    Sends chat history to a backend LLM and returns the response.
    
    Args:
        api_key (str): Your API key for the LLM.
        chat_history (list): The list of chat messages from st.session_state.
        user_info (dict): The user's profile information for context.
        
    Returns:
        str: The generated response from the LLM.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Format the chat history for the LLM
    formatted_chat_history = [{"role": m["role"], "parts": [m["content"]]} for m in chat_history]
    
    # Add user profile info to the first user message for context
    if formatted_chat_history and formatted_chat_history[0]['role'] == 'user':
        # Add the initial context message to the first user part
        initial_context = (
            f"User profile: {json.dumps(user_info)}\n\n"
            "You are a helpful and knowledgeable recipe assistant. Use the user's "
            "profile information to inform your responses, especially for recipe suggestions. "
            "Now, respond to the user's question."
        )
        formatted_chat_history[0]['parts'].insert(0, initial_context)

    try:
        # A simple response to demonstrate functionality
        response = model.generate_content(formatted_chat_history)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"
