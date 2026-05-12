from celery import shared_task 
import csv
from jinja2 import Template
from .mail import send_email
from .models import *
from datetime import datetime, timedelta
import requests

@shared_task(ignore_results=False, name="download_csv_report")
def export_csv_report(userId):
    usr_details = User.query.filter_by(user_id=userId, user_role="patient").first()
    if not usr_details:
        return f"No patient found"

    csv_file_name = f"treatments_{userId}_{datetime.now().strftime('%Y%m%d')}.csv"
    appointments = Appointment.query.filter_by(patient_id=userId).join(Treatment).all()

    with open(f'static/{csv_file_name}', 'w', newline="") as csvfile:
        card_csv = csv.writer(csvfile, delimiter=',')
        card_csv.writerow(['#', 'Patient Name', 'Doctor Name', 'Appointment Date', 'Status', 'Diagnosis', 'Treatment', 'Notes'])
        sr_no = 1

        if not appointments:
            card_csv.writerow([sr_no, usr_details.user_fullname, "NA", "NA", "NA", "NA", "NA"])
        else:
            for appt in appointments:
                treatment = appt.treatment
                doctor_name = appt.doctor.user_fullname if appt.doctor else "NA"
                appointment_date = appt.appointment_date.strftime("%Y-%m-%d") if appt.appointment_date else "NA"
                appointment_status = appt.appointment_status if appt.appointment_status else "NA"

                card_csv.writerow([
                    sr_no,
                    usr_details.user_fullname,
                    doctor_name,
                    appointment_date,
                    appointment_status,
                    getattr(treatment, "treatment_diagnosis", "NA"),
                    getattr(treatment, "treatment_prescription", "NA"),
                    getattr(treatment, "treatment_notes", "NA"),
                ])
                sr_no += 1
    return csv_file_name

@shared_task(ignore_results=False, name="monthly_doctor_report")
def monthly_doctor_report():
    today = datetime.utcnow()
    first_day = today.replace(day=1)
    last_month = first_day - timedelta(days=1)
    month_start = last_month.replace(day=1)
    month_end = last_month.replace(day=last_month.day)

    doctors = User.query.filter_by(user_role="doctor", is_active=True).all()
    for doctor in doctors:
        appointments = Appointment.query.filter(Appointment.doctor_id == doctor.user_id).join(Treatment).filter(Treatment.treatment_created_at >= month_start,
                                                                                                                Treatment.treatment_created_at <= month_end).all()

        doctor_data = []
        for appt in appointments:
            doctor_info = {
                "patient_name": appt.patient.user_fullname if appt.patient else "NA",
                "date": appt.treatment.treatment_created_at.strftime("%Y-%m-%d") if appt.treatment and appt.treatment.treatment_created_at else "NA",
                "diagnosis": appt.treatment.treatment_diagnosis if appt.treatment else "",
                "prescription": appt.treatment.treatment_prescription if appt.treatment else "",
                "notes": appt.treatment.treatment_notes if appt.treatment else ""
            }
            doctor_data.append(doctor_info)

        mail_template = """
        <h3>Dear {{ doctor_name }},</h3>
        <p>Here is your monthly activity report for <strong>{{ month_name }}</strong>.</p>
        <p>Below are the details of your appointments and treatments provided.</p>

        <table border="1" cellspacing="0" cellpadding="6">
            <tr>
                <th>Patient Name</th>
                <th>Treatment Date</th>
                <th>Diagnosis</th>
                <th>Prescription</th>
                <th>Notes</th>
            </tr>
            {% for d in details %}
            <tr>
                <td>{{ d.patient_name }}</td>
                <td>{{ d.date }}</td>
                <td>{{ d.diagnosis }}</td>
                <td>{{ d.prescription }}</td>
                <td>{{ d.notes }}</td>
            </tr>
            {% endfor %}
        </table>

        <p><br>Regards,<br>
        MedixHub Team</p>
        """
        if not doctor_data:
            continue
        message = Template(mail_template).render(doctor_name=doctor.user_fullname,
                                                 month_name=month_start.strftime("%B %Y"),
                                                 details=doctor_data)

        send_email(to_address=doctor.username,
                   subject=f"Monthly Activity Report - {month_start.strftime('%B %Y')}",
                   message=message)

    return "Monthly doctor reports sent successfully."

@shared_task(ignore_results=False, name="daily_reminders")
def generate_msg_patient():
    today = datetime.utcnow().date()
    appointments = Appointment.query.filter(Appointment.appointment_date == today, Appointment.appointment_status == 'Booked').all()

    if not appointments:
        return "No appointments for today."
    for appt in appointments:
        patient_name = appt.patient.user_fullname if appt.patient else "Patient"
        doctor_name = appt.doctor.user_fullname if appt.doctor else "Doctor"
        appt_time = appt.appointment_time.strftime("%I:%M %p") if appt.appointment_time else "NA"

        msg = (
            f"Hi {patient_name}, this is a reminder for your appointment today "
            f"with {doctor_name} at {appt_time}. "
            f"Please visit the hospital on time.")
        requests.post("https://chat.googleapis.com/v1/spaces/AAQAjKAP_v0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=h-uC-_HSSgEp8l-K8GjUHNcGWdbT5La7nYgJctzmBw4", json={"text": msg})
    return "Daily reminders sent successfully."

@shared_task(ignore_results=True, name="doctor_credentials")
def generate_doctor_credentials(fullname, username, password):
    msg = (
        f"*Hi {fullname}, welcome to MedixHub!*\n\n"
        f"Here are your login credentials:\n"
        f"- Username: `{username}`\n"
        f"- Password: `{password}`\n"
        f"Login here: http://127.0.0.1:5173")
    requests.post("https://chat.googleapis.com/v1/spaces/AAQAjKAP_v0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=h-uC-_HSSgEp8l-K8GjUHNcGWdbT5La7nYgJctzmBw4", json={"text": msg})
    return "Docotor credentials sent successfully."