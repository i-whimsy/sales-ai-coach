from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Recording(Base):
    __tablename__ = "recordings"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    upload_time = Column(DateTime, default=datetime.utcnow)
    score = Column(Float)
    report_json = Column(Text)