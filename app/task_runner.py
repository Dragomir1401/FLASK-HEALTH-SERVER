import os
from queue import Queue
from threading import Thread, Event
import time
from concurrent.futures import ThreadPoolExecutor

class Job:
    def __init__(self, job_id):
        self.job_id = job_id

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        #   * implement the ThreadPool as a singleton by hand
        if 'TP_NUM_OF_THREADS' in os.environ:
            self.num_threads = int(os.environ['TP_NUM_OF_THREADS'])
        else:
            self.num_threads = os.cpu_count()

        # Initialize the ThreadPoolExecutor with the number of threads
        self.executor = ThreadPoolExecutor(max_workers=self.num_threads)

        # Initialize the queue
        self.queue = Queue()

    def __submit__(self, execute_job, params, job_id):
        # Submit the job to the ThreadPoolExecutor
        self.executor.submit(execute_job, params, job_id)

    def __shutdown__(self):
        # Shutdown the ThreadPool
        self.executor.shutdown()

    def job_is_running(self, job_id):
        # Check the status of a job
        # Return True if the job is still running
        # Return False if the job is done
        if self.executor._futures[job_id].running():
            return True
        return False     
