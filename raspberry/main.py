import yaml
import logging
import time

from wakeonlan import send_magic_packet

logging.basicConfig(
    filename="WOL.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def main():
    time.sleep(180)
    with open('config/pc.yaml') as pc:
        pcs = yaml.safe_load(pc)

    def wake():
        for mac in pcs.values():
            send_magic_packet(mac)

    logging.info("Sending packages to wake on lan\n")
    wake()


if __name__ == '__main__':
    main()
