import pandas as pd

def calculate_kpis(cleaned_file_path: str, value_col: str):
    df = pd.read_csv(cleaned_file_path)
    
    total_sum = df[value_col].sum()
    average = df[value_col].mean()
    row_count = len(df)
    
    return {
        "total_sum": float(total_sum),
        "average": float(average),
        "row_count": int(row_count)
    }

def generate_timeseries(cleaned_file_path: str, date_col: str, value_col: str):
    df = pd.read_csv(cleaned_file_path)
    df[date_col] = pd.to_datetime(df[date_col]).dt.strftime('%Y-%m-%d')
    grouped = df.groupby(date_col)[value_col].sum().reset_index()
    grouped = grouped.rename(columns={date_col: "date", value_col: "value"})
    return grouped.to_dict(orient="records")

def generate_category_chart(cleaned_file_path: str, category_col: str, value_col: str):
    df = pd.read_csv(cleaned_file_path)
    grouped = df.groupby(category_col)[value_col].sum().reset_index()
    grouped = grouped.rename(columns={category_col: "category", value_col: "value"})
    return grouped.to_dict(orient="records")
