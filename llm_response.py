import google.generativeai as genai
import pandas as pd
import json
from memo import get_all_memories 

def generate_simple_recipe(api_key: str,info: dict, csv_path: str = 'grocery_list/grocery_list.csv') -> str:
    
    genai.configure(api_key=api_key)
     
    df = pd.read_csv(csv_path)
    table_text = df.to_markdown(index=False)
    user_memory = get_all_memories(user_id=info['name'])
    
    prompt = f"""Make me a very simple recipe of food using these ingredients. Make it easy and quick.
                 You don't have to use all the items: \n{table_text}. Take the info about the person and make food according to 
                 height and weight and age and gender \n{json.dumps(info, indent=2)}
                 Previous feedback/memory: {user_memory}"""
    
    #current query
    
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    return response.text.strip()

