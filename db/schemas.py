from pydantic import BaseModel
from typing import Optional, List

# --- DailyNotePersonalCareRedacted Schemas ---
class DailyNotePersonalCareRedactedBase(BaseModel):
    care_provide: Optional[str] = None
    wear_decision: Optional[str] = None
    cleaner_type: Optional[str] = None
    body_part: Optional[str] = None
    dry_by: Optional[str] = None
    assistance_detail: Optional[str] = None
    hair_wash: Optional[float] = None
    assistance: Optional[int] = None
    hair_shave: Optional[float] = None
    moving_equipment: Optional[float] = None
    rating_1: Optional[int] = None
    rating_2: Optional[float] = None
    created_on: Optional[str] = None
    created_by_id: Optional[int] = None
    mood_1_id: Optional[int] = None
    mood_2_id: Optional[float] = None
    service_user_id: Optional[int] = None
    brush_teeth: Optional[float] = None
    dry_assistance: Optional[str] = None
    equipment_used: Optional[str] = None
    mouth_wash_used: Optional[int] = None
    personal_care_carried: Optional[str] = None
    su_clothing: Optional[str] = None
    wash_type: Optional[str] = None
    full_description: Optional[str] = None
    notes_and_thoughts: Optional[str] = None
    urgency_flag: Optional[str] = None
    action_note: Optional[str] = None
    marked_read: Optional[int] = None
    note: Optional[str] = None
    bowel_movement: Optional[int] = None
    bowel_size: Optional[str] = None
    urine_passed: Optional[int] = None
    bowel_type: Optional[float] = None
    action_taken: Optional[str] = None
    manager_comment: Optional[str] = None
    action_reason: Optional[str] = None
    action_reason_other: Optional[float] = None

class DailyNotePersonalCareRedacted(DailyNotePersonalCareRedactedBase):
    id: int
    class Config:
        from_attributes = True

