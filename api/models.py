from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Observation(Base):
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    condition = Column(String(50), nullable=False)
    pokemon = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
