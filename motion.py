from datetime import datetime
import RPi.GPIO as GPIO
import os
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
from time import sleep

from config import FILENAME_PREFIX, SAVE_DIRECTORY_PATH, DIRECTORY_NAME_PREFIX, LED_INDICATORS

POWER_LED_PIN = 20
RECORD_LED_PIN = 16

SWITCH_PIN = 26

MOTION_PIN = 25

DELAY_TIME = 3

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
encoder = H264Encoder(bitrate=1000000)

def setup_pins():
    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)

    GPIO.setup(POWER_LED_PIN, GPIO.OUT)
    GPIO.output(POWER_LED_PIN, GPIO.LOW)

    GPIO.setup(RECORD_LED_PIN, GPIO.OUT)
    GPIO.output(RECORD_LED_PIN, GPIO.LOW)

    GPIO.setup(SWITCH_PIN, GPIO.IN)

    GPIO.setup(MOTION_PIN, GPIO.IN)


def pin(pin, status=True):
    if LED_INDICATORS == True:
        if status == False:
            GPIO.output(pin, GPIO.LOW)
        else:
            GPIO.output(pin, GPIO.HIGH)


def set_up_folder():
    folder_time = datetime.now().strftime("%m.%d.%Y")

    path_str = f"{SAVE_DIRECTORY_PATH}{DIRECTORY_NAME_PREFIX}{folder_time}"
    
    if os.path.isdir(path_str) ==  False:
        os.mkdir(path_str)

    os.chdir(path_str)


def add_zeros_to_number(num):
    num_str = str(num)

    num_zeros = 6 - len(num_str)

    if num_zeros > 0:
        return '0' * num_zeros + num_str
    else:
        return num_str


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
        picam2.stop_recording()

        video_counter = video_counter + 1

        print(f"Recorded {output}")
        pin(RECORD_LED_PIN, False)


def stop_program():
    print("\n\n")

    print("Cleaning up GPIO...")
    GPIO.cleanup()

    print("Done")
    exit()



if __name__ == "__main__":
    try:
        video_counter = 0

        setup_pins()

        set_up_folder()

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
        print(e.args)