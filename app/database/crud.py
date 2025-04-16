from datetime import datetime
from typing import Optional, Union, Dict, Any

import nanoid
from sqlalchemy.orm import Session

from app.database.models import Paste
from app.api.v1.schemas import PasteCreate


def generate_unique_id(db: Session, size: int = 8) -> str:
    """
    Generate a unique ID using nanoid.
    
    Args:
        db: Database session
        size: Length of the ID
        
    Returns:
        str: Unique ID
    """
    while True:
        new_id = nanoid.generate(size=size)
        # Check for collision
        existing = get_paste(db, new_id)
        if not existing:
            return new_id


def create_paste(db: Session, paste: PasteCreate) -> Paste:
    """
    Create a new paste in the database.
    
    Args:
        db: Database session
        paste: Paste data
        
    Returns:
        Paste: Created paste object
    """
    # Validate input
    if not paste.content:
        raise ValueError("Paste content cannot be empty")
    
    if len(paste.content) > 100000:
        raise ValueError("Paste content exceeds maximum length (100000 characters)")
    
    # Generate ID
    paste_id = generate_unique_id(db)
    
    # Create paste object
    db_paste = Paste(
        id=paste_id,
        content=paste.content,
        expires_at=paste.expires_at
    )
    
    # Add to database
    db.add(db_paste)
    db.commit()
    db.refresh(db_paste)
    
    return db_paste


def get_paste(db: Session, paste_id: str) -> Optional[Paste]:
    """
    Get a paste by ID.
    
    Args:
        db: Database session
        paste_id: Paste ID
        
    Returns:
        Optional[Paste]: Paste object if found, None otherwise
    """
    # Query database
    paste = db.query(Paste).filter(Paste.id == paste_id).first()
    
    # Check if paste exists and is not expired
    if paste and paste.expires_at and paste.expires_at < datetime.now():
        # Paste has expired
        return None
        
    return paste


def delete_paste(db: Session, paste_id: str) -> bool:
    """
    Delete a paste by ID.
    
    Args:
        db: Database session
        paste_id: Paste ID
        
    Returns:
        bool: True if deleted, False otherwise
    """
    # Query database
    paste = db.query(Paste).filter(Paste.id == paste_id).first()
    
    if not paste:
        return False
    
    # Delete paste
    db.delete(paste)
    db.commit()
    
    return True 