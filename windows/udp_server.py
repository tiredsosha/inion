import socket
import time
import os
import yaml


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 8009))
    while True:
        try:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            data = data.decode()
            print(data)
            if data == 'sleep':
                os.system(
                    'nircmd exec hide taskkill /f /im RestartOnCrash.exe')
                os.system('nircmd exec hide taskkill /f /im adefrg.exe')
                os.system('nircmd exec hide taskkill /f /im LaserTracker.exe')
            elif data == 'wake':
                os.system('shutdown /r /f')
        except Exception:
            pass


if __name__ == '__main__':
    main()
