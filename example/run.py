from sys import stderr, exit
from time import sleep
import loghead


def main():
    loghead.init('example/config/jsonout.yaml')
    try:
        while True:
            loghead.debug("Hello, world!");
            loghead.info("Hello, world!");
            loghead.notice("Hello, world!");
            loghead.warning("Hello, world!");
            loghead.error("Hello, world!");
            stderr.write('\n')
            sleep(1)
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
