from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from db import schemas
from db.dependencies import get_db

router = APIRouter()

@router.get("/dash_data_model/", response_model=List[schemas.DashDataModel], tags=["Dashboard"])
def get_dashboard_data_model(db: Session = Depends(get_db)):
    """
    Retrieves a denormalized dataset for accident prediction modeling by joining
    service user data with their accidents and associated moods.
    """

    query_string = """
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
        LEFT JOIN dailynote_accidentsincidents_redacted aai on aai.service_user_id = su.id 
        LEFT JOIN dailynote_mood moo1 on aai.mood_1_id = moo1.id
        LEFT JOIN dailynote_mood moo2 on aai.mood_2_id = moo2.id

        WHERE
            su.age > 0
            AND
            su.status = 1
    """
    

    results = db.execute(text(query_string))
    
    # Convert the results to a list of dictionaries that Pydantic can understand
    data = [dict(row) for row in results.mappings()]
    
    return data