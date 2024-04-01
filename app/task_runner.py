import os
from queue import Queue
from threading import Thread, Event
from concurrent.futures import ThreadPoolExecutor
from app import logger

class ThreadPool:
    def __init__(self):
        if 'TP_NUM_OF_THREADS' in os.environ:
            self.num_threads = int(os.environ['TP_NUM_OF_THREADS'])
        else:
            self.num_threads = os.cpu_count() or 1  # Ensure at least 1 thread
        
        self.executor = ThreadPoolExecutor(max_workers=self.num_threads)

    def __submit__(self, execute_job, params, job_id):
        try:
            future = self.executor.submit(execute_job, params, job_id)
            
            # Add a callback to handle job completion
            future.add_done_callback(lambda f: self._handle_job_done(job_id, f))
        except Exception as e:
            # Log the exception
            logger.error(f"Error submitting job {job_id}: {str(e)}")

    def _handle_job_done(self, job_id, future):
        # Check for exception in the executed job
        try:
            result = future.result()  # This will re-raise any exception caught during job execution
            # Log the job completion
        except Exception as e:
            # Log the exception
            logger.error(f"Error during execution of job {job_id}: {str(e)}")

    def __shutdown__(self):
        self.executor.shutdown(wait=True)
