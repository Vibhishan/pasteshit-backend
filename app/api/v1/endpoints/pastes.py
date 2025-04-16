from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional

from app.core.config import get_settings
from app.database.connection import get_db
from app.database import crud
from app.api.v1 import schemas

# Get settings
settings = get_settings()

router = APIRouter(
    prefix="/pastes", 
    tags=["pastes"]
)


@router.post(
    "",
    response_model=schemas.PasteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new paste",
    description="Create a new paste with the provided content and optional expiration date."
)
def create_paste(
    paste: schemas.PasteCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Create a new paste.
    
    Args:
        paste: Paste data
        request: Request object
        db: Database session
        
    Returns:
        PasteResponse: Created paste data
    
    Raises:
        HTTPException: If the paste creation fails
    """
    try:
        # Create paste
        db_paste = crud.create_paste(db=db, paste=paste)
        
        # Generate URL
        base_url = str(request.base_url).rstrip('/')
        paste_url = f"{base_url}{settings.API_V1_PREFIX}/pastes/{db_paste.id}"
        
        return schemas.PasteResponse(id=db_paste.id, url=paste_url)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Log error
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create paste"
        )


@router.get(
    "/{paste_id}",
    response_model=schemas.PasteDetailResponse,
    summary="Get a paste by ID",
    description="Retrieve a paste by its unique identifier."
)
def get_paste(paste_id: str, db: Session = Depends(get_db)):
    """
    Get a paste by ID.
    
    Args:
        paste_id: Paste ID
        db: Database session
        
    Returns:
        PasteDetailResponse: Paste data
    
    Raises:
        HTTPException: If the paste is not found
    """
    # Get paste
    db_paste = crud.get_paste(db=db, paste_id=paste_id)
    
    # Check if paste exists
    if db_paste is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paste with ID {paste_id} not found"
        )
    
    return db_paste


@router.delete(
    "/{paste_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a paste",
    description="Delete a paste by its unique identifier."
)
def delete_paste(paste_id: str, db: Session = Depends(get_db)):
    """
    Delete a paste by ID.
    
    Args:
        paste_id: Paste ID
        db: Database session
        
    Raises:
        HTTPException: If the paste is not found
    """
    # Delete paste
    result = crud.delete_paste(db=db, paste_id=paste_id)
    
    # Check if paste existed
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paste with ID {paste_id} not found"
        )
    
    return None 