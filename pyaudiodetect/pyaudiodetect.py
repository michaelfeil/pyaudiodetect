import os
import time
import subprocess
from iot_utils import TapoP100Plug
import logging
import argparse


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
SHUTDOWN_WAIT_TIME = 180  # seconds
POOLING_INTERVAL = 5.5  # seconds


def is_sound_playing() -> bool:
    """
    check if sound is playing by reading the ALSA Sound Card on RaspberryPi
        default for Hifiberry
    """
    out = subprocess.check_output(
        "cat /proc/asound/card*/pcm*p/sub*/hw_params", shell=True
    ).decode("utf-8")
    return not ("closed" in out)


# is_sound_playing = lambda t=1: bool(time.time() % 2)


def main():
    # settings
    parser = argparse.ArgumentParser(description="Description of your program")
    parser.add_argument("-i", "--tapo_ip", type=str, help="Description of TAPO_IP")
    parser.add_argument("-m", "--tapo_mail", type=str, help="Description of TAPO_MAIL")
    parser.add_argument("-p", "--tapo_pw", type=str, help="Description of TAPO_PW")

    args = parser.parse_args()
    on_countdown = SHUTDOWN_WAIT_TIME

    powerplug = TapoP100Plug(args.tapo_ip, args.tapo_mail, args.tapo_pw)
    status = None

    while True:
        is_sound = is_sound_playing()
        logging.info("sound playing % s", is_sound)
        time.sleep(POOLING_INTERVAL)

        if is_sound:
            on_countdown = SHUTDOWN_WAIT_TIME
            if not status or int(on_countdown / POOLING_INTERVAL) % 3 == 0:
                powerplug.on()
                logging.info("Now switch plug on")
                status = True
        else:
            # no sound
            on_countdown -= POOLING_INTERVAL

        if on_countdown < 0:
            powerplug.off()
            status = False
            on_countdown = SHUTDOWN_WAIT_TIME
            logging.info("therefore switch plug OFF")
        else:
            logging.info("switch off in % s", on_countdown)


if __name__ == "__main__":
    main()
