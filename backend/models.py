from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    original_filename = Column(String)
    file_path = Column(String)
    
    date_col = Column(String, nullable=True)
    category_col = Column(String, nullable=True)
    value_col = Column(String, nullable=True)
    
    is_cleaned = Column(Boolean, default=False)
    cleaned_file_path = Column(String, nullable=True)
