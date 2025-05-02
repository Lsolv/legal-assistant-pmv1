from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..utils.database import Base

class LegalQuery(Base):
    __tablename__ = "legal_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    response = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="queries")