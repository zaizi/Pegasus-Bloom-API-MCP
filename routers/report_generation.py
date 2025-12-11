from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.dependencies import get_db
from typing import  Dict, Any
from datetime import date
from services.cognito.auth import auth_dep
import logging

router = APIRouter(dependencies=[auth_dep])
logger = logging.getLogger(__name__)

@router.get("/generate_service_user_report", tags=["tools"])
def generate_service_user_report(user_id:int, start_date: str, end_date: str, db: Session = Depends(get_db)):
    """
    Retrieves a comprehensive, un-duplicated report of all a service user's
    activities within a given date range.
    """
    
    #Base query for the service user
    user_query = text("""
        SELECT * FROM serviceuser_redacted WHERE id = :user_id
    """)
    
    # Use mappings().first() to get a dict-like object, or None if not found
    user_result = db.execute(user_query, {"user_id": user_id}).mappings().first()


    # This is the base report object we will build
    report: Dict[str, Any] = {"service_user": dict(user_result)}

    # Define all the tables to query and the key they will have in the final JSON report
    activity_tables = {
        "accidents_and_incidents": "dailynote_accidentsincidents_redacted",
        "personal_care_notes": "dailynote_personalcare_redacted",
        "medication_notes": "dailynote_medication_redacted",
        "general_notes": "dailynote_generalnote_redacted",
        "leisure_activity_notes": "dailynote_leisureactivity_redacted",
        "contact_log_notes": "dailynote_contactlog_redacted",
        #No service user id for medication table???
        #"medication_administration_notes": "dailynote_medicationadministration_redacted",
        "night_check_notes": "dailynote_nightcheck_redacted",
        "health_monitoring_notes": "dailynote_healthmonitoring_redacted",
        "meal_notes": "dailynote_meal_redacted",
    }

    
    for report_key, table_name in activity_tables.items():
        try:
            # Use parameterized queries to prevent SQL injection
            query_string = text(f"""
                SELECT * FROM {table_name}
                WHERE
                    service_user_id = :user_id
                    AND CAST(created_on AS DATE) BETWEEN :start_date AND :end_date
            """)
            
            params = {"user_id": user_id, "start_date": start_date, "end_date": end_date}
            
            results = db.execute(query_string, params).mappings().all()
            
            report[report_key] = [dict(row) for row in results]
            report["Date Report Generated"] = date.today()
            
        except Exception as e:
            # If one table fails, log the error but continue building the report
            logger.error(f"Error querying table {table_name}: {e}")
            report[report_key] = {"error": f"Failed to retrieve data from {table_name}."}

    if not report:
        return {"report": "No data available"}
    return report