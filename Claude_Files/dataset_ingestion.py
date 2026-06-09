import os
import csv
import io
from pathlib import Path
from typing import Tuple, List, Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime

# Configuration
UPLOAD_DIR = "uploads"
PREVIEW_ROWS = 5

# Ensure upload directory exists
Path(UPLOAD_DIR).mkdir(exist_ok=True)


def save_and_preview_csv(file_obj, filename: str) -> Tuple[str, List[str], List[Dict[str, Any]]]:
    """
    Save uploaded CSV file and return preview data.
    """
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Read file content
    content = file_obj.read()
    
    # Save original file
    with open(file_path, 'wb') as f:
        f.write(content)
    
    # Parse CSV for preview using pandas (fast)
    df = pd.read_csv(io.BytesIO(content), nrows=PREVIEW_ROWS + 1)
    
    columns = df.columns.tolist()
    preview = df.head(PREVIEW_ROWS).to_dict('records')
    
    return file_path, columns, preview


def _is_valid_date(date_str: str) -> bool:
    """
    Check if string is a valid date.
    Accepts formats: YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY
    """
    if not isinstance(date_str, str) or not date_str.strip():
        return False
    
    date_str = date_str.strip()
    
    # Try common date formats
    formats = [
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%d-%m-%Y',
        '%Y/%m/%d',
        '%d.%m.%Y',
    ]
    
    for fmt in formats:
        try:
            datetime.strptime(date_str, fmt)
            return True
        except ValueError:
            continue
    
    return False


def _is_valid_value(value: Any) -> bool:
    """
    Check if value is a valid number (int or float).
    """
    if pd.isna(value):
        return False
    
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def process_and_clean_dataset(
    file_path: str,
    date_col: str,
    category_col: str,
    value_col: str
) -> Tuple[str, int, int, int]:
    """
    Process and clean dataset with strict validation.
    """
    
    # Validate column names exist
    df = pd.read_csv(file_path, nrows=1)
    if date_col not in df.columns:
        raise ValueError(f"Column '{date_col}' not found in CSV")
    if category_col not in df.columns:
        raise ValueError(f"Column '{category_col}' not found in CSV")
    if value_col not in df.columns:
        raise ValueError(f"Column '{value_col}' not found in CSV")
    
    # Read entire CSV with optimized settings
    df = pd.read_csv(
        file_path,
        dtype={date_col: str, category_col: str, value_col: str},
        keep_default_na=False,  # Don't convert empty strings to NaN
        na_values=[''],  # Only treat empty strings as NaN
    )
    
    original_count = len(df)
    
    # Strip whitespace from all string columns (vectorized operation)
    string_cols = df.select_dtypes(include=['object']).columns
    df[string_cols] = df[string_cols].apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
    
    # Create boolean masks for validation (vectorized - very fast)
    # Date validation
    valid_dates = df[date_col].apply(_is_valid_date)
    
    # Category validation (not empty after stripping)
    valid_categories = (df[category_col].notna()) & (df[category_col] != '')
    
    # Value validation (valid number)
    valid_values = df[value_col].apply(_is_valid_value)
    
    # Combine all conditions
    valid_rows = valid_dates & valid_categories & valid_values
    
    # Keep only valid rows
    df_cleaned = df[valid_rows].copy()
    
    cleaned_count = len(df_cleaned)
    dropped_count = original_count - cleaned_count
    
    # Generate output filename
    base_name = os.path.basename(file_path)
    cleaned_filename = base_name.replace('.csv', '_cleaned.csv')
    cleaned_path = os.path.join(UPLOAD_DIR, cleaned_filename)
    
    # Write cleaned CSV with optimized settings
    df_cleaned.to_csv(
        cleaned_path,
        index=False,
        quoting=csv.QUOTE_MINIMAL,
        lineterminator='\n'
    )
    
    return cleaned_path, original_count, cleaned_count, dropped_count
