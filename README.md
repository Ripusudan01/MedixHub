# MedixHub – Hospital Management System

A full-stack **Hospital Management System** for managing patients, doctors, appointments, and treatment records with role-based access.

---

## Features

* Role-Based Authentication & Authorization
* Admin, Doctor & Patient Management
* Doctor Availability Management
* Appointment Booking & Cancellation
* Appointment Conflict Prevention
* Patient Treatment History
* Diagnosis & Prescription Management
* Automated Appointment Reminders
* Monthly Doctor Activity Reports
* Asynchronous CSV Export
* Redis Caching
* Celery Background Jobs

---

## Tech Stack

* **Frontend:** Vue.js, Bootstrap
* **Backend:** Flask
* **Database:** SQLite
* **ORM:** SQLAlchemy
* **Caching:** Redis
* **Background Jobs:** Celery
* **Email:** MailHog

---

## Roles & Permissions

| Role        | Permissions                                                |
| ----------- | ---------------------------------------------------------- |
| **Admin**   | Manage doctors, patients & appointments                    |
| **Doctor**  | Manage availability, appointments & treatments             |
| **Patient** | Search doctors, book appointments & view treatment history |

---

## Project Setup

> The following commands were used to run the application on **Ubuntu/Linux**.

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

### MailHog

```bash
mailhog
```

### Redis

```bash
redis-cli ping
redis-server
```

### Celery Worker

```bash
cd backend
source venv/bin/activate
celery -A app.celery worker --loglevel=info
```

### Celery Beat

```bash
cd backend
source venv/bin/activate
celery -A app.celery beat --loglevel=info
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```
