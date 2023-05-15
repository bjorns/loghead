from sys import stderr, exit
from time import sleep
import kuvio


def main():
    kuvio.init('example/config/jsonout.yaml')
    try:
        while True:
            kuvio.debug("Hello, world!");
            kuvio.info("Hello, world!");
            kuvio.notice("Hello, world!");
            kuvio.warning("Hello, world!");
            kuvio.error("Hello, world!");
            stderr.write('\n')
            sleep(1)
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
