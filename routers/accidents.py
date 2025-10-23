from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.dependencies import get_db

router = APIRouter()

@router.get("/get_accidents_count/", tags=["tools"])
def get_accidents_count(start_date: str, end_date: str, db: Session = Depends(get_db)):
    """
    Retrieves the number of distinct accidents within a given date period.
    """
    query_string = text("""
        SELECT
            COUNT(DISTINCT aai.id) AS accident_count
        FROM 
            dailynote_accidentsincidents_redacted aai
        WHERE
            CAST(aai.created_on AS DATE) BETWEEN :start_date AND :end_date
    """)
    
    result = db.execute(
        query_string, 
        {"start_date": start_date, "end_date": end_date}
    ).first()
    
    if result:
        return {"total_accidents": result[0]}
    return {"total_accidents": 0}