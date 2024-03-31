
class JobMaintainer:
    def __init__(self):
        self.running_jobs = set()
        self.done_jobs = set()

    def is_job_running(self, job_id):
        return job_id in self.running_jobs
    
    def is_job_done(self, job_id):
        return job_id in self.done_jobs
    
    def finish_job(self, job_id):
        self.running_jobs.remove(job_id)
        self.done_jobs.add(job_id)

    def start_job(self, job_id):
        self.running_jobs.add(job_id)