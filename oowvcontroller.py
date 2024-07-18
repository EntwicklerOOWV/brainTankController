import RPi.GPIO as GPIO
import threading
import sys
import datetime
import os
import time
import logging

from modules.database import db_init
from modules.endpoints import run_flask_app
from modules.core import default_process, drain_process

# Custom print function with timestamp and log directory
def dated_output(stream, log_directory, *args, **kwargs):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = " ".join(map(str, args))
    log_path = f"{log_directory}/{stream}_output.log"
    
    if message.strip():  # Skip if the message is blank
        with open(log_path, "a") as log_file:
            print(f"[{timestamp}] {message}", file=log_file, **kwargs)

def monitor_threads(target_functions, logger):
    threads = []
    thread_names = [target.__name__ for target in target_functions]
    
    for i, target in enumerate(target_functions):
        thread = threading.Thread(target=target)
        thread.start()
        threads.append(thread)
        logger.info(f"{thread_names[i]} has been started.")
        
    while True:
        for i, thread in enumerate(threads):
            if not thread.is_alive():
                logger.warning(f"{thread_names[i]} is not alive, restarting...")
                new_thread = threading.Thread(target=target_functions[i])
                new_thread.start()
                threads[i] = new_thread
                logger.info(f"{thread_names[i]} has been restarted.")
        time.sleep(2)


if __name__ == '__main__':
    
    try:
        # Setup logging
        logging.basicConfig(filename='monitor.log', level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')
        logger = logging.getLogger()

        # Initialize Database
        db_init()

        # List of target functions for the threads
        target_functions = [run_flask_app, default_process, drain_process]

        # Start the monitor thread
        monitor_thread = threading.Thread(target=monitor_threads, args=(target_functions, logger))
        monitor_thread.start()


    except KeyboardInterrupt:
        GPIO.cleanup()