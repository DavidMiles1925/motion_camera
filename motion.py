from datetime import datetime
import RPi.GPIO as GPIO
import os
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
from time import sleep

# Import constants from config.py
from config import FILENAME_PREFIX, SAVE_DIRECTORY_PATH, DIRECTORY_NAME_PREFIX, LED_INDICATORS

# Set up pins for LED indicators
POWER_LED_PIN = 20
RECORD_LED_PIN = 16

# Set up pin for on/off switch. 
# THE SWITCH ONLY WORKS WHEN THE PROGRAM IS ALREADY RUNNING
SWITCH_PIN = 26

# Set up pin for motion detector
MOTION_PIN = 25

##################################################
##################################################
#####                                        #####
#####            SET UP CAMERA               #####
#####                                        #####
##################################################
##################################################


picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
encoder = H264Encoder(bitrate=1000000)


##################################################
##################################################
#####                                        #####
#####         SUPPORTING FUNCTIONS           #####
#####                                        #####
##################################################
##################################################


# Sets up pin configuration
def setup_pins():
    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)

    GPIO.setup(POWER_LED_PIN, GPIO.OUT)
    GPIO.output(POWER_LED_PIN, GPIO.LOW)

    GPIO.setup(RECORD_LED_PIN, GPIO.OUT)
    GPIO.output(RECORD_LED_PIN, GPIO.LOW)

    GPIO.setup(SWITCH_PIN, GPIO.IN)

    GPIO.setup(MOTION_PIN, GPIO.IN)


# Used to turn a pin on or off.
#   Note that the `status` parameter is optional and only 
#   needs to be passed for a `False` value
def pin(pin, status=True):
    if LED_INDICATORS == True:
        if status == False:
            GPIO.output(pin, GPIO.LOW)
        else:
            GPIO.output(pin, GPIO.HIGH)


# Sets up the folder where the videos will be stored.
def set_up_folder():
    folder_time = datetime.now().strftime("%m.%d.%Y")

    path_str = f"{SAVE_DIRECTORY_PATH}{DIRECTORY_NAME_PREFIX}{folder_time}"
    
    if os.path.isdir(path_str) ==  False:
        os.mkdir(path_str)

    os.chdir(path_str)


# Adds zeros to the video number in the filename.
#   - This was done to ensure videos stayed in chronological
#     order, even when displayed alphabetically.
def add_zeros_to_number(num):
    num_str = str(num)

    num_zeros = 6 - len(num_str)

    if num_zeros > 0:
        return '0' * num_zeros + num_str
    else:
        return num_str
    

# The sequence for cleaning up and stopping the program.
def stop_program():
    print("\n\n")

    print("Cleaning up GPIO...")
    GPIO.cleanup()

    print("Done")
    exit()


##################################################
##################################################
#####                                        #####
#####            CAMERA FUNCTION             #####
#####                                        #####
##################################################
##################################################


def run_camera():
    global video_counter

    if GPIO.input(MOTION_PIN):
        print("Camera Running")
        pin(RECORD_LED_PIN)

        timestamp = datetime.now().strftime("%H.%M")

        video_counter_str = add_zeros_to_number(video_counter)

        output = f"{FILENAME_PREFIX}-{video_counter_str}-[{timestamp}].h264"

        picam2.start_recording(encoder, output)
        sleep(15)

        # If there is still motion, continue recording.
        while GPIO.input(MOTION_PIN):
            sleep(15)
        
        picam2.stop_recording()

        video_counter = video_counter + 1

        print(f"Recorded {output}")
        pin(RECORD_LED_PIN, False)


##################################################
##################################################
#####                                        #####
#####             MAIN FUNCTION              #####
#####                                        #####
##################################################
##################################################


if __name__ == "__main__":
    try:
        video_counter = 0

        setup_pins()

        set_up_folder()

        # Checks to see if the switch is in the `ON` position.
        #   - If it is, the `run_camera` funtion will be triggered.
        while True:
            pin(POWER_LED_PIN)

            is_recording = GPIO.input(SWITCH_PIN)

            if is_recording == False:
                run_camera()
            else:
                pin(RECORD_LED_PIN, False)


    except KeyboardInterrupt:
        stop_program()

    except Exception as e:
        print("\n\nThe program stopped unexpectedly.")
        print(e)
        print(e.args)