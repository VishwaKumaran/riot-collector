from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from fastapi import FastAPI
from firebase_admin import firestore_async

from app.core.config import settings
from app.core.job_scripts.patch_release import patch_release
from app.db import firebase
from app.routers.main import api_router
from app.scheduler import scheduler

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1}/openai.json",
)

firebase.db = firestore_async.client()

app.include_router(api_router, prefix=settings.API_V1)

scheduler.start()
if not scheduler.get_job(settings.JOB_RELEASE_PATCH):
    scheduler.add_job(patch_release, CronTrigger(day='*', start_date=datetime.now()), settings.JOB_RELEASE_PATCH)


@app.get('/')
def root():
    return 'Riot-Collector successfully initialized.'
