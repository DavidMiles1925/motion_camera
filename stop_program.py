######################################################################
######################################################################
#####                                                            #####
#####                        STOP PROGRAM                        #####
#####                                                            #####
#####    This script is to stop the program after accessing      #####
#####    the Raspberry Pi via SSH. Since it is running in the    #####
#####    background, CTRL-C does not work.                       #####
#####                                                            #####
######################################################################
######################################################################


from config import LOGGING_ENABLED, CONSOLE_OUTPUT_ON
from logger import write_to_log

import subprocess
import os

filename = "motion.py"

def stop_motion_program():
    try:
        command = f"ps aux | grep '{filename}' | grep -v grep"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = process.communicate()

        if output:
            lines = output.decode().split('\n')
            for line in lines:
                if f'{filename}' in line:
                    console_and_log(f"The program was stopped via SSH connection. Process ('{filename}') with PID {pid}")
                    # Extract the PID from the output
                    pid = int(line.split()[1])
                    # Stop the process using the PID
                    os.system(f"sudo kill -TERM {pid}")
                    print(f"Process with PID {pid}  has been stopped.")
                    return True  # Exit the function after stopping the process
            print(f"No process with '{filename}' found.")
            return False  # No process found to stop
        else:
            print(f"No output received. Check if '{filename}' process is running.")
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


# Example usage
stop_motion_program()