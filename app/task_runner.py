"""This module contains the ThreadPool class that is responsible for managing the thread pool. """
import os
from concurrent.futures import ThreadPoolExecutor

def _handle_job_done(job_id, future):
    """Handle the completion of a job."""
    # Check for exception in the executed job
    try:
        future.result()  # This will re-raise any exception caught during job execution
        # Log the job completion
    except RuntimeError as exception:
        # Log the exception
        print(f"Error during execution of job {job_id}: {str(exception)}")

class ThreadPool:
    """Class to manage the thread pool."""
    def __init__(self):
        """Initialize the ThreadPool class."""
        if 'TP_NUM_OF_THREADS' in os.environ:
            self.num_threads = int(os.environ['TP_NUM_OF_THREADS'])
        else:
            self.num_threads = os.cpu_count() or 1  # Ensure at least 1 thread

        self.executor = ThreadPoolExecutor(max_workers=self.num_threads)

    def __submit__(self, execute_job, params, job_id):
        """Submit a job to the thread pool."""
        try:
            future = self.executor.submit(execute_job, params, job_id)

            # Add a callback to handle job completion
            future.add_done_callback(lambda f: _handle_job_done(job_id, f))
        except RuntimeError as exception:
            # Log the exception
            print(f"Error submitting job {job_id}: {str(exception)}")

    def __shutdown__(self):
        """Shut down the thread pool."""
        self.executor.shutdown(wait=True)
