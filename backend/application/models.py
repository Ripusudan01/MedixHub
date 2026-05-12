from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    user_fullname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    user_password = db.Column(db.String(200), nullable=False)
    user_role = db.Column(db.Enum("admin", "doctor", "patient", name="user_roles"), default="patient", nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    user_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    doctor_profile = db.relationship("DoctorProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    patient_profile = db.relationship("PatientProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    appointments_as_doctor = db.relationship("Appointment", backref="doctor", foreign_keys="Appointment.doctor_id", cascade="all, delete-orphan")
    appointments_as_patient = db.relationship("Appointment", backref="patient", foreign_keys="Appointment.patient_id", cascade="all, delete-orphan")

class Department(db.Model):
    __tablename__ = "departments"

    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    department_description = db.Column(db.Text)

    doctors = db.relationship("DoctorProfile", backref="department")

class DoctorProfile(db.Model):
    __tablename__ = "doctor_profiles"

    doctor_profile_id = db.Column(db.Integer, primary_key=True)
    doctor_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False, unique=True)
    doctor_specialization = db.Column(db.String(100), nullable=False)
    doctor_availability = db.Column(db.JSON)
    doctor_department_id = db.Column(db.Integer, db.ForeignKey("departments.department_id"))
    # doctor_experience = db.Column(db.Integer, nullable=False)
    # doctor_fee = db.Column(db.Integer, nullable=False)

class PatientProfile(db.Model):
    __tablename__ = "patient_profiles"

    patient_profile_id = db.Column(db.Integer, primary_key=True)
    patient_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False, unique=True)
    patient_age = db.Column(db.Integer)
    patient_gender = db.Column(db.Enum("Male", "Female", "Other", name="genders"), nullable=True)
    patient_contact = db.Column(db.String(20))

class Appointment(db.Model):
    __tablename__ = "appointments"

    appointment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False, index=True)
    appointment_date = db.Column(db.Date, nullable=False, index=True)
    appointment_time = db.Column(db.Time, nullable=False)
    appointment_status = db.Column(db.Enum("Booked", "Completed", "Cancelled", name="appointment_statuses"), default="Booked", nullable=False)
    appointment_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    treatment = db.relationship("Treatment", backref="appointment", uselist=False, cascade="all, delete-orphan")

class Treatment(db.Model):
    __tablename__ = "treatments"

    treatment_id = db.Column(db.Integer, primary_key=True)
    treatment_appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.appointment_id"), nullable=False, unique=True)
    treatment_diagnosis = db.Column(db.Text)
    treatment_prescription = db.Column(db.Text)
    treatment_notes = db.Column(db.Text)
    treatment_created_at = db.Column(db.DateTime, default=datetime.utcnow)