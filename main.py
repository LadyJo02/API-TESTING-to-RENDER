import os

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for request validation
class Item(BaseModel):
    name: str
    message: str

# File name for CSV storage
CSV_FILE = "data.csv"

# Initialize CSV file if it does not exist
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["name", "message"])
    df.to_csv(CSV_FILE, index=False)

# POST request to receive data
@app.post("/data")
def receive_data(item: Item):
    # Read the existing CSV file
    df = pd.read_csv(CSV_FILE)

    # Append the new data
    new_data = pd.DataFrame([{"name": item.name, "message": item.message}])
    df = pd.concat([df, new_data], ignore_index=True)

    # Save back to CSV
    df.to_csv(CSV_FILE, index=False)

    return {"message": "Data saved successfully", "data": item}

# GET request to retrieve all data
@app.get("/data")
def get_data():
    # Read the existing CSV file
    df = pd.read_csv(CSV_FILE)
    return df.to_dict(orient="records")
