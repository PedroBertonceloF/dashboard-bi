from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
import jwt
import models
import security
import dataset_ingestion
import analytics
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class DatasetResponse(BaseModel):
    dataset_id: int
    columns: list[str]
    preview: list[dict]

class ColumnMapping(BaseModel):
    date_col: str
    category_col: str
    value_col: str

class ProcessResponse(BaseModel):
    message: str
    original_rows: int
    cleaned_rows: int
    dropped_rows: int

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/api/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = security.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/auth/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = security.create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.post("/api/datasets/upload", response_model=DatasetResponse)
def upload_dataset(file: UploadFile = File(...), current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    unique_filename = f"{current_user.id}_{file.filename}"
    try:
        file_path, columns, preview = dataset_ingestion.save_and_preview_csv(file.file, unique_filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV file: {str(e)}")
    
    db_dataset = models.Dataset(user_id=current_user.id, original_filename=file.filename, file_path=file_path)
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    
    return {
        "dataset_id": db_dataset.id,
        "columns": columns,
        "preview": preview
    }

@app.post("/api/datasets/{dataset_id}/process", response_model=ProcessResponse)
def process_dataset(dataset_id: int, mapping: ColumnMapping, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_dataset = db.query(models.Dataset).filter(models.Dataset.id == dataset_id, models.Dataset.user_id == current_user.id).first()
    if not db_dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    try:
        cleaned_path, orig_rows, clean_rows, drop_rows = dataset_ingestion.process_and_clean_dataset(
            file_path=db_dataset.file_path,
            date_col=mapping.date_col,
            category_col=mapping.category_col,
            value_col=mapping.value_col
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    db_dataset.date_col = mapping.date_col
    db_dataset.category_col = mapping.category_col
    db_dataset.value_col = mapping.value_col
    db_dataset.is_cleaned = True
    db_dataset.cleaned_file_path = cleaned_path
    db.commit()
    
    return {
        "message": "Dataset processed successfully",
        "original_rows": orig_rows,
        "cleaned_rows": clean_rows,
        "dropped_rows": drop_rows
    }

class KPIResponse(BaseModel):
    total_sum: float
    average: float
    row_count: int

@app.get("/api/datasets/{dataset_id}/kpis", response_model=KPIResponse)
def get_dataset_kpis(dataset_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_dataset = db.query(models.Dataset).filter(models.Dataset.id == dataset_id, models.Dataset.user_id == current_user.id).first()
    if not db_dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    if not db_dataset.is_cleaned or not db_dataset.cleaned_file_path:
        raise HTTPException(status_code=400, detail="Dataset must be cleaned before generating KPIs")
        
    kpis = analytics.calculate_kpis(db_dataset.cleaned_file_path, db_dataset.value_col)
    
    return kpis

class ChartPoint(BaseModel):
    value: float

class TimeSeriesPoint(ChartPoint):
    date: str

class CategoryPoint(ChartPoint):
    category: str

@app.get("/api/datasets/{dataset_id}/charts/timeseries", response_model=list[TimeSeriesPoint])
def get_timeseries(dataset_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_dataset = db.query(models.Dataset).filter(models.Dataset.id == dataset_id, models.Dataset.user_id == current_user.id).first()
    if not db_dataset or not db_dataset.is_cleaned:
        raise HTTPException(status_code=404, detail="Dataset not found or not cleaned")
    return analytics.generate_timeseries(db_dataset.cleaned_file_path, db_dataset.date_col, db_dataset.value_col)

@app.get("/api/datasets/{dataset_id}/charts/categories", response_model=list[CategoryPoint])
def get_categories(dataset_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_dataset = db.query(models.Dataset).filter(models.Dataset.id == dataset_id, models.Dataset.user_id == current_user.id).first()
    if not db_dataset or not db_dataset.is_cleaned:
        raise HTTPException(status_code=404, detail="Dataset not found or not cleaned")
    return analytics.generate_category_chart(db_dataset.cleaned_file_path, db_dataset.category_col, db_dataset.value_col)
