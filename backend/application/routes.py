from flask import jsonify, request, send_from_directory
from application.models import *
from flask_jwt_extended import create_access_token, current_user, jwt_required
from functools import wraps
from datetime import date, timedelta, time
from .tasks import export_csv_report, monthly_doctor_report, generate_msg_patient, generate_doctor_credentials
from celery.result import AsyncResult 
from .cache import cache

def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.user_role != roles:
                return jsonify(msg="Access denied: insufficient role"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def routesRegistration(app):
    #------------------------------ LOGIN ------------------------------
    @app.route("/api/login", methods=["POST"])
    def login():
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        user = User.query.filter_by(username=username).first()
        if not user or not user.user_password == password:
            return jsonify(message = "Wrong username or password"), 401
        if not user.is_active:
            return jsonify(message = "Your account has been blocked"), 403
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token, role=user.user_role, id=user.user_id)
    
    #------------------------------ REGISTER ------------------------------
    @app.route("/api/register", methods=['POST'])
    def register():
        username = request.json.get("username", None)
        fullname = request.json.get("fullname", None)
        password = request.json.get("password", None)

        if User.query.filter_by(username=username).first():
            return jsonify("User already exists"), 409
        
        user = User(username=username, user_fullname=fullname, user_password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify("User added succesfully"), 201
    
    @app.route("/api/dash_layout_data")
    @jwt_required()
    def dashLayoutData():
        patient_profile = getattr(current_user, "patient_profile", None)

        return jsonify({
            "fullname": current_user.user_fullname,
            "age": patient_profile.patient_age if patient_profile else None,
            "ph_number": patient_profile.patient_contact if patient_profile else None
        })

    #------------------------------ ADMIN DASHBOARD ------------------------------
    
    @app.route("/api/admin_dash/homePage", methods=['GET'])
    @role_required("admin")
    @cache.cached(timeout=5)
    def adminDashHome():
        patients_count = User.query.filter_by(user_role='patient').count()
        doctors_count = User.query.filter_by(user_role='doctor').count()
        today_appointment = Appointment.query.filter(Appointment.appointment_date == date.today(),
                                                        Appointment.appointment_status == "Booked").count()
        completed_appointment = Appointment.query.filter(Appointment.appointment_status == "Completed").count()
        cancelled_appointment = Appointment.query.filter(Appointment.appointment_status == "Cancelled").count()
        recent_5_user = User.query.filter(User.user_role!="admin").order_by(User.user_created_at.desc()).limit(5).all()

        return jsonify({
        "role": current_user.user_role,
        "total_doctors": doctors_count,
        "total_patients": patients_count,
        "upcoming_appointments_count": today_appointment,
        "completed_appointments_count": completed_appointment,
        "cancelled_appointments_count": cancelled_appointment,
        "recent_5_user": [
            {
                "user_id": p.user_id,
                "name": p.user_fullname,
                "registered_on": p.user_created_at.strftime("%d-%m-%Y"),
                "status": p.is_active,
                "role": p.user_role
            } for p in recent_5_user
        ]})
    
    @app.route("/api/admin_dash/doctorPage", methods=['GET', 'POST'])
    @role_required("admin")
    def adminDashDoctor():
        if request.method == 'GET':
            doctors = User.query.filter_by(user_role="doctor").all()
            departments = Department.query.all()
            return jsonify({
                "doctors": [
                    {
                        "id": d.user_id,
                        "fullname": d.user_fullname,
                        "username": d.username,
                        "specialization": d.doctor_profile.doctor_specialization if d.doctor_profile else None,
                        "status": d.is_active,
                        "joined_on": d.user_created_at.strftime("%d-%m-%Y"),
                        "department_id": d.doctor_profile.doctor_department_id if d.doctor_profile else None,
                        "department_name": d.doctor_profile.department.department_name if d.doctor_profile and d.doctor_profile.department else None
                    }
                    for d in doctors
                ],
                "departments": [
                    {"id": dep.department_id, "name": dep.department_name}
                    for dep in departments
                ]
            })

        else:
            fullname = request.json.get("fullname", None)
            username = request.json.get("username", None)
            password = request.json.get("password", None)
            role = "doctor"

            if User.query.filter_by(username=username).first():
                return jsonify({"msg": "Doctor already exists"}), 409

            new_user = User(user_fullname=fullname, username=username, user_password=password, user_role=role)
            db.session.add(new_user)
            db.session.commit()

            specialization = request.json.get("specialization", None)
            department_id = request.json.get("department_id", None)

            doctor_profile = DoctorProfile(doctor_user_id=new_user.user_id, 
                                           doctor_specialization=specialization, 
                                           doctor_department_id=department_id, 
                                           doctor_availability={})
            
            db.session.add(doctor_profile)
            db.session.commit()
            generate_doctor_credentials.delay(fullname, username, password)
            return jsonify({"msg": "Doctor added successfully"}), 201
        
    def doctorSlots(date, start_time, end_time, slot_minutes=30):
        slots = []
        start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

        while start_dt < end_dt:
            slot_end = start_dt + timedelta(minutes=slot_minutes)
            if slot_end <= end_dt:
                slots.append({"start": start_dt.strftime("%H:%M"), "end": slot_end.strftime("%H:%M")})
            start_dt = slot_end
        return slots
        
    @app.route("/api/admin_dash/doctorPage/<int:id>", methods=['PUT'])
    @role_required("admin")
    def adminDashEditDoctor(id):
        doctor = User.query.filter_by(user_id=id, user_role='doctor').first()
        if not doctor:
            return jsonify({"msg": "Doctor not found"}), 404
        
        fullname = request.json.get("fullname", None)
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        specialization = request.json.get("specialization", None)
        department_id = request.json.get("department_id", None)
        if fullname:
            doctor.user_fullname = fullname
        if username:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user and existing_user.user_id != doctor.user_id:
                return jsonify({"msg": "Username already taken"}), 409
            doctor.username = username
        if password:
            doctor.user_password = password
        if doctor.doctor_profile:
            if specialization:
                doctor.doctor_profile.doctor_specialization = specialization
            if department_id:
                doctor.doctor_profile.doctor_department_id = department_id
        db.session.commit()
        return jsonify({"msg": "Doctor updated successfully"}), 200

    @app.route("/api/admin_dash/doctorPage/<int:id>/status", methods=['PATCH'])
    @role_required("admin")
    def adminDashDoctorStatus(id):
        doctor = User.query.filter_by(user_id=id, user_role="doctor").first()
        if not doctor:
            return jsonify({"msg": "Doctor not found"}), 404
        doctor.is_active = not doctor.is_active
        db.session.commit()
        return jsonify({"msg": "Doctor status updated"}), 200
    
    @app.route("/api/admin_dash/doctorPage/<int:id>/delete", methods=['DELETE'])
    @role_required("admin")
    def adminDashDoctorDelete(id):
        doctor = User.query.filter_by(user_id=id, user_role="doctor").first()
        if not doctor:
            return jsonify({"msg": "Doctor not found"}), 404
        db.session.delete(doctor)
        db.session.commit()
        return jsonify({"msg": "Doctor deleted successfully"}), 200

    @app.route("/api/admin_dash/deptPage", methods=['GET', 'POST'])
    @role_required("admin")
    def adminDashDept():
        departments = Department.query.all()
        if request.method == 'GET':
            return jsonify({
                "department": [
                    {
                        "id": dep.department_id,
                        "name": dep.department_name,
                        "description": dep.department_description,
                        "doctorCount": len(dep.doctors)
                    }
                    for dep in departments
                ]
            })
        else:
            dept_name = request.json.get("deptName", None)
            dept_description = request.json.get("deptDescription", None)
            if Department.query.filter_by(department_name=dept_name).first():
                return jsonify({"msg": "Department already exists"}), 409
            else:
                new_dept = Department(department_name=dept_name, department_description=dept_description)
                db.session.add(new_dept)
                db.session.commit()
                return jsonify({"msg": "Department added successfully"}), 201
            
    @app.route("/api/admin_dash/patientPage")
    @role_required("admin")
    def adminDashPatient():
        patients = User.query.filter_by(user_role='patient').all()
        return jsonify({
        "patients": [
            {
                "id": p.user_id,
                "fullname": p.user_fullname,
                "username": p.username,
                "age": p.patient_profile.patient_age if p.patient_profile else None,
                "gender": p.patient_profile.patient_gender if p.patient_profile else None,
                "contact": p.patient_profile.patient_contact if p.patient_profile else None,
                "status": p.is_active,
                "registered_on": p.user_created_at.strftime("%d-%m-%Y"),
                "appointments": len(p.appointments_as_patient)
            }
            for p in patients
            ]
        })

    @app.route("/api/admin_dash/patientPage/<int:id>/status", methods=['PATCH'])
    @role_required("admin")
    def adminDashPatientStatus(id):
        patient = User.query.filter_by(user_id=id, user_role="patient").first()
        if not patient:
            return jsonify({"msg": "Patient not found"}), 404
        patient.is_active = not patient.is_active
        db.session.commit()
        return jsonify({"msg": "Patient status updated"}), 200
    
    @app.route("/api/admin_dash/patientPage/<int:id>/delete", methods=['DELETE'])
    @role_required("admin")
    def adminDashPatientDelete(id):
        patient = User.query.filter_by(user_id=id, user_role="patient").first()
        if not patient:
            return jsonify({"msg": "Patient not found"}), 404
        db.session.delete(patient)
        db.session.commit()
        return jsonify({"msg": "Patient deleted successfully"}), 200
    
    @app.route("/api/admin_dash/appointmentPage", methods=["GET"])
    @role_required("admin")
    def adminDashAppointments():
        appointments = Appointment.query.order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc()).all()
        # appointments = Appointment.query.filter(Appointment.appointment_date >= date.today()).order_by(Appointment.appointment_date.asc(), Appointment.appointment_time.asc()).all()

        return jsonify({
            "appointments": [
                {
                    "appointment_id": appt.appointment_id,
                    "date": appt.appointment_date.strftime("%d-%m-%Y"),
                    "time": appt.appointment_time.strftime("%H:%M"),
                    "status": appt.appointment_status,

                    "patient": {
                        "id": appt.patient.user_id,
                        "name": appt.patient.user_fullname,
                        "contact": appt.patient.patient_profile.patient_contact if appt.patient.patient_profile else None,
                    },

                    "doctor": {
                        "id": appt.doctor.user_id,
                        "name": appt.doctor.user_fullname,
                        "department": (appt.doctor.doctor_profile.department.department_name
                                       if appt.doctor.doctor_profile and appt.doctor.doctor_profile.department
                                       else None)
                    },

                    "treatment": {
                        "diagnosis": appt.treatment.treatment_diagnosis if appt.treatment else None,
                        "prescription": appt.treatment.treatment_prescription if appt.treatment else None,
                        "notes": appt.treatment.treatment_notes if appt.treatment else None,
                    }
                }
                for appt in appointments
            ]
        })
    
    #------------------------------ USER DASHBOARD ------------------------------
    @app.route("/api/patient_dash/editProfile", methods=['PUT'])
    @role_required('patient')
    def patientDashProfile():
        userId = current_user.user_id
        usr = User.query.filter_by(user_id=userId, user_role='patient').first()
        if not usr:
            return jsonify({"msg": "Patient not found"}), 404
        fullname = request.json.get("fullname", None)
        age = request.json.get("age", None)
        phone_number = request.json.get("ph_number", None)
        gender = request.json.get("gender")

        if fullname:
            usr.user_fullname = fullname
        if not usr.patient_profile:
            usr.patient_profile = PatientProfile(patient_user_id=userId)
        if age:
            usr.patient_profile.patient_age = age
        if phone_number:
            usr.patient_profile.patient_contact = phone_number
        if gender:
            usr.patient_profile.patient_gender = gender
        db.session.commit()
        return jsonify({"msg": "Profile updated successfully"}), 200

    @app.route("/api/patient_dash/homePage", methods=['GET'])
    @role_required("patient")
    def patientDashHome():
        userId = current_user.user_id

        recentTreatment = Treatment.query.join(Appointment, Treatment.treatment_appointment_id == Appointment.appointment_id).filter(Appointment.patient_id == userId).order_by(Treatment.treatment_created_at.desc()).first()
        nextAppointment = Appointment.query.filter(Appointment.patient_id == userId, 
                                                   Appointment.appointment_status == "Booked", 
                                                   Appointment.appointment_date >= date.today()).order_by(Appointment.appointment_date.asc()).first()
        recent_appointments = (Appointment.query.filter(Appointment.patient_id == userId).order_by(Appointment.appointment_date.desc()).limit(5).all())

        return jsonify({
            "role": current_user.user_role,

            "recent_treatment": {
                "medicine": recentTreatment.treatment_prescription,
                "diagnosis": recentTreatment.treatment_diagnosis,
                "date": recentTreatment.treatment_created_at.strftime("%d-%m-%Y"),
                "doctor": recentTreatment.appointment.doctor.user_fullname,
            } if recentTreatment else None,

            "next_appointment": {
            "date": nextAppointment.appointment_date.strftime("%d-%m-%Y"),
            "doctor": nextAppointment.doctor.user_fullname,
            "status": nextAppointment.appointment_status,
            "department": (nextAppointment.doctor.doctor_profile.department.department_name)
            } if nextAppointment else None,

            "recent_appointments": [
                {
                    "appointment_id": appt.appointment_id,
                    "date": appt.appointment_date.strftime("%d-%m-%Y"),
                    "doctor": appt.doctor.user_fullname,
                    "status": appt.appointment_status,
                }
                for appt in recent_appointments]
        })
    
    @app.route("/api/patient_dash/deptPage", methods=['GET'])
    @role_required("patient")
    def patientDashDept():
        departments = Department.query.all()
        return jsonify({
            "department": [
                {
                    "id": dept.department_id,
                    "name": dept.department_name,
                    "description": dept.department_description,
                    "doctorCount": len(dept.doctors)
                }
                for dept in departments
            ]
        })
    
    @app.route("/api/patient_dash/doctorPage", methods=['GET', 'POST'])
    @role_required("patient")
    def patientDashDoctor():
        if request.method == 'GET':
            doctors = User.query.filter_by(user_role="doctor", is_active=True).all()
            doctor_list = []

            for d in doctors:
                availability = {}
                if d.doctor_profile and d.doctor_profile.doctor_availability:
                    for date_str, slots in d.doctor_profile.doctor_availability.items():
                        slot_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                        if slot_date < date.today():
                            continue
                        free_slots = []
                        for slot in slots:
                            appt = Appointment.query.filter_by(
                                doctor_id=d.user_id,
                                appointment_date=slot_date,
                                appointment_time=datetime.strptime(slot["start"], "%H:%M").time()
                            ).filter(Appointment.appointment_status == "Booked").first()
                            if not appt:
                                free_slots.append(slot)
                        availability[date_str] = free_slots

                doctor_list.append({
                    "id": d.user_id,
                    "fullname": d.user_fullname,
                    "specialization": d.doctor_profile.doctor_specialization if d.doctor_profile else None,
                    "department": d.doctor_profile.department.department_name if d.doctor_profile and d.doctor_profile.department else None,
                    "availability": availability
                })

            return jsonify({"doctors": doctor_list})
        else:
            doctor_id = request.json.get("doctor_id")
            appt_date = request.json.get("date")
            time = request.json.get("time")
            appointment_date = datetime.strptime(appt_date, "%Y-%m-%d").date()
            appointment_time = datetime.strptime(time, "%H:%M").time()

            if not doctor_id or not appt_date or not time:
                return jsonify({"msg": "Missing required fields"}), 400
            
            patient_id = current_user.user_id
            existing_appointment = Appointment.query.filter_by(doctor_id=doctor_id,
                                                               appointment_date=appointment_date,
                                                               appointment_time=appointment_time,
                                                               appointment_status="Booked").first()
            if existing_appointment:
                return jsonify({"msg": "Slot already Booked"}), 409
            
            new_appointment = Appointment(doctor_id=doctor_id,
                                          patient_id=patient_id,
                                          appointment_date=appointment_date,
                                          appointment_time=appointment_time,
                                          appointment_status="Booked")
            db.session.add(new_appointment)
            db.session.commit()
            return jsonify({"msg": "Appointment Booked Successfully!"}), 201
    
    @app.route("/api/patient_dash/apptPage", methods=['GET'])
    @role_required("patient")
    def patientDashAppt():
        user_id = current_user.user_id
        appointments = Appointment.query.filter_by(patient_id=user_id).order_by(Appointment.appointment_date.desc(), 
                                                                                Appointment.appointment_time.desc()).all()

        return jsonify({
        "appointments": [
            {
                "id": appt.appointment_id,
                "date": appt.appointment_date.strftime("%d-%m-%Y"),
                "time": appt.appointment_time.strftime("%H:%M"),
                "status": appt.appointment_status,
                "doctorName": appt.doctor.user_fullname,
                "specialization": (
                    appt.doctor.doctor_profile.doctor_specialization
                    if appt.doctor.doctor_profile else None
                ),
                "treatment": {
                    "diagnosis": appt.treatment.treatment_diagnosis if appt.treatment else None,
                    "prescription": appt.treatment.treatment_prescription if appt.treatment else None,
                    "notes": appt.treatment.treatment_notes if appt.treatment else None
                } if appt.appointment_status == "Completed" else None
            }
            for appt in appointments
        ]
    })
    
    @app.route("/api/appt/cancel/<int:appt_id>", methods=['PUT'])
    @jwt_required()
    def cancelAppointment(appt_id):
        user_id = current_user.user_id
        appt = Appointment.query.filter_by(appointment_id=appt_id).first()

        if not appt:
            return jsonify({"msg": "Appointment not found"}), 404

        if appt.appointment_status in ["Completed", "Cancelled"]:
            return jsonify({"msg": "Failed to cancel appointment"}), 400

        if current_user.user_role == "patient" and appt.patient_id != user_id:
            return jsonify({"msg": "Unauthorized"}), 403
        
        if current_user.user_role == "doctor" and appt.doctor_id != user_id:
            return jsonify({"msg": "Unauthorized"}), 403

        appt.appointment_status = "Cancelled"
        db.session.commit()
        return jsonify({"msg": "Appointment cancelled successfully"}), 200


    #------------------------------ DOCTOR DASHBOARD ------------------------------
    @app.route("/api/doctor_dash/homePage", methods=['GET', 'POST'])
    @role_required("doctor")
    def doctorDashHome():
        doctor_id = current_user.user_id
        if request.method == 'GET':
            today = date.today()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            today_appointments = Appointment.query.filter(Appointment.doctor_id == doctor_id,
                                                        Appointment.appointment_date == today,
                                                        Appointment.appointment_status == "Booked").count()
            upcoming_appointments = Appointment.query.filter(Appointment.doctor_id == doctor_id,
                                                            Appointment.appointment_date > today,
                                                            Appointment.appointment_status == "Booked").count()
            completed_appointments = Appointment.query.filter(Appointment.doctor_id == doctor_id,
                                                            Appointment.appointment_status == "Completed").count()

            today_start = datetime.combine(today, time.min)
            today_end = datetime.combine(today, time.max)
            treatments_today = Treatment.query.join(Appointment).filter(Appointment.doctor_id == doctor_id, 
                                                                        Treatment.treatment_created_at >= today_start, 
                                                                        Treatment.treatment_created_at <= today_end).count()
            
            week_start = datetime.combine(start_of_week, time.min)
            week_end = datetime.combine(end_of_week, time.max)
            treatments_week = Treatment.query.join(Appointment).filter(Appointment.doctor_id == doctor_id, 
                                                                    Treatment.treatment_created_at >= week_start, 
                                                                    Treatment.treatment_created_at <= week_end).count()
            treatments_total = Treatment.query.join(Appointment).filter(Appointment.doctor_id == doctor_id).count()

            recent_appointments = (Appointment.query.filter(Appointment.doctor_id == doctor_id).order_by(Appointment.appointment_date.desc(), 
                                                                                                        Appointment.appointment_time.desc()).limit(5).all())

            return jsonify({
                "appointments": {
                    "today": today_appointments,
                    "upcoming": upcoming_appointments,
                    "completed": completed_appointments
                },
                "treatments": {
                    "today": treatments_today,
                    "week": treatments_week,
                    "total": treatments_total
                },
                "recent_patients": [
                {
                    "appointment_id": appt.appointment_id,
                    "date": appt.appointment_date.strftime("%d-%m-%Y"),
                    "time": appt.appointment_time.strftime("%H:%M"),
                    "status": appt.appointment_status,
                    "patientName": appt.patient.user_fullname
                }
                for appt in recent_appointments
                ]
            })
        else:
            selected_dates = request.json.get("selected_dates", [])
            shift_start = request.json.get("shift_start")
            shift_end = request.json.get("shift_end")

            if not selected_dates or not shift_start or not shift_end:
                return jsonify({"msg": "Missing availability details"}), 400

            availability = {}
            for d in selected_dates:
                availability[d] = doctorSlots(d, shift_start, shift_end)

            doctor_profile = DoctorProfile.query.filter_by(doctor_user_id=doctor_id).first()
            if not doctor_profile:
                return jsonify({"msg": "Doctor profile not found"}), 404

            doctor_profile.doctor_availability = availability
            db.session.commit()
            return jsonify({"msg": "Availability saved successfully"}), 200
    
    @app.route("/api/doctor_dash/patientPage", methods=['GET'])
    @role_required("doctor")
    def doctorDashPatient():
        doctor_id = current_user.user_id
        appointments = Appointment.query.filter_by(doctor_id=doctor_id, appointment_status='Completed').order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc()).all()

        return jsonify({
            "patients": [
                {
                    "patient_id": appt.patient.user_id,
                    "fullname": appt.patient.user_fullname,
                    "age": appt.patient.patient_profile.patient_age if appt.patient.patient_profile else None,
                    "gender": appt.patient.patient_profile.patient_gender if appt.patient.patient_profile else None,
                    "phone": appt.patient.patient_profile.patient_contact if appt.patient.patient_profile else None,
                    "latest_appointment": appt.appointment_date.strftime("%d-%m-%Y"),
                    "status": appt.appointment_status
                }
                for appt in appointments
            ]
        })
    
    @app.route("/api/doctor_dash/apptPage", methods=['GET'])
    @role_required("doctor")
    def doctorDashAppt():
        doctor_id = current_user.user_id
        appointments = Appointment.query.filter_by(doctor_id=doctor_id).order_by(Appointment.appointment_date.desc(), 
                                                                                 Appointment.appointment_time.desc()).all()

        return jsonify({
            "appointments": [
                {
                    "id": appt.appointment_id,
                    "date": appt.appointment_date.strftime("%d-%m-%Y"),
                    "time": appt.appointment_time.strftime("%H:%M"),
                    "status": appt.appointment_status,
                    "patientName": appt.patient.user_fullname,
                    "age": appt.patient.patient_profile.patient_age if appt.patient.patient_profile else None,
                    "gender": appt.patient.patient_profile.patient_gender if appt.patient.patient_profile else None,
                    "contact": appt.patient.patient_profile.patient_contact if appt.patient.patient_profile else None,
                    "treatment": {
                        "diagnosis": appt.treatment.treatment_diagnosis if appt.treatment else None,
                        "prescription": appt.treatment.treatment_prescription if appt.treatment else None,
                        "notes": appt.treatment.treatment_notes if appt.treatment else None
                    } if appt.appointment_status == "Completed" else None
                }
                for appt in appointments
            ]
        })
    
    @app.route("/api/doctor_dash/apptPage/<int:appt_id>/treatment", methods=['POST'])
    @role_required("doctor")
    def doctorDashAddTreatment(appt_id):
        doctor_id = current_user.user_id
        appt = Appointment.query.filter_by(appointment_id=appt_id, doctor_id=doctor_id).first()

        if not appt:
            return jsonify({"msg": "Appointment not found"}), 404

        if appt.appointment_status != "Booked":
            return jsonify({"msg": "Treatment can only be added to booked appointments"}), 400

        diagnosis = request.json.get("diagnosis", None)
        prescription = request.json.get("prescription", None)
        notes = request.json.get("notes", None)

        treatment = Treatment(treatment_appointment_id=appt.appointment_id,
                              treatment_diagnosis=diagnosis,
                              treatment_prescription=prescription,
                              treatment_notes=notes)

        appt.appointment_status = "Completed"
        db.session.add(treatment)
        db.session.commit()
        return jsonify({"msg": "Treatment added successfully"}), 201
    
    @app.route("/api/doctor_dash/chart")
    @role_required("doctor")
    def doctorDashChart():
        doctor_id = current_user.user_id
        appt_status = ["Booked", "Completed", "Cancelled"]
        chart_data = []
        for status in appt_status:
            count = Appointment.query.filter_by(doctor_id=doctor_id, appointment_status=status).count()
            chart_data.append({"status": status, "count": count})
        return jsonify({"appointmentStatus": chart_data})
    
    #------------------------------ BACKEND JOBS ------------------------------
    @app.route("/api/patient_export_csv/<int:user_id>")
    def patientDashExportCsv(user_id):
        res = export_csv_report.delay(user_id)
        return {
            "task_id": res.id,
            "message": f"Export CSV job triggered for user {user_id}"
        }
    @app.route('/api/csv_result/<task_id>')
    def csv_result(task_id):
        res = AsyncResult(task_id)
        if not res.ready():
            return {"status":"Pending"}
        return send_from_directory('static', res.result)
    
    @app.route("/api/send_email")
    def send_email():
        res = monthly_doctor_report.delay()
        return {"message": "Monthly Doctor Report task started!"}
    @app.route("/api/daily_reminders")
    def daily_reminders_trigger():
        res = generate_msg_patient.delay()
        return {
            "task_id": res.id,
            "message": "Daily reminder job triggered!",
            "result": res.result
        }