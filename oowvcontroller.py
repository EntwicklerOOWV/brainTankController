import RPi.GPIO as GPIO
import threading
import sys
import datetime

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

if __name__ == '__main__':
    
    try:
        # Define your log directory
        log_directory = "/home/quantumfrog/oowv-controller/logs"

        # Replace the standard print function with the custom_print function
        sys.stdout.write = lambda message: dated_output("stdout", log_directory, message)
        sys.stderr.write = lambda message: dated_output("stderr", log_directory, message)

        # Initialize Database
        db_init()

        # Start the Flask App in a new thread
        flask_thread = threading.Thread(target=run_flask_app)
        flask_thread.start()

        # Start the default cycle in a new thread
        default_thread = threading.Thread(target=default_process)
        default_thread.start()

        # Start the drain process in a new thread
        drain_thread = threading.Thread(target=drain_process)
        drain_thread.start()

    except KeyboardInterrupt:
        GPIO.cleanup()