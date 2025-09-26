from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import db.models as models
import db.schemas as schemas
from db.dependencies import get_db

router = APIRouter()
@router.get("/personal-care-notes/", response_model=List[schemas.DailyNotePersonalCareRedacted])
def read_personal_care_notes(skip: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retrieve a list of all personal care notes from the database.
    """
    query = db.query(models.DailyNotePersonalCareRedacted)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    notes = query.all()
    return notes

@router.get("/medication-notes/", response_model=List[schemas.DailyNoteMedicationRedacted])
def read_medication_notes(skip: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retrieve a list of all medication notes from the database.
    """
    query = db.query(models.DailyNoteMedicationRedacted)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    notes = query.all()
    return notes

@router.get("/accidents-incidents/", response_model=List[schemas.DailyNoteAccidentsIncidentsRedacted])
def read_accidents_incidents(skip: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retrieve a list of all accident and incident notes from the database.
    """
    query = db.query(models.DailyNoteAccidentsIncidentsRedacted)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    notes = query.all()
    return notes

@router.get("/general-notes/", response_model=List[schemas.DailyNoteGeneralNoteRedacted])
def read_general_notes(skip: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retrieve a list of all general notes from the database.
    """
    query = db.query(models.DailyNoteGeneralNoteRedacted)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    notes = query.all()
    return notes

@router.get("/leisure-activity-notes/", response_model=List[schemas.DailyNoteLeisureActivityRedacted])
def read_leisure_activity_notes(skip: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retrieve a list of all leisure activity notes from the database.
    """
    query = db.query(models.DailyNoteLeisureActivityRedacted)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    notes = query.all()
    return notes

@router.get("/contact-logs/", response_model=List[schemas.DailyNoteContactLogRedacted])
def read_contact_logs(skip: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retrieve a list of all contact logs from the database.
    """
    query = db.query(models.DailyNoteContactLogRedacted)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    notes = query.all()
    return notes

@router.get("/medication-administrations/", response_model=List[schemas.DailyNoteMedicationAdministrationRedacted])
def read_medication_administrations(skip: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retrieve a list of all medication administration records from the database.
    """
    query = db.query(models.DailyNoteMedicationAdministrationRedacted)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    notes = query.all()
    return notes

@router.get("/night-checks/", response_model=List[schemas.DailyNoteNightCheckRedacted])
def read_night_checks(skip: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retrieve a list of all night check records from the database.
    """
    query = db.query(models.DailyNoteNightCheckRedacted)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    notes = query.all()
    return notes

@router.get("/health-monitoring-notes/", response_model=List[schemas.DailyNoteHealthMonitoringRedacted])
def read_health_monitoring_notes(skip: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retrieve a list of all health monitoring notes from the database.
    """
    query = db.query(models.DailyNoteHealthMonitoringRedacted)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    notes = query.all()
    return notes

@router.get("/meals/", response_model=List[schemas.DailyNoteMealRedacted])
def read_meals(skip: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retrieve a list of all meal records from the database.
    """
    query = db.query(models.DailyNoteMealRedacted)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    notes = query.all()
    return notes

@router.get("/service-users/", response_model=List[schemas.ServiceUserRedacted])
def read_service_users(skip: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retrieve a list of all service user records from the database.
    """
    query = db.query(models.ServiceUserRedacted)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    users = query.all()
    return users