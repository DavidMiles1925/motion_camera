from config import LOGGING_ENABLED, CONSOLE_OUTPUT_ON
from logger import write_to_log

import subprocess
import os

def stop_motion_program():
    try:
        command = "ps aux | grep 'motion.py' | grep -v grep"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = process.communicate()

        if output:
            lines = output.decode().split('\n')
            for line in lines:
                if 'motion.py' in line:
                    # Extract the PID from the output
                    pid = int(line.split()[1])
                    # Stop the process using the PID
                    os.kill(pid, 9)
                    print(f"Process with PID {pid} ('motion.py') has been stopped.")
                    return True  # Exit the function after stopping the process
            print("No process with 'motion.py' found.")
            return False  # No process found to stop
        else:
            print("No output received. Check if 'motion.py' process is running.")
            return False  # No output received
    except Exception as e:
        print(f"Error occurred: {e}")
        return False  # Error occurred while trying to stop the process


# Function for logging and printing to console. Can be easily enabled/diabled through the console
def console_and_log(message=""):
    if CONSOLE_OUTPUT_ON:
        print(message)

    if LOGGING_ENABLED:
        write_to_log(message)

console_and_log("The program was stopped via SSH connection.")

# Example usage
stop_motion_program()