from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime, timezone
from database import Base

class PersonPosition(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))