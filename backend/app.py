from flask import Flask
from application.models import db, User
from application.routes import routesRegistration
from application.security import jwt
from flask_cors import CORS
from application.celery_init import celery_init_app
from celery.schedules import crontab
from application.tasks import generate_msg_patient, monthly_doctor_report
from application.cache import cache

from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config.update({
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_HOST": "localhost",
    "CACHE_REDIS_PORT": 6379,
    "CACHE_DEFAULT_TIMEOUT": 5
})

db.init_app(app)
jwt.init_app(app)
cache.init_app(app)

celery = celery_init_app(app)
celery.autodiscover_tasks()
@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/2'), monthly_doctor_report.s())
    # sender.add_periodic_task(crontab(day_of_month=1, hour=9, minute=0), monthly_doctor_report.s())
    sender.add_periodic_task(crontab(minute='*/2'), generate_msg_patient.s())
    # sender.add_periodic_task(crontab(hour=9, minute=0), generate_msg_patient.s())

with app.app_context():
    db.create_all()
    if not User.query.filter_by(user_role="admin").first():
        admin=User(username="admin@medixhub.com",
                   user_password=os.getenv("ADMIN_PASSWORD"),
                   user_fullname='Ripusudan Jha',
                   user_role="admin")
        db.session.add(admin)
        db.session.commit()

routesRegistration(app)

if __name__ == "__main__":
    app.run()