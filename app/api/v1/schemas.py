from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class PasteBase(BaseModel):
    """
    Base Pydantic model for Paste objects.
    """
    content: str = Field(
        ..., 
        min_length=1,
        description="Text content of the paste"
    )
    
class PasteCreate(PasteBase):
    """
    Pydantic model for creating pastes.
    Only adding expires_at on top of base paste model.
    """
    expires_at: Optional[datetime] = Field(
        None,
        description="Optional expiration date for the paste"
    )

class PasteResponse(BaseModel):
    """
    Pydantic model for paste creation response.
    """
    id: str = Field(
        ...,
        description="Unique identifier for the paste"
    )
    url: str = Field(
        ...,
        description="URL to access the paste"
    )
    
class PasteDetailResponse(BaseModel):
    """
    Pydantic model for detailed paste response.
    """
    id: str = Field(
        ...,
        description="Unique identifier for the paste"
    )
    content: str = Field(
        ...,
        description="Text content of the paste"
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the paste was created"
    )
    expires_at: Optional[datetime] = Field(
        None,
        description="Optional timestamp when the paste will expire"
    )
    
    class Config:
        """Config for Pydantic model."""
        orm_mode = True 