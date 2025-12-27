from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    DateTime, Text, ForeignKey, CheckConstraint
)
from sqlalchemy.orm import declarative_base, relationship, validates
from datetime import datetime

Base = declarative_base()

class AITool(Base):
    __tablename__ = "ai_tools"

    __table_args__ = (
        CheckConstraint('avg_rating >= 0 AND avg_rating <= 5'),
        CheckConstraint('trust_score >= 0 AND trust_score <= 5'),
        CheckConstraint('mostly_used_score >= 0 AND mostly_used_score <= 5'),
    )

    id = Column(Integer, primary_key=True, index=True)
    app_name = Column(String(200), nullable=False, unique=True)
    size_mb = Column(Float, nullable=False)
    is_paid = Column(Boolean, default=False)
    price = Column(Float, nullable=True)
    version = Column(String(50), nullable=False)
    status = Column(String(50), default="active")
    avg_rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    trust_score = Column(Float, default=0.0)
    mostly_used_score = Column(Float, default=0.0)
    date_of_creation = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    description = Column(Text, nullable=True)

    # Relationship with Review table
    reviews = relationship("Review", back_populates="tool", cascade="all, delete-orphan")

    @validates("avg_rating","trust_score","mostly_used_score")
    def validate_rating(self, key, value):
        if value is not None and not (0 <= value <= 5):
            raise ValueError(f"{key} must be between 0 and 5")
        return value

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    tool_id = Column(Integer, ForeignKey("ai_tools.id"), nullable=False)
    user_name = Column(String(100), nullable=True)
    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)
    status = Column(String(50), default="Pending")  # Pending / Approved / Rejected
    date_of_creation = Column(DateTime, default=datetime.utcnow)

    # Relationship back to AI Tool
    tool = relationship("AITool", back_populates="reviews")

    @validates("rating")
    def validate_rating(self, key, value):
        if not (0 <= value <= 5):
            raise ValueError("Rating must be between 0 and 5")
        return value
