from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()

# Load the CSV once when the app starts
df = pd.read_csv("personal_profile/personal_info.csv")

@app.get("/")
def read_root():
    return {"message": "CSV API is running"}

@app.get("/data")
def get_all_data():
    return df.to_dict(orient="records")

@app.get("/data/{name}")
def get_person_by_name(name: str):
    person = df[df['name'].str.lower() == name.lower()]
    if not person.empty:
        return person.to_dict(orient="records")[0]
    return JSONResponse(status_code=404, content={"error": "Person not found"})

print(get_all_data())
print(get_person_by_name("Abhinav"))