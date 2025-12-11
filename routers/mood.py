from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import db.models as models
import db.schemas as schemas
from db.dependencies import get_db
from services.cognito.auth import auth_dep


router = APIRouter(dependencies=[auth_dep])

@router.get("/moods/", response_model=List[schemas.DailyNoteMood])
def read_moods(skip: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retrieve a list of all mood records from the database.
    """
    query = db.query(models.DailyNoteMood)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    notes = query.all()
    return notes