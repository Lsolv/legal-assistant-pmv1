from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..utils.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_disabled = Column(Boolean, default=False)
    accessibility_preferences = Column(String)  # JSON con preferencias de accesibilidad
    
    queries = relationship("LegalQuery", back_populates="user")
