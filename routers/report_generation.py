from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.dependencies import get_db

router = APIRouter()

@router.get("/generate_service_user_report", tags=["tools"])
def generate_service_user_report(user_id:int, start_date: str, end_date: str, db: Session = Depends(get_db)):
    """
    Retrieves data for the report used by carehomes staff
    """
    query_string = text("""
        SELECT
            su.id as service_user_id
            ,su.start_date
            ,su.end_date
            ,su.dob
            ,su.min_fluid
            ,su.track_fluid
            ,su.flag_bowel
            ,su.age
            ,su.LOS_days
            ,aai.id as accident_id
            ,aai.transformer_incident_subject as incident_category
            ,aai.created_on as aai_created_on
            ,aai.incident_time
            ,aai.aggressive
            ,aai.toward_su
            ,aai.toward_staff
            ,aai.call_police 
            ,aai.call_paramedics
            ,aai.call_family
            ,aai.rating_1
            ,aai.rating_2
            ,moo1.name as first_mood
            ,moo2.name as second_mood
        FROM serviceuser_redacted su
        LEFT JOIN 
            dailynote_accidentsincidents_redacted aai on aai.service_user_id = su.id                  
        LEFT JOIN 
            dailynote_mood moo1 on aai.mood_1_id = moo1.id
        LEFT JOIN
            dailynote_mood moo2 on aai.mood_2_id = moo2.id
        WHERE
        su.age > 0                
        AND su.id = :user_id  
        AND CAST(su.start_date AS DATE) BETWEEN :start_date AND :end_date  
        AND CAST(su.end_date AS DATE) BETWEEN :start_date AND :end_date 
        AND CAST(aai.created_on AS DATE) BETWEEN :start_date AND :end_date
            
    """)
    
    result = db.execute(
        query_string, 
        {"start_date": start_date, "end_date": end_date, "user_id":user_id}
    ).first()
    
    if result:
        return {"total_accidents": result[0]}
    return {"total_accidents": 0}