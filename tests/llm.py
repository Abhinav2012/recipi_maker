import google.generativeai as genai
import pandas as pd

key = "AIzaSyAAPYkEaq2shO3kvsfGM25AEb2VNaSwrmY"

df = pd.read_csv('grocery_list/grocery_list.csv')

table_text = df.to_markdown(index=False)
prompt = f"""Make me a very simple recipe of food using these ingedriends. make it easy and quick.
            You dont have to use all the items {table_text}"""

genai.configure(api_key=key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
response = model.generate_content(prompt)

print(response.text.strip())