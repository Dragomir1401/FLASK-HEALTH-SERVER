"""This module contains the JobMaintainer class"""

class JobMaintainer:
    """Class to maintain the status of jobs"""
    def __init__(self):
        """Initialize the JobMaintainer class"""
        self.running_jobs = set()
        self.done_jobs = set()

    def is_job_running(self, job_id):
        """Check if a job with the given job_id is running"""
        return job_id in self.running_jobs

    def is_job_done(self, job_id):
        """Check if a job with the given job_id is done"""
        return job_id in self.done_jobs

    def finish_job(self, job_id):
        """Finish a job with the given job_id"""
        self.running_jobs.remove(job_id)
        self.done_jobs.add(job_id)

    def start_job(self, job_id):
        """Start a job with the given job_id"""
        self.running_jobs.add(job_id)
