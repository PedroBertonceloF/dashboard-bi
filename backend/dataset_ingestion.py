import pandas as pd
import os
import shutil

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_and_preview_csv(file_obj, filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file_obj, buffer)
        
    df = pd.read_csv(file_path, nrows=5)
    columns = df.columns.tolist()
    # Replace NaNs with None for JSON serialization
    preview = df.where(pd.notnull(df), None).to_dict(orient="records")
    
    return file_path, columns, preview
