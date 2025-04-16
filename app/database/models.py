from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

from app.database.connection import Base

class Paste(Base):
    """
    SQLAlchemy model for paste entries.
    
    Attributes:
        id: Unique identifier for the paste
        content: Text content of the paste
        created_at: Timestamp when the paste was created
        expires_at: Optional timestamp when the paste will expire
    """
    __tablename__ = "pastes"

    id = Column(String, primary_key=True, index=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    expires_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Paste(id='{self.id}', created_at='{self.created_at}')>" 