from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, Date, text
from typing import Optional, List
from db.dependencies import get_db
from db.models import (
    ServiceUserRedacted as ServiceUser,
    DailyNoteAccidentsIncidentsRedacted as AccidentsIncidents,
    DailyNoteMood as Mood,
)

router = APIRouter()


@router.get("/dash_data_model/", tags=["dashboard"])
def get_dashboard_data_model(
    db: Session = Depends(get_db),
    accident_start_date: Optional[str] = None,
    accident_end_date: Optional[str] = None,
    su_start_date: Optional[str] = None,
    su_end_date: Optional[str] = None,
    aggressive: Optional[int] = None,
    user_id: Optional[List[int]] = Query(None),
    incident_category: Optional[List[str]] = Query(None),
):
    try:
        Mood1 = aliased(Mood)
        Mood2 = aliased(Mood)

        query = (
            db.query(
                ServiceUser.id.label("service_user_id"),
                AccidentsIncidents.id.label("accident_id"),
                AccidentsIncidents.created_on.label("aai_created_on"),
                ServiceUser.start_date,
                ServiceUser.end_date,
                ServiceUser.dob,
                ServiceUser.min_fluid,
                ServiceUser.track_fluid,
                ServiceUser.flag_bowel,
                ServiceUser.age,
                AccidentsIncidents.transformer_incident_subject.label("incident_category"),
                AccidentsIncidents.incident_time,
                AccidentsIncidents.aggressive,
                AccidentsIncidents.toward_su,
                AccidentsIncidents.toward_staff,
                AccidentsIncidents.call_police,
                AccidentsIncidents.call_paramedics,
                AccidentsIncidents.call_family,
                AccidentsIncidents.rating_1,
                AccidentsIncidents.rating_2,
                Mood1.name.label("first_mood"),
                Mood2.name.label("second_mood"),
            )
            .join(AccidentsIncidents, AccidentsIncidents.service_user_id == ServiceUser.id)
            .outerjoin(Mood1, Mood1.id == AccidentsIncidents.mood_1_id)
            .outerjoin(Mood2, Mood2.id == AccidentsIncidents.mood_2_id)
            .filter(ServiceUser.age > 0)
        )

        filters = []
        if accident_start_date:
            filters.append(AccidentsIncidents.created_on.cast(Date) >= accident_start_date)
        if accident_end_date:
            filters.append(AccidentsIncidents.created_on.cast(Date) <= accident_end_date)
        if user_id:
            if len(user_id) > 0:
                filters.append(ServiceUser.id.in_(user_id))
        if su_start_date:
            filters.append(ServiceUser.start_date.cast(Date) >= su_start_date)
        if su_end_date:
            filters.append(ServiceUser.end_date.cast(Date) <= su_end_date)
        if incident_category:
            if len(incident_category) > 0:
                filters.append(AccidentsIncidents.transformer_incident_subject.in_(incident_category))
        if aggressive is not None:
            filters.append(AccidentsIncidents.aggressive == aggressive)

        if filters:
            query = query.filter(and_(*filters))

        results = query.all()
        data = [
            {col.name: getattr(row, col.name) for col in row.__table__.columns}
            if hasattr(row, "__table__") else dict(row._mapping)
            for row in results
        ]

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")


@router.get("/all_user_id/", tags=["dashboard"])
def get_all_user_ids(db: Session = Depends(get_db),):
    try:
        query = db.query(AccidentsIncidents.service_user_id).distinct()
        results = query.all()
        user_ids = [r[0] for r in results]
        return user_ids


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    
@router.get("/all_accident_categories/", tags=["dashboard"])
def get_all_accident_categories(db: Session = Depends(get_db),):
    try:
        query = db.query(AccidentsIncidents.transformer_incident_subject).distinct().order_by(AccidentsIncidents.transformer_incident_subject)
        results = query.all()
        categories = [r[0] for r in results]
        return categories


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")


@router.get("/root_cause_data/", tags=["dashboard"])
def get_root_cause_data(
    db: Session = Depends(get_db),
    accident_start_date: Optional[str] = None,
    accident_end_date: Optional[str] = None,
    user_id: Optional[List[int]] = Query(None),
):
    try:
        if not accident_start_date:
            accident_start_date = (date.today() - timedelta(days=30)).isoformat()
        if not accident_end_date:
            accident_end_date = date.today().isoformat()

        params = {
            "accident_start_date": accident_start_date,
            "accident_end_date": accident_end_date,
        }

        user_filter_clause = ""
        if user_id and len(user_id) > 0:
            user_filter_clause = "WHERE id = ANY(:user_id)"
            params["user_id"] = user_id

        query_string = f"""
        WITH date_series AS (
            SELECT generate_series(
                CAST(:accident_start_date AS DATE),
                CAST(:accident_end_date AS DATE),
                interval '1 day'
            )::date AS day
        ),
        users AS (
            SELECT id AS service_user_id FROM serviceuser_redacted
            {user_filter_clause}
        ),
        personal_model AS (
            SELECT service_user_id, CAST(created_on AS DATE) AS day,
                SUM(bowel_movement) AS total_bowel_movements,
                SUM(urine_passed) AS total_urine_passed,
                SUM(brush_teeth) AS total_brush_teeth
            FROM dailynote_personalcare_redacted
            GROUP BY service_user_id, day
        ),
        leisure_model AS (
            SELECT service_user_id, CAST(created_on AS DATE) AS day,
                COUNT(id) AS count_leisure_activity_on_day
            FROM dailynote_leisureactivity_redacted
            GROUP BY service_user_id, day
        ),
        night_model AS (
            SELECT service_user_id, CAST(created_on AS DATE) AS day,
                COUNT(woken_up_during_night) AS woke_at_night
            FROM dailynote_nightcheck_redacted
            GROUP BY service_user_id, day
        ),
        accident_model AS (
            SELECT service_user_id, CAST(created_on AS DATE) AS day,
                COUNT(*) AS total_accidents,
                SUM(CASE WHEN aggressive = 1 THEN 1 ELSE 0 END) AS aggressive_incidents
            FROM dailynote_accidentsincidents_redacted
            GROUP BY service_user_id, day
        )
        SELECT u.service_user_id, d.day,
            COALESCE(a.total_accidents, 0) AS total_accidents,
            COALESCE(a.aggressive_incidents, 0) AS aggressive_incidents,
            COALESCE(p.total_bowel_movements, 0) AS total_bowel_movements,
            COALESCE(p.total_urine_passed, 0) AS total_urine_passed,
            COALESCE(p.total_brush_teeth, 0) AS total_brush_teeth,
            COALESCE(l.count_leisure_activity_on_day, 0) AS count_leisure_activity_on_day,
            COALESCE(nm.woke_at_night, 0) AS woke_at_night
        FROM users u
        CROSS JOIN date_series d
        LEFT JOIN accident_model a ON a.service_user_id = u.service_user_id AND a.day = d.day
        LEFT JOIN personal_model p ON p.service_user_id = u.service_user_id AND p.day = d.day
        LEFT JOIN leisure_model l ON l.service_user_id = u.service_user_id AND l.day = d.day
        LEFT JOIN night_model nm ON nm.service_user_id = u.service_user_id AND nm.day = d.day
        ORDER BY u.service_user_id, d.day;
        """

        results = db.execute(text(query_string), params)
        data = [dict(row) for row in results.mappings()]
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
