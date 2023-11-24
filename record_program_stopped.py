from config import LOGGING_ENABLED, CONSOLE_OUTPUT_ON
from logger import write_to_log

# Function for logging and printing to console. Can be easily enabled/diabled through the console
def console_and_log(message=""):
    if CONSOLE_OUTPUT_ON:
        print(message)

    if LOGGING_ENABLED:
        write_to_log(message)

console_and_log("The program was stopped via SSH connection.")