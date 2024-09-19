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

    def list_jobs(self):
        return [{
            'id': job.id,
            'name': job.name,
            'func': job.func_ref,
            'next_run_time': str(job.next_run_time),
            'trigger': str(job.trigger),
            'args': job.args,
            'kwargs': job.kwargs,
        } for job in self.__scheduler.get_jobs()]
