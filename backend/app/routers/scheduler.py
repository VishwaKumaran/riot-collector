from fastapi import APIRouter

from app.scheduler import scheduler

router = APIRouter()


@router.get("/jobs")
def get_jobs():
    return scheduler.list_jobs()
