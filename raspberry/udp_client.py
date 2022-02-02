import yaml
import time
import socket
import datetime
import os
import RPi.GPIO as GPIO

PINS = (23, 24)


def start_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    GPIO.setup([pin for pin in PINS], GPIO.OUT)
    GPIO.output([pin for pin in PINS], GPIO.HIGH)


def read_files():
    with open('home/pi/kek/configs/pc.yaml') as pc:
        pcs = list(yaml.safe_load(pc).values())
    with open('home/pi/kek/configs/wake.yaml') as wake:
        wake = yaml.safe_load(wake)
        wake_hour = int(wake['hours'])
        wake_mins = int(wake['mins'])
    with open('home/pi/kek/configs/sleep.yaml') as sleep:
        sleep = yaml.safe_load(sleep)
        sleep_hour = int(sleep['hours'])
        sleep_mins = int(sleep['mins'])

    return pcs, wake_hour, wake_mins, sleep_hour, sleep_mins


def send_udp(ip: str, command: str):
    byte_message = bytes(command, "utf-8")
    opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    opened_socket.sendto(byte_message, (ip, 8009))
    opened_socket.close()


def main():
    ips, wake_hour, wake_mins, sleep_hour, sleep_mins = read_files()
    start_gpio()
    index = False

    while True:
        real_hour = int(datetime.datetime.now().time().hour)
        real_min = int(datetime.datetime.now().time().minute)

        if real_hour == wake_hour and wake_mins - 10 <= real_min <= wake_mins and not index:
            try:
                [send_udp(ip, 'wake') for ip in ips]
                index = True
            except Exception:
                [send_udp(ip, 'wake') for ip in ips]
                index = True
            finally:
                os.system('sudo reboot')

            GPIO.output([pin for pin in PINS], GPIO.HIGH)

        elif real_hour == sleep_hour and sleep_mins + 6 <= real_min >= sleep_mins:
            try:
                [send_udp(ip, 'sleep') for ip in ips]
                index = False
            except Exception:
                [send_udp(ip, 'sleep') for ip in ips]
                index = False
            finally:
                os.system('sudo reboot')
            GPIO.output([pin for pin in PINS], GPIO.LOW)

        else:
            time.sleep(60)


if __name__ == '__main__':
    main()
