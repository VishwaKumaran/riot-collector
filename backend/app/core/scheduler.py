from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class Scheduler:
    def __init__(self) -> None:
        self.__scheduler = AsyncIOScheduler()

    def start(self) -> None:
        self.__scheduler.start()

    def shutdown(self) -> None:
        self.__scheduler.shutdown()

    def add_job(self, func, trigger: CronTrigger, job_id: str) -> str:
        if not self.__scheduler.get_job(job_id):
            self.__scheduler.add_job(func, trigger, id=job_id)
            return f"Job {job_id} successfully created."
        return f"Job {job_id} already exists."

    def get_job(self, job_id: str):
        return self.__scheduler.get_job(job_id)
