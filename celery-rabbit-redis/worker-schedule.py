import os
from datetime import datetime

from celery import Celery
from celery.schedules import crontab, schedule

app = Celery(
    "ticker",
    broker=os.environ.get("CELERY_BROKER_URL"),
    backend=os.environ.get("CELERY_BACKEND_URL"),
)

OUTPUT_PATH = "/data/timestamp.txt"

@app.task
def write_timestamp():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
        f.write(datetime.now().isoformat() + "\n")


#Defining a schedule every 10 seconds
app.conf.beat_schedule = {
    "timestamp_writer": {
        "task": "worker-schedule.write_timestamp",
        "schedule": schedule(5)
    }
}

#Defining a cron job to run every day at 18:44
# app.conf.beat_schedule = {
#     "nightly-job": {
#         "task": "worker-schedule.write_timestamp",
#         "schedule": crontab(hour=18, minute=54),
#     }
# }


app.conf.timezone = 'Europe/Warsaw'
app.conf.enable_utc = True