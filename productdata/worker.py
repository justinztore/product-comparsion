from celery import Celery

app = Celery(
    "task",
    # execution successful for the task included in tasks.py
    include=["productdata.tasks"],
    broker="pyamqp://worker:worker@localhost:5672/"
)