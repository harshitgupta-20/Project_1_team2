
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, Numeric
import datetime

Base = declarative_base()

class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    app_name = Column(String(255), unique=True, nullable=False)

    # App details
    size_mb = Column(Float, nullable=True)
    is_paid = Column(Boolean, nullable=False, default=False)
    price = Column(Numeric(10, 2), nullable=True)  # null if not paid
    version = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False, default="active")  # 'active' | 'inactive'

    # Metrics
    avg_rating = Column(Float, nullable=False, default=0.0)
    rating_count = Column(Integer, nullable=False, default=0)
    trust_score = Column(Float, nullable=False, default=0.0)
    mostly_used_score = Column(Float, nullable=False, default=0.0)

    # Timestamps
    date_of_creation = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Optional description
    description = Column(Text, nullable=True)