# --- ServiceUserRedacted Schemas ---
class ServiceUserRedactedBase(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    dob: Optional[str] = None
    status: Optional[int] = None
    care_giver_id: Optional[float] = None
    created_by_id: Optional[int] = None
    auth_user_id: Optional[float] = None
    created_on: Optional[str] = None
    min_fluid: Optional[float] = None
    track_fluid: Optional[int] = None
    flag_bowel: Optional[int] = None
    age: Optional[float] = None
    LOS_days: Optional[float] = None

class ServiceUserRedacted(ServiceUserRedactedBase):
    id: int
    class Config:
        from_attributes = True

# --- DailyNoteMedicationRedacted Schemas ---
class DailyNoteMedicationRedactedBase(BaseModel):
    created_on: Optional[str] = None
    notes_and_thoughts: Optional[str] = None
    urgency_flag: Optional[str] = None
    marked_read: Optional[int] = None
    action_note: Optional[str] = None
    action_taken: Optional[str] = None
    manager_comment: Optional[str] = None
    created_by_id: Optional[int] = None
    service_user_id: Optional[int] = None
    full_description: Optional[str] = None
    mood_1_new_id: Optional[int] = None
    mood_2_new_id: Optional[float] = None
    rating_1_new: Optional[int] = None
    rating_2_new: Optional[float] = None
    consent_refused: Optional[int] = None
    continueWithoutConsent: Optional[int] = None
    action_reason: Optional[float] = None
    action_reason_other: Optional[float] = None

class DailyNoteMedicationRedacted(DailyNoteMedicationRedactedBase):
    id: int
    class Config:
        from_attributes = True

# --- DailyNoteAccidentsIncidentsRedacted Schemas ---
class DailyNoteAccidentsIncidentsRedactedBase(BaseModel):
    incident_description: Optional[str] = None
    incident_time: Optional[str] = None
    aggressive: Optional[int] = None
    toward_su: Optional[int] = None
    toward_staff: Optional[int] = None
    call_police: Optional[int] = None
    call_paramedics: Optional[int] = None
    call_family: Optional[int] = None
    reported_to: Optional[str] = None
    su_comments: Optional[str] = None
    resolved: Optional[str] = None
    rating_1: Optional[int] = None
    rating_2: Optional[float] = None
    created_on: Optional[str] = None
    created_by_id: Optional[int] = None
    mood_1_id: Optional[int] = None
    mood_2_id: Optional[float] = None
    service_user_id: Optional[int] = None
    full_description: Optional[str] = None
    notes_and_thoughts: Optional[str] = None
    call_other: Optional[int] = None
    incident_string: Optional[float] = None
    who_was_present: Optional[str] = None
    urgency_flag: Optional[str] = None
    action_note: Optional[str] = None
    marked_read: Optional[int] = None
    manager_comment: Optional[str] = None
    action_reason: Optional[str] = None
    action_reason_other: Optional[float] = None
    transformer_incident_subject: Optional[str] = None

class DailyNoteAccidentsIncidentsRedacted(DailyNoteAccidentsIncidentsRedactedBase):
    id: int
    class Config:
        from_attributes = True

# --- DailyNoteGeneralNoteRedacted Schemas ---
class DailyNoteGeneralNoteRedactedBase(BaseModel):
    full_description: Optional[str] = None
    note: Optional[str] = None
    rating_1: Optional[int] = None
    created_on: Optional[str] = None
    notes_and_thoughts: Optional[str] = None
    urgency_flag: Optional[str] = None
    marked_read: Optional[int] = None
    action_note: Optional[str] = None
    created_by_id: Optional[int] = None
    mood_1_id: Optional[float] = None
    mood_2_id: Optional[float] = None
    service_user_id: Optional[int] = None
    manager_comment: Optional[str] = None
    image: Optional[float] = None
    action_reason: Optional[str] = None
    action_reason_other: Optional[str] = None

class DailyNoteGeneralNoteRedacted(DailyNoteGeneralNoteRedactedBase):
    id: int
    class Config:
        from_attributes = True

# --- DailyNoteLeisureActivityRedacted Schemas ---
class DailyNoteLeisureActivityRedactedBase(BaseModel):
    activity_type: Optional[str] = None
    activity_description: Optional[str] = None
    activity_place: Optional[str] = None
    activity_place_description: Optional[str] = None
    su_engaged_with: Optional[str] = None
    su_requested_take_part_again: Optional[int] = None
    activity_duration: Optional[str] = None
    activity_future_request: Optional[str] = None
    rating_1: Optional[int] = None
    rating_2: Optional[float] = None
    created_on: Optional[str] = None
    created_by_id: Optional[int] = None
    mood_1_id: Optional[int] = None
    mood_2_id: Optional[float] = None
    service_user_id: Optional[int] = None
    full_description: Optional[str] = None
    notes_and_thoughts: Optional[str] = None
    urgency_flag: Optional[str] = None
    action_note: Optional[str] = None
    marked_read: Optional[int] = None
    note: Optional[str] = None
    action_taken: Optional[str] = None
    manager_comment: Optional[float] = None
    support_needed: Optional[int] = None
    action_reason: Optional[float] = None
    action_reason_other: Optional[float] = None

class DailyNoteLeisureActivityRedacted(DailyNoteLeisureActivityRedactedBase):
    id: int
    class Config:
        from_attributes = True

# --- DailyNoteContactLogRedacted Schemas ---
class DailyNoteContactLogRedactedBase(BaseModel):
    visited_or_called_person: Optional[str] = None
    su_interact: Optional[int] = None
    description: Optional[str] = None
    addition_comments: Optional[str] = None
    rating_1: Optional[int] = None
    rating_2: Optional[float] = None
    created_on: Optional[str] = None
    created_by_id: Optional[int] = None
    mood_1_id: Optional[int] = None
    mood_2_id: Optional[float] = None
    service_user_id: Optional[int] = None
    full_description: Optional[str] = None
    notes_and_thoughts: Optional[str] = None
    type_of_visit: Optional[str] = None
    urgency_flag: Optional[str] = None
    action_note: Optional[str] = None
    marked_read: Optional[int] = None
    manager_comment: Optional[str] = None
    duration: Optional[str] = None
    type_of_contact: Optional[str] = None
    action_reason: Optional[str] = None
    action_reason_other: Optional[float] = None

class DailyNoteContactLogRedacted(DailyNoteContactLogRedactedBase):
    id: int
    class Config:
        from_attributes = True

# --- DailyNoteMedicationAdministrationRedacted Schemas ---
class DailyNoteMedicationAdministrationRedactedBase(BaseModel):
    full_description: Optional[float] = None
    medication_name: Optional[str] = None
    blister_pack_usage: Optional[int] = None
    blister_pack_usage_reason: Optional[float] = None
    whole_dosage_taken: Optional[int] = None
    whole_dosage_taken_reason: Optional[str] = None
    medication_count: Optional[float] = None
    medication_count_reason: Optional[str] = None
    comment_future_medication: Optional[float] = None
    note: Optional[str] = None
    rating_1: Optional[float] = None
    rating_2: Optional[float] = None
    warning: Optional[str] = None
    warning_reason: Optional[float] = None
    medication_note_id: Optional[int] = None
    photo: Optional[float] = None
    medication_entry_id: Optional[float] = None
    medication_type: Optional[str] = None
    dosage_given: Optional[str] = None
    flag_to_manager: Optional[int] = None

class DailyNoteMedicationAdministrationRedacted(DailyNoteMedicationAdministrationRedactedBase):
    id: int
    class Config:
        from_attributes = True

# --- DailyNoteNightCheckRedacted Schemas ---
class DailyNoteNightCheckRedactedBase(BaseModel):
    sleep_time: Optional[str] = None
    wearing_pad: Optional[int] = None
    bedrails_up: Optional[int] = None
    woken_up_during_night: Optional[int] = None
    woken_up_during_night_reason: Optional[str] = None
    rating_1: Optional[float] = None
    rating_2: Optional[float] = None
    created_on: Optional[str] = None
    created_by_id: Optional[int] = None
    mood_1_id: Optional[float] = None
    mood_2_id: Optional[float] = None
    service_user_id: Optional[int] = None
    full_description: Optional[str] = None
    notes_and_thoughts: Optional[str] = None
    night_check: Optional[str] = None
    urgency_flag: Optional[str] = None
    bed_time: Optional[str] = None
    action_note: Optional[str] = None
    marked_read: Optional[int] = None
    action_taken: Optional[float] = None
    manager_comment: Optional[str] = None
    action_reason: Optional[str] = None
    action_reason_other: Optional[float] = None

class DailyNoteNightCheckRedacted(DailyNoteNightCheckRedactedBase):
    id: int
    class Config:
        from_attributes = True

# --- DailyNoteMood Schemas ---
class DailyNoteMoodBase(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    ordering: Optional[float] = None
    urgency_flag: Optional[float] = None

class DailyNoteMood(DailyNoteMoodBase):
    id: int
    class Config:
        from_attributes = True

# --- DailyNoteHealthMonitoringRedacted Schemas ---
class DailyNoteHealthMonitoringRedactedBase(BaseModel):
    monitoring_type: Optional[str] = None
    rating_1: Optional[int] = None
    rating_2: Optional[float] = None
    created_on: Optional[str] = None
    created_by_id: Optional[int] = None
    mood_1_id: Optional[int] = None
    mood_2_id: Optional[float] = None
    service_user_id: Optional[int] = None
    full_description: Optional[str] = None
    notes_and_thoughts: Optional[str] = None
    blood_test_reason: Optional[str] = None
    blood_test_result: Optional[str] = None
    diastolic: Optional[float] = None
    duration_seizure: Optional[str] = None
    glucose_level: Optional[str] = None
    heart_rate: Optional[str] = None
    heart_rate_notes: Optional[str] = None
    heightbmi: Optional[str] = None
    other_test_reason: Optional[str] = None
    other_test_result: Optional[str] = None
    other_test_taken: Optional[str] = None
    reason_treatment_foot: Optional[str] = None
    seizure_assistance_sought: Optional[int] = None
    systolic: Optional[float] = None
    temperature: Optional[str] = None
    treatment_foot: Optional[str] = None
    type_seizure: Optional[str] = None
    weight_foot: Optional[str] = None
    weightbmi: Optional[str] = None
    wound_care_further_actions: Optional[str] = None
    wound_care_image: Optional[float] = None
    wound_care_location: Optional[str] = None
    wound_care_provided: Optional[str] = None
    wound_care_size: Optional[str] = None
    health_monitor_date: Optional[str] = None
    location: Optional[str] = None
    measurement_system: Optional[str] = None
    refer_to_doctor: Optional[int] = None
    urgency_flag: Optional[str] = None
    action_note: Optional[str] = None
    marked_read: Optional[int] = None
    note: Optional[str] = None
    action_taken: Optional[str] = None
    illness_symptoms: Optional[str] = None
    manager_comment: Optional[str] = None
    treatment_details: Optional[str] = None
    wound_x_position: Optional[float] = None
    wound_y_position: Optional[float] = None
    wound_location_image: Optional[str] = None
    action_reason: Optional[float] = None
    action_reason_other: Optional[float] = None

class DailyNoteHealthMonitoringRedacted(DailyNoteHealthMonitoringRedactedBase):
    id: int
    class Config:
        from_attributes = True

# --- DailyNoteMealRedacted Schemas ---
class DailyNoteMealRedactedBase(BaseModel):
    meal: Optional[str] = None
    prepared: Optional[str] = None
    eating_amount: Optional[float] = None
    eating_method: Optional[str] = None
    nutritional_requirements: Optional[str] = None
    su_drink: Optional[str] = None
    eating_type: Optional[str] = None
    comments: Optional[float] = None
    created_on: Optional[str] = None
    rating_1: Optional[int] = None
    rating_2: Optional[float] = None
    created_by_id: Optional[int] = None
    mood_1_id: Optional[int] = None
    mood_2_id: Optional[float] = None
    service_user_id: Optional[int] = None
    full_description: Optional[str] = None
    notes_and_thoughts: Optional[str] = None
    food_item: Optional[str] = None
    thickener: Optional[int] = None
    urgency_flag: Optional[str] = None
    action_note: Optional[str] = None
    marked_read: Optional[int] = None
    note: Optional[str] = None
    drink_amount: Optional[str] = None
    meal_type: Optional[float] = None
    action_taken: Optional[str] = None
    manager_comment: Optional[str] = None
    drink_total: Optional[str] = None
    action_reason: Optional[float] = None
    action_reason_other: Optional[float] = None

class DailyNoteMealRedacted(DailyNoteMealRedactedBase):
    id: int
    class Config:
        from_attributes = True

