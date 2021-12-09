from requests import get
from os import system
from time import sleep


def ping():
    raspberry = get('172.16.107.1')
    r_status = raspberry.status_code
    pc = get('172.16.107.1')
    pc_status = pc.status_code
    if (r_status == 200 and pc_status == 200) or (pc_status != 200
                                                  and r_status != 200):
        return False
    elif pc_status == 200 and r_status != 200:
        return True


def main():
    while True:
        status = ping()
        if status:
            system("shutdown /f")
        else:
            sleep(30)


main()
