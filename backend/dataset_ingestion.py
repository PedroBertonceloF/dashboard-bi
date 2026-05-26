import pandas as pd
import pandas as pd
import os
import shutil

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_and_preview_csv(file_obj, filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file_obj, buffer)

    df = pd.read_csv(file_path, nrows=5, on_bad_lines='skip', engine='python')
    columns = df.columns.tolist()
    # Replace NaNs with None for JSON serialization
    preview = df.where(pd.notnull(df), None).to_dict(orient="records")

    return file_path, columns, preview

def process_and_clean_dataset(file_path: str, date_col: str, category_col: str, value_col: str):
    df = pd.read_csv(file_path, on_bad_lines='skip', engine='python')

    # Check if columns exist
    missing_cols = [col for col in [date_col, category_col, value_col] if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing mapped columns in dataset: {', '.join(missing_cols)}")

    original_rows = len(df)

    # Optimize Date Parsing: 'mixed' format is much faster than default inference in Pandas 2.0+
    # We also use cache=True to speed up repeated dates
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce', format='mixed')

    # Coerce invalid values to NaN
    df[value_col] = pd.to_numeric(df[value_col], errors='coerce')

    # Optimize string empty check: vector string methods are faster than regex replace
    df[category_col] = df[category_col].replace(r'^\s*$', pd.NA, regex=True)

    cleaned_df = df.dropna(subset=[date_col, category_col, value_col])
    cleaned_rows = len(cleaned_df)
    dropped_rows = original_rows - cleaned_rows

    # Save cleaned data
    cleaned_file_path = file_path.replace(".csv", "_cleaned.csv")
    cleaned_df.to_csv(cleaned_file_path, index=False)

    return cleaned_file_path, original_rows, cleaned_rows, dropped_rows
