import pandas as pd

def _apply_filters(df, date_col, category_col, start_date=None, end_date=None, categories=None):
    if start_date:
        df = df[df[date_col] >= start_date]
    if end_date:
        df = df[df[date_col] <= end_date]
    if categories:
        cat_list = [c.strip() for c in categories.split(',')]
        df = df[df[category_col].isin(cat_list)]
    return df

def calculate_kpis(cleaned_file_path: str, date_col: str, category_col: str, value_col: str, start_date: str = None, end_date: str = None, categories: str = None):
    df = pd.read_csv(cleaned_file_path)
    df = _apply_filters(df, date_col, category_col, start_date, end_date, categories)
    
    total_sum = df[value_col].sum() if not df.empty else 0.0
    average = df[value_col].mean() if not df.empty else 0.0
    row_count = len(df)
    
    return {
        "total_sum": float(total_sum),
        "average": float(average),
        "row_count": int(row_count)
    }

def generate_timeseries(cleaned_file_path: str, date_col: str, category_col: str, value_col: str, start_date: str = None, end_date: str = None, categories: str = None):
    df = pd.read_csv(cleaned_file_path)
    df = _apply_filters(df, date_col, category_col, start_date, end_date, categories)
    
    if df.empty:
        return []
        
    df[date_col] = pd.to_datetime(df[date_col]).dt.strftime('%Y-%m-%d')
    grouped = df.groupby(date_col)[value_col].sum().reset_index()
    grouped = grouped.rename(columns={date_col: "date", value_col: "value"})
    return grouped.to_dict(orient="records")

def generate_category_chart(cleaned_file_path: str, date_col: str, category_col: str, value_col: str, start_date: str = None, end_date: str = None, categories: str = None):
    df = pd.read_csv(cleaned_file_path)
    df = _apply_filters(df, date_col, category_col, start_date, end_date, categories)
    
    if df.empty:
        return []
        
    grouped = df.groupby(category_col)[value_col].sum().reset_index()
    grouped = grouped.rename(columns={category_col: "category", value_col: "value"})
    return grouped.to_dict(orient="records")

def generate_export_csv(cleaned_file_path: str, date_col: str, category_col: str, value_col: str, start_date: str = None, end_date: str = None, categories: str = None):
    df = pd.read_csv(cleaned_file_path)
    df = _apply_filters(df, date_col, category_col, start_date, end_date, categories)
    
    total_sum = df[value_col].sum() if not df.empty else 0.0
    average = df[value_col].mean() if not df.empty else 0.0
    row_count = len(df)
    
    csv_header = f"KPI: Total Sum,{total_sum:.2f}\n"
    csv_header += f"KPI: Average,{average:.2f}\n"
    csv_header += f"KPI: Row Count,{row_count}\n\n"
    
    return csv_header + df.to_csv(index=False)
